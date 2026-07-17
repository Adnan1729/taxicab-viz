"""Tests for taxicab.core."""

from taxicab.core import Representation, icbrt, representations, representations_bounded


class TestIcbrt:
    def test_perfect_cubes(self) -> None:
        assert icbrt(0) == 0
        assert icbrt(1) == 1
        assert icbrt(8) == 2
        assert icbrt(1728) == 12
        assert icbrt(1000000) == 100

    def test_negative_perfect_cubes(self) -> None:
        assert icbrt(-1) == -1
        assert icbrt(-27) == -3
        assert icbrt(-1728) == -12

    def test_non_cubes_return_none(self) -> None:
        assert icbrt(2) is None
        assert icbrt(9) is None
        assert icbrt(1727) is None
        assert icbrt(1729) is None  # 1729 is a sum of cubes, not itself a cube


class TestRepresentationsPositive:
    def test_ramanujan_1729(self) -> None:
        """1729 = 1^3 + 12^3 = 9^3 + 10^3 — the Hardy-Ramanujan number."""
        reps = representations(1729, regime="positive")
        assert set(reps) == {Representation(1, 12), Representation(9, 10)}

    def test_second_taxicab_4104(self) -> None:
        """4104 = 2^3 + 16^3 = 9^3 + 15^3."""
        reps = representations(4104, regime="positive")
        assert set(reps) == {Representation(2, 16), Representation(9, 15)}

    def test_no_representations_for_small_n(self) -> None:
        assert representations(1, regime="positive") == []
        assert representations(0, regime="positive") == []

    def test_unique_representation(self) -> None:
        # 2 = 1 + 1, exactly one representation.
        assert representations(2, regime="positive") == [Representation(1, 1)]

    def test_a_leq_b_invariant(self) -> None:
        for rep in representations(4104, regime="positive"):
            assert rep.a <= rep.b


class TestRepresentationsBounded:
    def test_mixed_finds_trivial_family(self) -> None:
        """3k^2 + 3k + 1 = (k+1)^3 + (-k)^3. Check for k=1: n=7 = 2^3 + (-1)^3."""
        reps = representations_bounded(7, a_min=-10, a_max=10, regime="mixed")
        assert Representation(-1, 2) in reps

    def test_mixed_finds_91(self) -> None:
        """Cabtaxi(2) = 91 = 3^3 + 4^3 = 6^3 + (-5)^3."""
        reps = representations_bounded(91, a_min=-20, a_max=20, regime="mixed")
        assert Representation(3, 4) in reps
        assert Representation(-5, 6) in reps


class TestRepresentationInvariants:
    def test_rejects_a_greater_than_b(self) -> None:
        try:
            Representation(5, 3)
        except ValueError:
            pass
        else:
            raise AssertionError("Expected ValueError for a > b")

    def test_value_matches_definition(self) -> None:
        rep = Representation(9, 10)
        assert rep.value == 9**3 + 10**3 == 1729
