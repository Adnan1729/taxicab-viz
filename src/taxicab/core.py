"""Core routines: finding integer solutions to a^3 + b^3 = N."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SignRegime = Literal["positive", "mixed"]


@dataclass(frozen=True, order=True)
class Representation:
    """A single (a, b) pair with a <= b such that a^3 + b^3 = N."""

    a: int
    b: int

    def __post_init__(self) -> None:
        if self.a > self.b:
            raise ValueError(f"Representation must satisfy a <= b, got ({self.a}, {self.b}).")

    @property
    def value(self) -> int:
        return self.a**3 + self.b**3


def icbrt(n: int) -> int | None:
    """Exact integer cube root: returns k if n == k^3 for some integer k, else None.

    Handles negative n. Uses integer arithmetic only — no floats.
    """
    if n == 0:
        return 0
    sign = 1 if n > 0 else -1
    n_abs = abs(n)

    # Initial estimate via float, then correct with integer checks.
    # Float is fine as a *starting point*; we verify with exact arithmetic.
    k: int = round(n_abs ** (1 / 3))
    # Search a small window around the estimate to handle float imprecision.
    for candidate in (k - 1, k, k + 1):
        if candidate >= 0 and candidate**3 == n_abs:
            return sign * candidate
    return None


def representations(n: int, regime: SignRegime = "positive") -> list[Representation]:
    """All (a, b) with a <= b and a^3 + b^3 == n, under the given sign regime.

    Parameters
    ----------
    n : int
        Target value.
    regime : {"positive", "mixed"}
        - "positive": require a >= 1 and b >= 1.
        - "mixed":    allow a, b in Z (any signs).

    Notes
    -----
    In the "mixed" regime the identity (k+1)^3 + (-k)^3 = 3k^2 + 3k + 1 means
    infinitely many n have a trivial representation. Callers doing research on
    non-trivial coincidences should filter those out downstream, not here.
    """
    if regime not in ("positive", "mixed"):
        raise ValueError(f"Unknown regime: {regime!r}")

    results: list[Representation] = []

    if regime == "positive":
        if n < 2:  # smallest positive sum is 1^3 + 1^3 = 2
            return results
        # a ranges from 1 to floor(cbrt(n/2)) since a <= b implies 2a^3 <= n.
        a_max = round((n / 2) ** (1 / 3)) + 1
        for a in range(1, a_max + 1):
            if 2 * a**3 > n:
                break
            b_cubed = n - a**3
            b = icbrt(b_cubed)
            if b is not None and b >= a:
                results.append(Representation(a, b))
        return results

    # Mixed regime: a can be negative. Bound: a^3 <= n/2 still holds if we keep a <= b,
    # but a can also be very negative. We bound |a| by (|n| + something) — pragmatically
    # we cap the search at a range provided by the caller in a higher-level function.
    # For now, implement a bounded version and document the limitation.
    raise NotImplementedError(
        "Mixed-regime search needs an explicit bound on |a|; use `representations_bounded`."
    )


def representations_bounded(
    n: int, a_min: int, a_max: int, regime: SignRegime = "mixed"
) -> list[Representation]:
    """All (a, b) with a <= b, a in [a_min, a_max], a^3 + b^3 == n.

    Use this when `regime == "mixed"` since the search space is otherwise unbounded.
    """
    results: list[Representation] = []
    for a in range(a_min, a_max + 1):
        if regime == "positive" and a < 1:
            continue
        b_cubed = n - a**3
        b = icbrt(b_cubed)
        if b is None:
            continue
        if b < a:
            continue
        if regime == "positive" and b < 1:
            continue
        results.append(Representation(a, b))
    return results
