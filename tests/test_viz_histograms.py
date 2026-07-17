"""Smoke tests for representation-count distribution and growth plots."""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")

from taxicab.viz.histograms import (
    plot_count_distribution,
    plot_cumulative_growth,
    plot_distribution_and_growth,
)
from taxicab.viz.style import use_publication_style


def _toy_df() -> pd.DataFrame:
    # 3 singletons + 1 taxicab-2 (1729) + 1 imagined 3-rep (99999)
    rows = [
        (10, 1, 2),
        (20, 1, 3),
        (30, 2, 3),
        (1729, 1, 12),
        (1729, 9, 10),
        (99999, 1, 2),  # placeholder — not real, just for shape
        (99999, 3, 4),
        (99999, 5, 6),
    ]
    return pd.DataFrame(rows, columns=["N", "a", "b"]).astype({"N": "int64", "a": "int32", "b": "int32"})


def test_count_distribution_renders() -> None:
    use_publication_style()
    fig, ax = plt.subplots()
    plot_count_distribution(ax, _toy_df())
    assert len(ax.patches) == 3  # 3 bars for k=1, 2, 3
    plt.close(fig)


def test_cumulative_growth_renders() -> None:
    use_publication_style()
    fig, ax = plt.subplots()
    plot_cumulative_growth(ax, _toy_df(), thresholds=(1, 2), n_max=100000)
    # 2 data lines + 1 reference slope = 3 lines
    assert len(ax.lines) == 3
    plt.close(fig)


def test_two_panel_figure_renders() -> None:
    use_publication_style()
    fig = plot_distribution_and_growth(_toy_df(), n_max=100000)
    assert len(fig.axes) == 2
    plt.close(fig)
