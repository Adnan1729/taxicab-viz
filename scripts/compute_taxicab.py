"""Compute taxicab representations and persist to data/processed/."""

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
    parser.add_argument("--regime", type=str, default="positive", choices=[r.value for r in SignRegime])
    parser.add_argument("--n-max", type=int, help="Output bound (POSITIVE regime).")
    parser.add_argument("--b-max", type=int, help="Input bound |a|,|b| (MIXED regime).")
    parser.add_argument("--n-workers", type=int, default=4)
    parser.add_argument("--name", type=str, default=None)
    args = parser.parse_args()

    regime = SignRegime(args.regime)

    if regime is SignRegime.POSITIVE:
        if args.n_max is None:
            raise SystemExit("POSITIVE regime requires --n-max")
        config = SearchConfig(regime=regime, n_max=args.n_max, n_workers=args.n_workers)
        default_name = f"sweep_positive_1e{len(str(args.n_max)) - 1}"
    else:
        if args.b_max is None:
            raise SystemExit("MIXED regime requires --b-max")
        config = SearchConfig(regime=regime, b_max=args.b_max, n_workers=args.n_workers)
        default_name = f"sweep_mixed_b{args.b_max}"

    name = args.name or default_name

    print(f"Sweeping in {regime.value} regime on {args.n_workers} workers...")
    start = time.time()
    df = sweep(config)
    elapsed = time.time() - start
    print(f"Complete in {elapsed:.2f}s: {len(df):,} representations.")

    parquet_path = write_sweep(
        df, DATA_DIR, name, regime=regime, n_max=args.n_max, b_max=args.b_max
    )
    print(f"Wrote {parquet_path}")

    summary = multi_representation_summary(df)
    print(f"\n{len(summary)} values of N have >= 2 representations.")
    print(summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
