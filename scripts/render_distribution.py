"""Render the two-panel representation-count distribution figure.

Usage:
    python scripts/render_distribution.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from taxicab.io import read_sweep
from taxicab.viz.histograms import plot_distribution_and_growth
from taxicab.viz.style import savefig, use_publication_style

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = REPO_ROOT / "figures"
SWEEP_PATH = REPO_ROOT / "data" / "processed" / "sweep_positive_1e9.parquet"


def main() -> None:
    if not SWEEP_PATH.exists():
        raise SystemExit(
            f"Sweep file not found: {SWEEP_PATH}\n"
            "Run: python scripts/compute_taxicab.py --n-max 1000000000"
        )

    use_publication_style()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df, manifest = read_sweep(SWEEP_PATH)
    fig = plot_distribution_and_growth(df, n_max=manifest.n_max)

    out_path = FIGURES_DIR / "representation_distribution.svg"
    savefig(fig, str(out_path))
    plt.close(fig)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
