"""Render the cubic-residue Cayley tables for mod 7 and mod 9."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from taxicab.viz.residues import plot_residue_analysis
from taxicab.viz.style import savefig, use_publication_style

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES = REPO_ROOT / "figures"


def main() -> None:
    use_publication_style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig = plot_residue_analysis(moduli=(7, 9))
    out = FIGURES / "cubic_residues.svg"
    savefig(fig, str(out))
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
