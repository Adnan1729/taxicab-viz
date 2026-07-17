"""Compute taxicab representations up to a bound and persist to data/processed/.

Usage:
    python scripts/compute_taxicab.py --n-max 1000000 --n-workers 4
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from taxicab.io import write_sweep
from taxicab.search import SearchConfig, multi_representation_summary, sweep
from taxicab.signs import SignRegime

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "processed"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-max", type=int, required=True, help="Upper bound on N.")
    parser.add_argument("--n-workers", type=int, default=4, help="Multiprocessing workers.")
    parser.add_argument(
        "--regime",
        type=str,
        default="positive",
        choices=[r.value for r in SignRegime],
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Output basename (default: sweep_{regime}_1eN).",
    )
    args = parser.parse_args()

    regime = SignRegime(args.regime)
    name = args.name or f"sweep_{regime.value}_1e{len(str(args.n_max)) - 1}"

    config = SearchConfig(n_max=args.n_max, regime=regime, n_workers=args.n_workers)

    print(f"Sweeping N <= {args.n_max:,} in {regime.value} regime on {args.n_workers} workers...")
    start = time.time()
    df = sweep(config)
    elapsed = time.time() - start
    print(f"Sweep complete in {elapsed:.2f}s: {len(df):,} representations.")

    parquet_path = write_sweep(df, DATA_DIR, name, n_max=args.n_max, regime=regime)
    print(f"Wrote {parquet_path}")

    summary = multi_representation_summary(df)
    print(f"\n{len(summary)} values of N have >= 2 representations.")
    print(summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
