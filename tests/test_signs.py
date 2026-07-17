"""Tests for taxicab.signs."""

from taxicab.signs import Family, classify, is_trivial_mixed


class TestIsTrivialMixed:
    def test_positive_examples(self) -> None:
        # (a, 1-a) with a <= 0 → trivial
        assert is_trivial_mixed(0, 1)   # gives N = 1
        assert is_trivial_mixed(-1, 2)  # gives N = 7 = 3*1^2 + 3*1 + 1
        assert is_trivial_mixed(-5, 6)  # gives N = 91
        assert is_trivial_mixed(-10, 11)

    def test_negative_examples(self) -> None:
        assert not is_trivial_mixed(3, 4)      # 91 = 3^3+4^3, but not trivial
        assert not is_trivial_mixed(1, 12)     # 1729
        assert not is_trivial_mixed(1, 2)      # b != 1-a
        assert not is_trivial_mixed(-2, 4)     # b != 1-a


class TestClassify:
    def test_trivial(self) -> None:
        assert classify(-5, 6) is Family.TRIVIAL

    def test_sporadic(self) -> None:
        assert classify(3, 4) is Family.SPORADIC
        assert classify(1, 12) is Family.SPORADIC
