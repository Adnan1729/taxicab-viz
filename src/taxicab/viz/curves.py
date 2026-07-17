"""Curve-overlay plots: continuous x^3 + y^3 = N with integer points marked."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt

from taxicab.curves import sample_curve_positive
from taxicab.viz.style import PALETTE


def _format_representation(a: int, b: int) -> str:
    """Render (a, b) as a math-typeset label like '$1^3 + 12^3$'."""
    return f"${a}^3 + {b}^3$"


def plot_curve_with_points(
    ax: plt.Axes,
    n: int,
    representations: Sequence[tuple[int, int]],
    *,
    curve_points: int = 400,
    label_points: bool = True,
) -> None:
    """Draw x^3 + y^3 = N with its integer-point representations marked.

    Parameters
    ----------
    ax : matplotlib Axes
        The panel to draw into.
    n : int
        The value whose curve we're plotting.
    representations : sequence of (a, b) pairs
        Integer points on the curve, with a <= b.
    curve_points : int
        Number of samples for the smooth curve.
    label_points : bool
        If True, annotate each integer point with a^3 + b^3.
    """
    xs, ys = sample_curve_positive(n, n_points=curve_points)

    # Smooth curve.
    ax.plot(xs, ys, color=PALETTE.primary, linewidth=0.9, zorder=2)

    # Integer points, both (a, b) and its mirror (b, a). Outlined markers
    # for the classical look — hollow circle with a black edge.
    for a, b in representations:
        ax.scatter(
            [a, b], [b, a],
            s=32,
            facecolor=PALETTE.background,
            edgecolor=PALETTE.text,
            linewidth=0.9,
            zorder=4,
        )

    if label_points:
        for a, b in representations:
            # Only label the upper-triangle copy (a <= b) to avoid clutter.
            ax.annotate(
                _format_representation(a, b),
                xy=(a, b),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=8,
                color=PALETTE.text,
                zorder=5,
            )

    cbrt_n = n ** (1 / 3)
    ax.set_xlim(-cbrt_n * 0.05, cbrt_n * 1.15)
    ax.set_ylim(-cbrt_n * 0.05, cbrt_n * 1.15)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(f"$N = {n:,}$", fontsize=10, pad=6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")


def plot_taxicab_grid(
    entries: Sequence[tuple[int, Sequence[tuple[int, int]]]],
    ncols: int = 2,
    panel_size: float = 3.8,
) -> plt.Figure:
    """Grid of curve-with-points panels, one per (N, representations) entry.

    Returns the figure — caller is responsible for saving and closing.
    """
    n_panels = len(entries)
    nrows = (n_panels + ncols - 1) // ncols
    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(panel_size * ncols, panel_size * nrows),
        squeeze=False,
    )
    for idx, (n, reps) in enumerate(entries):
        row, col = divmod(idx, ncols)
        plot_curve_with_points(axes[row][col], n, reps)

    for idx in range(n_panels, nrows * ncols):
        row, col = divmod(idx, ncols)
        axes[row][col].axis("off")

    fig.tight_layout()
    return fig
