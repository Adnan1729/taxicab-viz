"""Render positive vs mixed regime cumulative count comparison."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from taxicab.io import read_sweep
from taxicab.viz.regime_comparison import plot_regime_comparison
from taxicab.viz.style import savefig, use_publication_style

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES = REPO_ROOT / "figures"
POS_PATH = REPO_ROOT / "data" / "processed" / "sweep_positive_1e9.parquet"
MIX_PATH = REPO_ROOT / "data" / "processed" / "sweep_mixed_b2000.parquet"


def main() -> None:
    for p in (POS_PATH, MIX_PATH):
        if not p.exists():
            raise SystemExit(f"Missing sweep: {p}")

    use_publication_style()
    df_pos, mpos = read_sweep(POS_PATH)
    df_mix, _ = read_sweep(MIX_PATH)

    # Use the positive sweep's n_max for the x-axis extent.
    fig = plot_regime_comparison(df_pos, df_mix, n_max=mpos.n_max)

    out = FIGURES / "regime_comparison.svg"
    savefig(fig, str(out))
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
