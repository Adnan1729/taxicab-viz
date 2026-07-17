# """Residue heatmaps: which sums are achievable mod m."""

# from __future__ import annotations

# import matplotlib.pyplot as plt
# import numpy as np

# from taxicab.residues import cayley_table, unachievable_residues
# from taxicab.viz.style import PALETTE


# def plot_cayley_mod(ax: plt.Axes, m: int) -> None:
#     """Draw the m x m table of (i^3 + j^3) mod m.

#     Cells whose value lies in an unachievable residue class are lightly shaded
#     to distinguish them. Cell labels show the residue itself.
#     """
#     table = cayley_table(m)
#     unachievable = unachievable_residues(m)

#     # Build a color mask: 0 for achievable-residue cells, 1 for unachievable.
#     # (There are no unachievable *cells* — every cell's value is by definition
#     # achievable. So the mask is uniformly zero. This is the whole point.)
#     # Instead: shade cells whose ROW OR COLUMN index equals an unachievable residue,
#     # to highlight what's missing from the residue set on the axes.
#     #
#     # Actually the cleanest thing is to overlay row/column highlighting for
#     # unachievable residues on the axes themselves via tick color, and to
#     # annotate the table cells with the residues.

#     ax.imshow(
#         np.zeros_like(table),
#         cmap="Greys",
#         vmin=0,
#         vmax=1,
#         aspect="equal",
#     )

#     # Annotate every cell with its residue value.
#     for i in range(m):
#         for j in range(m):
#             ax.text(
#                 j, i, str(table[i, j]),
#                 ha="center", va="center",
#                 fontsize=7,
#                 color=PALETTE.text,
#             )

#     # Ticks: 0..m-1 on both axes, with unachievable residues highlighted.
#     ax.set_xticks(range(m))
#     ax.set_yticks(range(m))
#     ax.set_xticklabels(
#         [f"$\\mathbf{{{k}}}$" if k in unachievable else str(k) for k in range(m)],
#         fontsize=8,
#     )
#     ax.set_yticklabels(
#         [f"$\\mathbf{{{k}}}$" if k in unachievable else str(k) for k in range(m)],
#         fontsize=8,
#     )
#     ax.set_xlabel("$j$")
#     ax.set_ylabel("$i$")
#     ax.set_title(
#         f"$i^3 + j^3$ mod ${m}$" +
#         (f"\nunachievable: {sorted(unachievable)}" if unachievable else "\nall achievable"),
#         fontsize=10, pad=8,
#     )

#     # Hide the grid — it competes with the numeric labels.
#     ax.grid(False)


# def plot_residue_analysis(moduli: tuple[int, ...] = (7, 9)) -> plt.Figure:
#     """Row of Cayley tables for the given moduli."""
#     fig, axes = plt.subplots(1, len(moduli), figsize=(4.2 * len(moduli), 4.5))
#     if len(moduli) == 1:
#         axes = [axes]
#     for ax, m in zip(axes, moduli, strict=True):
#         plot_cayley_mod(ax, m)
#     fig.tight_layout()
#     return fig

"""Cubic residue analysis: bar charts of representability."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from taxicab.residues import cayley_table, unachievable_residues
from taxicab.viz.style import PALETTE


def plot_residue_frequencies(ax: plt.Axes, m: int) -> None:
    """Bar chart: for each residue r mod m, count of (i,j) pairs with i^3+j^3 ≡ r."""
    table = cayley_table(m)
    counts = np.bincount(table.flatten(), minlength=m)
    unachievable = unachievable_residues(m)
    residues = np.arange(m)

    bars = ax.bar(
        residues,
        counts,
        edgecolor=PALETTE.text,
        facecolor=PALETTE.background,
        linewidth=0.9,
        width=0.7,
    )

    # Mark unachievable residues explicitly with a small tick or annotation.
    # Their bar height is 0, but a visible cue helps.
    for r in unachievable:
        ax.text(
            r, -m * 0.15,  # position below the axis, scaled by grid size
            "×",
            ha="center", va="top",
            fontsize=12,
            color=PALETTE.accent_1,
            fontweight="bold",
        )

    ax.set_xticks(residues)
    ax.set_xlabel(f"Residue $r$ mod {m}")
    ax.set_ylabel("Number of $(i,j)$ pairs with $i^3+j^3 \\equiv r$")
    ax.set_title(
        f"Sums of two cubes mod {m}\n"
        f"({m - len(unachievable)}/{m} residues achievable)",
        pad=8,
    )
    # Give a little headroom below for the × marks.
    ax.set_ylim(-m * 0.25, counts.max() * 1.1)


def plot_residue_analysis(moduli: tuple[int, ...] = (7, 9)) -> plt.Figure:
    """Row of residue-frequency bar charts."""
    fig, axes = plt.subplots(1, len(moduli), figsize=(4.5 * len(moduli), 4.0))
    if len(moduli) == 1:
        axes = [axes]
    for ax, m in zip(axes, moduli, strict=True):
        plot_residue_frequencies(ax, m)
    fig.tight_layout()
    return fig
