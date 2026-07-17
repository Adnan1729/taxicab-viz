"""Sweep-based search for representations of integers as sums of two cubes."""

from __future__ import annotations

import multiprocessing as mp
from collections.abc import Iterator
from dataclasses import dataclass

import pandas as pd
import numpy as np

from taxicab.signs import Family, SignRegime, classify


@dataclass(frozen=True)
class SearchConfig:
    """Parameters for a sweep.

    For POSITIVE regime, `n_max` bounds the output: we enumerate all (a, b) with
    1 <= a <= b and a^3 + b^3 <= n_max.

    For MIXED regime, `b_max` bounds the input: we enumerate all (a, b) with
    a <= b, |a| <= b_max, |b| <= b_max. Exactly one of n_max / b_max must be
    supplied for each regime.
    """

    regime: SignRegime = SignRegime.POSITIVE
    n_max: int | None = None
    b_max: int | None = None
    n_workers: int = 1

    def __post_init__(self) -> None:
        if self.n_workers < 1:
            raise ValueError(f"n_workers must be >= 1, got {self.n_workers}")
        if self.regime is SignRegime.POSITIVE:
            if self.n_max is None:
                raise ValueError("POSITIVE regime requires n_max.")
            if self.n_max < 2:
                raise ValueError(f"n_max must be >= 2, got {self.n_max}")
            if self.b_max is not None:
                raise ValueError("POSITIVE regime uses n_max, not b_max.")
        else:  # MIXED
            if self.b_max is None:
                raise ValueError("MIXED regime requires b_max.")
            if self.b_max < 1:
                raise ValueError(f"b_max must be >= 1, got {self.b_max}")
            if self.n_max is not None:
                raise ValueError("MIXED regime uses b_max, not n_max.")


def _icbrt_floor(n: int) -> int:
    """Floor of the real cube root of a non-negative integer."""
    if n < 0:
        raise ValueError(f"_icbrt_floor requires n >= 0, got {n}")
    if n == 0:
        return 0
    k = round(n ** (1 / 3))
    while k > 0 and k**3 > n:
        k -= 1
    while (k + 1) ** 3 <= n:
        k += 1
    return k


# ---------- POSITIVE regime ----------


def _sweep_slice_positive(a_start: int, a_end: int, n_max: int) -> list[tuple[int, int, int]]:
    """Emit all (N, a, b) with a in [a_start, a_end), a <= b, a^3 + b^3 <= n_max."""
    rows: list[tuple[int, int, int]] = []
    for a in range(a_start, a_end):
        a3 = a**3
        if 2 * a3 > n_max:
            break
        b_max = _icbrt_floor(n_max - a3)
        for b in range(a, b_max + 1):
            rows.append((a3 + b**3, a, b))
    return rows


