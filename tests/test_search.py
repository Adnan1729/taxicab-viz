"""Tests for taxicab.search."""

import pandas as pd
import pytest #type: ignore[import]

from taxicab.search import (
    SearchConfig,
    _icbrt_floor,
    _slice_bounds_mixed,
    _slice_bounds_positive,
    multi_representation_summary,
    sweep,
)
from taxicab.signs import SignRegime


class TestIcbrtFloor:
    def test_perfect_cubes(self) -> None:
        assert _icbrt_floor(0) == 0
        assert _icbrt_floor(1) == 1
        assert _icbrt_floor(8) == 2
        assert _icbrt_floor(1728) == 12

    def test_between_cubes(self) -> None:
        assert _icbrt_floor(2) == 1
        assert _icbrt_floor(9) == 2
        assert _icbrt_floor(1729) == 12
        assert _icbrt_floor(2196) == 12

    def test_large_values(self) -> None:
        assert _icbrt_floor(10**18) == 10**6

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            _icbrt_floor(-1)


class TestSliceBoundsPositive:
    def test_contiguous_no_gaps(self) -> None:
        for n_workers in (1, 2, 3, 4, 7):
            bounds = _slice_bounds_positive(10000, n_workers)
            for start, end in bounds:
                assert start < end
            for (_, end_i), (start_j, _) in zip(bounds, bounds[1:], strict=False):
                assert end_i == start_j
            assert bounds[0][0] == 1


class TestSliceBoundsMixed:
    def test_covers_range(self) -> None:
        for n_workers in (1, 2, 3, 4):
            bounds = _slice_bounds_mixed(100, n_workers)
            assert bounds[0][0] == -100
            assert bounds[-1][1] == 101  # exclusive upper end
            for (_, end_i), (start_j, _) in zip(bounds, bounds[1:], strict=False):
                assert end_i == start_j


class TestSweepPositive:
    def test_finds_ramanujan_number(self) -> None:
        config = SearchConfig(regime=SignRegime.POSITIVE, n_max=2000, n_workers=1)
        df = sweep(config)
        n1729 = df[df["N"] == 1729]
        pairs = set(zip(n1729["a"], n1729["b"], strict=True))
        assert pairs == {(1, 12), (9, 10)}

    def test_no_family_column_in_positive(self) -> None:
        df = sweep(SearchConfig(regime=SignRegime.POSITIVE, n_max=2000))
        assert "family" not in df.columns

    def test_parallel_matches_serial(self) -> None:
        serial = sweep(SearchConfig(regime=SignRegime.POSITIVE, n_max=20000, n_workers=1))
        parallel = sweep(SearchConfig(regime=SignRegime.POSITIVE, n_max=20000, n_workers=4))
        s = set(map(tuple, serial.values.tolist()))
        p = set(map(tuple, parallel.values.tolist()))
        assert s == p


class TestSweepMixed:
    def test_finds_cabtaxi_2(self) -> None:
        """Cabtaxi(2) = 91 = 3^3 + 4^3 = 6^3 + (-5)^3."""
        df = sweep(SearchConfig(regime=SignRegime.MIXED, b_max=10, n_workers=1))
        n91 = df[df["N"] == 91]
        pairs = set(zip(n91["a"], n91["b"], strict=True))
        assert (3, 4) in pairs
        assert (-5, 6) in pairs

    def test_family_column_present(self) -> None:
        df = sweep(SearchConfig(regime=SignRegime.MIXED, b_max=5))
        assert "family" in df.columns

    def test_trivial_family_labeled(self) -> None:
        df = sweep(SearchConfig(regime=SignRegime.MIXED, b_max=20))
        # N = 7 has trivial rep (-1, 2)
        n7 = df[(df["N"] == 7) & (df["a"] == -1) & (df["b"] == 2)]
        assert len(n7) == 1
        assert n7.iloc[0]["family"] == "trivial"

    def test_sporadic_family_labeled(self) -> None:
        df = sweep(SearchConfig(regime=SignRegime.MIXED, b_max=15))
        # 91 = 3^3+4^3 is sporadic
        n91 = df[(df["N"] == 91) & (df["a"] == 3) & (df["b"] == 4)]
        assert len(n91) == 1
        assert n91.iloc[0]["family"] == "sporadic"

    def test_parallel_matches_serial(self) -> None:
        serial = sweep(SearchConfig(regime=SignRegime.MIXED, b_max=30, n_workers=1))
        parallel = sweep(SearchConfig(regime=SignRegime.MIXED, b_max=30, n_workers=4))
        # Compare as sets of (N, a, b); family is deterministic from (a,b) so can drop.
        s = set(zip(serial["N"], serial["a"], serial["b"], strict=True))
        p = set(zip(parallel["N"], parallel["a"], parallel["b"], strict=True))
        assert s == p


class TestSearchConfigValidation:
    def test_positive_requires_n_max(self) -> None:
        with pytest.raises(ValueError):
            SearchConfig(regime=SignRegime.POSITIVE)

    def test_mixed_requires_b_max(self) -> None:
        with pytest.raises(ValueError):
            SearchConfig(regime=SignRegime.MIXED)

    def test_positive_rejects_b_max(self) -> None:
        with pytest.raises(ValueError):
            SearchConfig(regime=SignRegime.POSITIVE, n_max=100, b_max=10)

    def test_mixed_rejects_n_max(self) -> None:
        with pytest.raises(ValueError):
            SearchConfig(regime=SignRegime.MIXED, b_max=10, n_max=100)


class TestMultiRepresentationSummary:
    def test_only_multi_rep_survives(self) -> None:
        df = sweep(SearchConfig(regime=SignRegime.POSITIVE, n_max=5000))
        summary = multi_representation_summary(df, min_count=2)
        assert set(summary["N"].tolist()) == {1729, 4104}
