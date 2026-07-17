"""Positive vs mixed regime cumulative-count comparison."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from taxicab.viz.style import PALETTE


def _cumulative_line(ax: plt.Axes, n_values: np.ndarray, label: str, linestyle: str) -> None:
    if len(n_values) == 0:
        return
    n_sorted = np.sort(n_values)
    cumulative = np.arange(1, len(n_sorted) + 1)
    ax.plot(n_sorted, cumulative, color=PALETTE.text, linestyle=linestyle, linewidth=0.9, label=label)


def plot_regime_comparison(
    df_positive: pd.DataFrame,
    df_mixed: pd.DataFrame,
    n_max: int,
) -> plt.Figure:
    """Two-panel figure: positive regime (left) vs mixed regime (right), both log-log."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10.5, 4.5), sharey=True)

    # --- Left: positive regime ---
    counts_pos = df_positive.groupby("N").size()
    multi_pos = counts_pos[counts_pos >= 2].index.to_numpy()
    _cumulative_line(ax_left, multi_pos, r"$\geq 2$ reps", "-")

    # Hooley x^(2/3) reference
    x_ref = np.logspace(3, np.log10(n_max), 50)
    y_ref = (len(multi_pos) / n_max ** (2 / 3)) * x_ref ** (2 / 3)
    ax_left.plot(x_ref, y_ref, color=PALETTE.accent_1, linestyle="-.", linewidth=0.8,
                 label=r"$x^{2/3}$ reference")

    ax_left.set_xscale("log")
    ax_left.set_yscale("log")
    ax_left.set_xlabel("$N$")
    ax_left.set_ylabel("Cumulative count of multi-rep $N \\leq x$")
    ax_left.set_title("Positive regime", pad=8)
    ax_left.legend(loc="lower right")

    # --- Right: mixed regime, split by family composition ---
    pos_df = df_mixed[df_mixed["N"] > 0]
    grouped = pos_df.groupby("N")
    counts_mix = grouped.size()
    multi_n = counts_mix[counts_mix >= 2].index

    # For each multi-rep N, does it have any trivial reps?
    has_trivial = grouped["family"].apply(lambda s: (s == "trivial").any())
    all_multi = multi_n.to_numpy()
    sporadic_only = multi_n[~has_trivial.loc[multi_n]].to_numpy()
    with_trivial = multi_n[has_trivial.loc[multi_n]].to_numpy()

    _cumulative_line(ax_right, all_multi, "all multi-rep", "-")
    _cumulative_line(ax_right, sporadic_only, "sporadic only", "--")
    _cumulative_line(ax_right, with_trivial, "trivial-crossing", ":")

    ax_right.set_xscale("log")
    ax_right.set_yscale("log")
    ax_right.set_xlabel("$N$")
    ax_right.set_title("Mixed regime (positive $N$ only)", pad=8)
    ax_right.legend(loc="lower right")

    fig.tight_layout()
    return fig