def _slice_bounds_positive(n_max: int, n_workers: int) -> list[tuple[int, int]]:
    """Partition the a-range [1, a_max+1) into n_workers contiguous slices."""
    a_max = _icbrt_floor(n_max // 2)
    if a_max < 1:
        return []
    per = (a_max + n_workers - 1) // n_workers
    bounds = []
    for i in range(n_workers):
        start = 1 + i * per
        end = min(1 + (i + 1) * per, a_max + 1)
        if start < end:
            bounds.append((start, end))
    return bounds


def _sweep_slice_positive_star(args: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    return _sweep_slice_positive(*args)


# ---------- MIXED regime ----------


def _sweep_slice_mixed(a_start: int, a_end: int, b_max: int) -> list[tuple[int, int, int]]:
    """Emit all (N, a, b) with a in [a_start, a_end), a <= b, |b| <= b_max, a^3+b^3=N.

    Both a and b are unrestricted in sign; enforce only a <= b canonicalization
    and |b| <= b_max.
    """
    rows: list[tuple[int, int, int]] = []
    for a in range(a_start, a_end):
        for b in range(a, b_max + 1):
            rows.append((a**3 + b**3, a, b))
    return rows


def _slice_bounds_mixed(b_max: int, n_workers: int) -> list[tuple[int, int]]:
    """Partition a-range [-b_max, b_max+1) into n_workers contiguous slices."""
    total = 2 * b_max + 1  # a runs from -b_max to +b_max inclusive
    per = (total + n_workers - 1) // n_workers
    bounds = []
    start = -b_max
    for i in range(n_workers):
        end = min(start + per, b_max + 1)
        if start < end:
            bounds.append((start, end))
        start = end
        if start > b_max:
            break
    return bounds


def _sweep_slice_mixed_star(args: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    return _sweep_slice_mixed(*args)


# ---------- Public API ----------


def sweep(config: SearchConfig) -> pd.DataFrame:
    """Run the sweep. Returns a DataFrame with columns (N, a, b[, family]).

    For POSITIVE regime, no `family` column (all sporadic by construction —
    trivial family is a mixed-regime concept).
    For MIXED regime, includes a `family` column with values 'trivial' or 'sporadic'.
    """
    if config.regime is SignRegime.POSITIVE:
        assert config.n_max is not None  # narrowed by __post_init__
        return _sweep_positive(config.n_max, config.n_workers)
    else:
        assert config.b_max is not None
        return _sweep_mixed(config.b_max, config.n_workers)


def _sweep_positive(n_max: int, n_workers: int) -> pd.DataFrame:
    bounds = _slice_bounds_positive(n_max, n_workers)
    if n_workers == 1 or len(bounds) <= 1:
        all_rows: list[tuple[int, int, int]] = []
        for start, end in bounds:
            all_rows.extend(_sweep_slice_positive(start, end, n_max))
    else:
        args = [(start, end, n_max) for start, end in bounds]
        with mp.Pool(processes=n_workers) as pool:
            chunks = pool.map(_sweep_slice_positive_star, args)
        all_rows = [row for chunk in chunks for row in chunk]

    df = pd.DataFrame(all_rows, columns=["N", "a", "b"])
    df = df.astype({"N": "int64", "a": "int32", "b": "int32"})
    return df


def _sweep_mixed(b_max: int, n_workers: int) -> pd.DataFrame:
    bounds = _slice_bounds_mixed(b_max, n_workers)
    if n_workers == 1 or len(bounds) <= 1:
        all_rows: list[tuple[int, int, int]] = []
        for start, end in bounds:
            all_rows.extend(_sweep_slice_mixed(start, end, b_max))
    else:
        args = [(start, end, b_max) for start, end in bounds]
        with mp.Pool(processes=n_workers) as pool:
            chunks = pool.map(_sweep_slice_mixed_star, args)
        all_rows = [row for chunk in chunks for row in chunk]

    df = pd.DataFrame(all_rows, columns=["N", "a", "b"])
    is_trivial = (df["b"] == 1 - df["a"]) & (df["a"] <= 0)
    df["family"] = pd.Series(
        np.where(is_trivial, Family.TRIVIAL.value, Family.SPORADIC.value),
        index=df.index,
    )
    df = df.astype({"N": "int64", "a": "int32", "b": "int32", "family": "category"})
    return df


def multi_representation_summary(df: pd.DataFrame, min_count: int = 2) -> pd.DataFrame:
    """Return N values with >= min_count representations, with their counts."""
    counts = df.groupby("N").size().rename("count").reset_index()
    return counts[counts["count"] >= min_count].sort_values("N").reset_index(drop=True)


def iter_representations_by_n(df: pd.DataFrame) -> Iterator[tuple[int, pd.DataFrame]]:
    """Iterate over N values with their representation rows."""
    for n_value, group in df.groupby("N"):
        cols = ["a", "b"]
        if "family" in group.columns:
            cols.append("family")
        yield int(n_value), group[cols].reset_index(drop=True)
