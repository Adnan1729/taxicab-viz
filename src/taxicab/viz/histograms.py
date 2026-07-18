"""Representation-count distributions and cumulative growth plots."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from taxicab.viz.style import PALETTE


def plot_count_distribution(
    ax: plt.Axes,
    df: pd.DataFrame,
    *,
    log_y: bool = True,
) -> None:
    """Bar chart: how many N have exactly k representations, for each k present.

    Uses unfilled (hollow) bars — the classical scientific convention.
    """
    counts_per_n = df.groupby("N").size()
    dist = counts_per_n.value_counts().sort_index()

    ks = dist.index.to_numpy()
    values = dist.to_numpy()

    bars = ax.bar(
        ks,
        values,
        edgecolor=PALETTE.text,
        facecolor=PALETTE.background,
        linewidth=0.9,
        width=0.6,
    )

    if log_y:
        ax.set_yscale("log")

    for bar, value in zip(bars, values, strict=True):
        ax.annotate(
            f"{value:,}",
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color=PALETTE.text,
        )

    ax.set_xlabel("Number of representations k")
    ax.set_ylabel("Count of N" + (" (log scale)" if log_y else ""))
    ax.set_xticks(ks)
    ax.set_xlim(ks.min() - 0.6, ks.max() + 0.6)
    if log_y:
        ax.set_ylim(0.5, values.max() * 3)
    else:
        ax.set_ylim(0, values.max() * 1.15)


def plot_cumulative_growth(
    ax: plt.Axes,
    df: pd.DataFrame,
    *,
    thresholds: Sequence[int] = (1, 2),
    reference_slopes: Sequence[float] = (2 / 3,),
    n_max: int | None = None,
) -> None:
    """Log-log cumulative counts of N ≤ x with ≥ k representations.

    Data lines are text-colored, distinguished by linestyle. Reference power-law
    slopes are drawn in accent_1 and anchored below the sparsest data line so
    they don't get occluded.
    """
    counts_per_n = df.groupby("N").size().sort_index()
    n_values = counts_per_n.index.to_numpy()
    counts_arr = counts_per_n.to_numpy()
    if n_max is None:
        n_max = int(n_values.max())

    linestyles = ["-", "--", ":"]

    # Track the sparsest line's endpoint so the reference can be anchored below it.
    sparsest_top: float | None = None

    for i, k in enumerate(thresholds):
        qualifying = n_values[counts_arr >= k]
        if len(qualifying) == 0:
            continue
        cumulative = np.arange(1, len(qualifying) + 1)
        ax.plot(
            qualifying,
            cumulative,
            color=PALETTE.text,
            linestyle=linestyles[i % len(linestyles)],
            linewidth=0.9,
            label=f"\u2265 {k} representations",
            zorder=3,
        )
        # Remember the highest threshold seen — its top y is the sparsest.
        if sparsest_top is None or float(cumulative[-1]) < sparsest_top:
            sparsest_top = float(cumulative[-1])

    # Reference: anchor below the sparsest data line, in the empty middle band
    # of the plot, so it isn't hidden underneath a solid line of the same color.
    if sparsest_top is not None:
        x_ref = np.logspace(
            np.log10(max(float(n_values.min()), 1e3)), np.log10(n_max), 50
        )
        anchor_y = sparsest_top * 0.35  # 35% below the sparsest line's endpoint
        for slope in reference_slopes:
            c = anchor_y / (n_max**slope)
            y_ref = c * x_ref**slope
            ax.plot(
                x_ref,
                y_ref,
                color=PALETTE.accent_1,
                linestyle="--",
                linewidth=1.0,
                label=f"x^{slope:.3g} reference",
                zorder=2,
            )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N (log scale)")
    ax.set_ylabel("Count of qualifying N \u2264 x (log scale)")
    ax.legend(loc="lower right")

def plot_distribution_and_growth(df: pd.DataFrame, n_max: int) -> plt.Figure:
    """Two-panel figure: left = count distribution, right = cumulative growth."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10.5, 4.5))
    plot_count_distribution(ax_left, df)
    ax_left.set_title("Distribution of representation counts", fontsize=11, pad=10)

    plot_cumulative_growth(ax_right, df, thresholds=(1, 2), n_max=n_max)
    ax_right.set_title("Cumulative growth vs Hooley's asymptotic", fontsize=11, pad=10)

    fig.tight_layout()
    return fig
