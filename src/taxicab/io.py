"""Persistence: read/write sweep results as parquet, with a sidecar manifest."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from taxicab.signs import SignRegime


@dataclass(frozen=True)
class SweepManifest:
    """Metadata about a persisted sweep result.

    Written as JSON alongside the parquet file. Ensures every artifact on disk
    carries enough context to be reproduced or understood later without
    grepping through code.
    """

    n_max: int
    regime: str
    n_representations: int
    n_multi_rep: int
    created_utc: str
    schema_version: int = 1

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, text: str) -> SweepManifest:
        return cls(**json.loads(text))


def write_sweep(df: pd.DataFrame, out_dir: Path, name: str, *, n_max: int, regime: SignRegime) -> Path:
    """Write a sweep result to `out_dir/name.parquet` with a `.json` sidecar.

    Returns the parquet path.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = out_dir / f"{name}.parquet"
    manifest_path = out_dir / f"{name}.json"

    df.to_parquet(parquet_path, engine="pyarrow", compression="snappy", index=False)

    counts = df.groupby("N").size()
    manifest = SweepManifest(
        n_max=n_max,
        regime=regime.value,
        n_representations=len(df),
        n_multi_rep=int((counts >= 2).sum()),
        created_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    manifest_path.write_text(manifest.to_json())
    return parquet_path


def read_sweep(parquet_path: Path) -> tuple[pd.DataFrame, SweepManifest]:
    """Read a parquet + sidecar produced by `write_sweep`."""
    parquet_path = Path(parquet_path)
    manifest_path = parquet_path.with_suffix(".json")
    df = pd.read_parquet(parquet_path, engine="pyarrow")
    manifest = SweepManifest.from_json(manifest_path.read_text())
    return df, manifest
