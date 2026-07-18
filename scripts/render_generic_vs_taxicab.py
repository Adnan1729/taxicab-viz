"""Render the pedagogical contrast: typical N vs 1729."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from taxicab.io import read_sweep
from taxicab.viz.curves import plot_generic_vs_taxicab
from taxicab.viz.style import savefig, use_publication_style

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES = REPO_ROOT / "figures"
SWEEP_PATH = REPO_ROOT / "data" / "processed" / "sweep_positive_1e9.parquet"


def main() -> None:
    use_publication_style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    df, _ = read_sweep(SWEEP_PATH)

    generic_n = 1027
    taxicab_n = 1729

    def pairs_for(n: int) -> list[tuple[int, int]]:
        rows = df[df["N"] == n]
        return list(zip(rows["a"].astype(int), rows["b"].astype(int), strict=True))

    fig = plot_generic_vs_taxicab(
        generic_n, pairs_for(generic_n),
        taxicab_n, pairs_for(taxicab_n),
    )
    out = FIGURES / "generic_vs_taxicab.svg"
    savefig(fig, str(out))
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
