"""Tests for taxicab.io."""

from pathlib import Path

import pandas as pd

from taxicab.io import SweepManifest, read_sweep, write_sweep
from taxicab.signs import SignRegime


def test_round_trip_positive(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {"N": [1729, 1729, 4104, 4104], "a": [1, 9, 2, 9], "b": [12, 10, 16, 15]}
    ).astype({"N": "int64", "a": "int32", "b": "int32"})

    parquet_path = write_sweep(df, tmp_path, "test", regime=SignRegime.POSITIVE, n_max=5000)
    df_read, manifest = read_sweep(parquet_path)

    pd.testing.assert_frame_equal(df.reset_index(drop=True), df_read.reset_index(drop=True))
    assert manifest.n_max == 5000
    assert manifest.b_max is None
    assert manifest.regime == "positive"


def test_round_trip_mixed(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {
            "N": [91, 91, 7],
            "a": [3, -5, -1],
            "b": [4, 6, 2],
            "family": pd.Categorical(["sporadic", "sporadic", "trivial"]),
        }
    ).astype({"N": "int64", "a": "int32", "b": "int32"})

    parquet_path = write_sweep(df, tmp_path, "test_mixed", regime=SignRegime.MIXED, b_max=10)
    df_read, manifest = read_sweep(parquet_path)

    assert manifest.b_max == 10
    assert manifest.n_max is None
    assert manifest.regime == "mixed"
    assert "family" in df_read.columns


def test_manifest_json_round_trip() -> None:
    m = SweepManifest(
        regime="mixed",
        n_representations=100,
        n_multi_rep=5,
        created_utc="2026-01-01T00:00:00+00:00",
        b_max=50,
    )
    assert SweepManifest.from_json(m.to_json()) == m
