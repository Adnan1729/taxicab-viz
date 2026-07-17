"""Tests for cubic residue analysis."""

from taxicab.residues import (
    cayley_table,
    cubic_residues,
    sum_of_two_cubes_residues,
    unachievable_residues,
)


def test_cubic_residues_mod_7() -> None:
    # x^3 mod 7 for x in 0..6: {0, 1, 1, 6, 1, 6, 6} → {0, 1, 6}
    assert cubic_residues(7) == {0, 1, 6}


def test_cubic_residues_mod_9() -> None:
    # x^3 mod 9 for x in 0..8 → {0, 1, 8}
    assert cubic_residues(9) == {0, 1, 8}


def test_sum_of_two_cubes_mod_7() -> None:
    # {0,1,6} + {0,1,6} mod 7 = {0,1,2,5,6} (missing 3, 4)
    assert sum_of_two_cubes_residues(7) == {0, 1, 2, 5, 6}


def test_unachievable_mod_7() -> None:
    assert unachievable_residues(7) == {3, 4}


def test_unachievable_mod_9() -> None:
    # Sums: {0,1,8} + {0,1,8} mod 9 = {0,1,2,7,8} (missing 3,4,5,6)
    # Wait: 1+8=9→0, 8+8=16→7. So set = {0, 1, 2, 7, 8}. Missing = {3,4,5,6}.
    assert unachievable_residues(9) == {3, 4, 5, 6}


def test_cayley_table_shape() -> None:
    t = cayley_table(7)
    assert t.shape == (7, 7)
    assert t[1, 12 % 7] == (1 + 12**3) % 7  # 1^3 + 5^3 = 126, 126 mod 7 = 0
