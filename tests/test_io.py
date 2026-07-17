"""Tests for taxicab.io."""

from pathlib import Path

import pandas as pd

from taxicab.io import SweepManifest, read_sweep, write_sweep
from taxicab.signs import SignRegime


def test_round_trip(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {"N": [1729, 1729, 4104, 4104], "a": [1, 9, 2, 9], "b": [12, 10, 16, 15]}
    ).astype({"N": "int64", "a": "int32", "b": "int32"})

    parquet_path = write_sweep(df, tmp_path, "test", n_max=5000, regime=SignRegime.POSITIVE)

    assert parquet_path.exists()
    assert parquet_path.with_suffix(".json").exists()

    df_read, manifest = read_sweep(parquet_path)
    pd.testing.assert_frame_equal(df.reset_index(drop=True), df_read.reset_index(drop=True))

    assert manifest.n_max == 5000
    assert manifest.regime == "positive"
    assert manifest.n_representations == 4
    assert manifest.n_multi_rep == 2


def test_manifest_json_round_trip() -> None:
    m = SweepManifest(
        n_max=1000,
        regime="positive",
        n_representations=10,
        n_multi_rep=1,
        created_utc="2026-01-01T00:00:00+00:00",
    )
    assert SweepManifest.from_json(m.to_json()) == m
