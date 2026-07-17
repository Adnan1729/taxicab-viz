"""Render the classical taxicab curve-overlay figure to figures/.

Usage:
    python scripts/render_curve_overlay.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from taxicab.io import read_sweep
from taxicab.viz.curves import plot_taxicab_grid
from taxicab.viz.style import savefig, use_publication_style

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = REPO_ROOT / "figures"
SWEEP_PATH = REPO_ROOT / "data" / "processed" / "sweep_positive_1e7.parquet"

CLASSICAL_TAXICABS = [1729, 4104, 13832, 20683]


def main() -> None:
    if not SWEEP_PATH.exists():
        raise SystemExit(
            f"Sweep file not found: {SWEEP_PATH}\n"
            "Run: python scripts/compute_taxicab.py --n-max 10000000"
        )

    use_publication_style()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df, _ = read_sweep(SWEEP_PATH)

    # Pull the (a, b) pairs for each classical N.
    entries: list[tuple[int, list[tuple[int, int]]]] = []
    for n in CLASSICAL_TAXICABS:
        rows = df[df["N"] == n]
        if rows.empty:
            raise SystemExit(f"N={n} not found in sweep — did you sweep to at least 20683?")
        pairs = list(zip(rows["a"].astype(int), rows["b"].astype(int), strict=True))
        entries.append((n, pairs))

    fig = plot_taxicab_grid(entries, ncols=2, panel_size=3.8)

    out_path = FIGURES_DIR / "classical_taxicab_curves.svg"
    savefig(fig, str(out_path))
    plt.close(fig)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
