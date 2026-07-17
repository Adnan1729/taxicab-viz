"""Tests for taxicab.search."""

import pandas as pd
import pytest

from taxicab.search import (
    SearchConfig,
    _icbrt_floor,
    _slice_bounds,
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
        assert _icbrt_floor(7) == 1
        assert _icbrt_floor(9) == 2
        assert _icbrt_floor(1729) == 12
        assert _icbrt_floor(2196) == 12  # 12^3 = 1728, 13^3 = 2197

    def test_large_values(self) -> None:
        assert _icbrt_floor(10**18) == 10**6
        assert _icbrt_floor(10**18 - 1) == 10**6 - 1

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            _icbrt_floor(-1)


class TestSliceBounds:
    def test_partitions_are_disjoint_and_cover(self) -> None:
        n_max = 10000
        for n_workers in (1, 2, 3, 4, 7):
            bounds = _slice_bounds(n_max, n_workers)
            # Each slice non-empty
            for start, end in bounds:
                assert start < end
            # Contiguous, no gaps, no overlaps
            for (_, end_i), (start_j, _) in zip(bounds, bounds[1:], strict=False):
                assert end_i == start_j
            # Covers 1..a_max inclusive where a_max = floor((n_max/2)^(1/3))
            assert bounds[0][0] == 1
            expected_a_max = int((n_max / 2) ** (1 / 3)) + 2  # loose upper
            assert bounds[-1][1] <= expected_a_max + 1


class TestSweep:
    def test_finds_ramanujan_number(self) -> None:
        config = SearchConfig(n_max=2000, regime=SignRegime.POSITIVE, n_workers=1)
        df = sweep(config)
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == {"N", "a", "b"}

        n1729 = df[df["N"] == 1729]
        pairs = set(zip(n1729["a"], n1729["b"], strict=True))
        assert pairs == {(1, 12), (9, 10)}

    def test_finds_second_taxicab(self) -> None:
        config = SearchConfig(n_max=5000, regime=SignRegime.POSITIVE, n_workers=1)
        df = sweep(config)
        n4104 = df[df["N"] == 4104]
        pairs = set(zip(n4104["a"], n4104["b"], strict=True))
        assert pairs == {(2, 16), (9, 15)}

    def test_a_leq_b_invariant(self) -> None:
        config = SearchConfig(n_max=10000, regime=SignRegime.POSITIVE)
        df = sweep(config)
        assert (df["a"] <= df["b"]).all()

    def test_sum_of_cubes_invariant(self) -> None:
        config = SearchConfig(n_max=10000, regime=SignRegime.POSITIVE)
        df = sweep(config)
        assert (df["a"] ** 3 + df["b"] ** 3 == df["N"]).all()

    def test_parallel_matches_serial(self) -> None:
        """Multi-worker result should match single-worker as a set of rows."""
        n_max = 20000
        serial = sweep(SearchConfig(n_max=n_max, n_workers=1))
        parallel = sweep(SearchConfig(n_max=n_max, n_workers=4))
        serial_rows = set(map(tuple, serial.values.tolist()))
        parallel_rows = set(map(tuple, parallel.values.tolist()))
        assert serial_rows == parallel_rows

    def test_mixed_regime_not_yet_implemented(self) -> None:
        with pytest.raises(NotImplementedError):
            SearchConfig(n_max=100, regime=SignRegime.MIXED)


class TestMultiRepresentationSummary:
    def test_only_multi_rep_survives(self) -> None:
        config = SearchConfig(n_max=5000, n_workers=1)
        df = sweep(config)
        summary = multi_representation_summary(df, min_count=2)
        assert set(summary["N"].tolist()) == {1729, 4104}
        assert summary[summary["N"] == 1729]["count"].iloc[0] == 2
