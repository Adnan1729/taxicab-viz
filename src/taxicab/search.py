"""Sweep-based search for representations of integers as sums of two cubes.

Enumerates pairs (a, b) with a <= b and a^3 + b^3 <= N_max, then groups by
a^3 + b^3 to find multi-representation values.
"""

from __future__ import annotations

import multiprocessing as mp
from collections.abc import Iterator
from dataclasses import dataclass

import pandas as pd

from taxicab.signs import SignRegime

from typing import cast, Any, Iterator


@dataclass(frozen=True)
class SearchConfig:
    """Parameters for a sweep."""

    n_max: int
    regime: SignRegime = SignRegime.POSITIVE
    n_workers: int = 1  # 1 = single-threaded (no multiprocessing overhead)

    def __post_init__(self) -> None:
        if self.n_max < 2:
            raise ValueError(f"n_max must be >= 2, got {self.n_max}")
        if self.n_workers < 1:
            raise ValueError(f"n_workers must be >= 1, got {self.n_workers}")
        if self.regime is SignRegime.MIXED:
            # Deferred to Phase 2 — mixed regime needs a different enumeration
            # strategy (bounded |a|, |b|) and separate treatment of the trivial family.
            raise NotImplementedError("MIXED regime sweep not implemented yet.")


def _icbrt_floor(n: int) -> int:
    """Floor of the real cube root of a non-negative integer.

    Used to bound loop ranges. For n < 0 the notion is unused here.
    """
    if n < 0:
        raise ValueError(f"_icbrt_floor requires n >= 0, got {n}")
    if n == 0:
        return 0
    k = int(round(n ** (1 / 3)))
    # Correct for float error: shrink until k^3 <= n, then grow while (k+1)^3 <= n.
    while k > 0 and k**3 > n:
        k -= 1
    while (k + 1) ** 3 <= n:
        k += 1
    return k


def _sweep_slice(a_start: int, a_end: int, n_max: int) -> list[tuple[int, int, int]]:
    """Emit all (N, a, b) with a in [a_start, a_end), a <= b, a^3 + b^3 <= n_max.

    POSITIVE regime only (a >= 1 enforced by caller via a_start).
    """
    rows: list[tuple[int, int, int]] = []
    for a in range(a_start, a_end):
        a3 = a**3
        if 2 * a3 > n_max:  # a <= b implies 2a^3 <= N <= n_max
            break
        b_max = _icbrt_floor(n_max - a3)
        for b in range(a, b_max + 1):
            rows.append((a3 + b**3, a, b))
    return rows


def _slice_bounds(n_max: int, n_workers: int) -> list[tuple[int, int]]:
    """Partition the a-range [1, a_max+1) into n_workers contiguous slices.

    Uses equal-width slicing on `a`. Note: the *work* per slice is not equal
    (small `a` has more `b` values). A more balanced scheme would slice on
    a^2 or use dynamic scheduling, but equal-width is fine for a first pass
    and easier to reason about.
    """
    a_max = _icbrt_floor(n_max // 2)  # largest a with 2a^3 <= n_max
    if a_max < 1:
        return []
    total = a_max  # a runs 1..a_max inclusive
    per = (total + n_workers - 1) // n_workers  # ceil division
    bounds = []
    for i in range(n_workers):
        start = 1 + i * per
        end = min(1 + (i + 1) * per, a_max + 1)
        if start < end:
            bounds.append((start, end))
    return bounds


def _sweep_slice_star(args: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """Adapter so multiprocessing.Pool.map can pass a tuple as args."""
    return _sweep_slice(*args)


def sweep(config: SearchConfig) -> pd.DataFrame:
    """Run the sweep and return a long-format DataFrame with columns (N, a, b).

    Rows are unsorted; caller can sort or group as needed. Every row satisfies
    a <= b and a^3 + b^3 == N.
    """
    bounds = _slice_bounds(config.n_max, config.n_workers)

    if config.n_workers == 1 or len(bounds) <= 1:
        all_rows: list[tuple[int, int, int]] = []
        for start, end in bounds:
            all_rows.extend(_sweep_slice(start, end, config.n_max))
    else:
        args = [(start, end, config.n_max) for start, end in bounds]
        with mp.Pool(processes=config.n_workers) as pool:
            chunks = pool.map(_sweep_slice_star, args)
        all_rows = [row for chunk in chunks for row in chunk]

    df = pd.DataFrame(all_rows, columns=["N", "a", "b"])
    # Downcast to the smallest int dtype that fits — matters for a big parquet file.
    df = df.astype({"N": "int64", "a": "int32", "b": "int32"})
    return df


def multi_representation_summary(df: pd.DataFrame, min_count: int = 2) -> pd.DataFrame:
    """Given the long-format output of `sweep`, return N values with >= min_count
    representations, along with their counts. Sorted by N ascending.
    """
    counts = df.groupby("N").size().rename("count").reset_index()
    return counts[counts["count"] >= min_count].sort_values("N").reset_index(drop=True)


def iter_representations_by_n(df: pd.DataFrame) -> Iterator[tuple[int, pd.DataFrame]]:
    """Iterate over N values with their group of representation rows.

    Convenience for plotting code: for each multi-rep N, get its (a, b) pairs.
    """
    for n_value, group in df.groupby("N"):
        yield int(cast(Any, n_value)), group[["a", "b"]].reset_index(drop=True)
