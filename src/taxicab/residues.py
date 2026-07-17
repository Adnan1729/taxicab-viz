"""Cubic residue analysis for sums of two cubes."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def cubic_residues(m: int) -> set[int]:
    """The set of cubic residues mod m: {x^3 mod m : x in Z_m}."""
    if m <= 0:
        raise ValueError(f"m must be positive, got {m}")
    return {pow(x, 3, m) for x in range(m)}


def sum_of_two_cubes_residues(m: int) -> set[int]:
    """The set of residues achievable as a sum of two cubes mod m."""
    cubes = cubic_residues(m)
    return {(r + s) % m for r in cubes for s in cubes}


def cayley_table(m: int) -> npt.NDArray[np.int64]:
    """m x m grid where cell (i, j) = (i^3 + j^3) mod m."""
    i = np.arange(m).reshape(-1, 1)
    j = np.arange(m).reshape(1, -1)
    return (i**3 + j**3) % m


def unachievable_residues(m: int) -> set[int]:
    """Residues mod m that are NOT expressible as any sum of two cubes."""
    return set(range(m)) - sum_of_two_cubes_residues(m)
