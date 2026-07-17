"""Tests for taxicab.viz.curves — smoke tests that plots render without error."""

import matplotlib
import matplotlib.pyplot as plt

# Use the non-interactive Agg backend so tests don't try to open windows.
matplotlib.use("Agg")

from taxicab.viz.curves import plot_curve_with_points, plot_taxicab_grid
from taxicab.viz.style import use_publication_style


def test_single_panel_renders() -> None:
    use_publication_style()
    fig, ax = plt.subplots()
    plot_curve_with_points(ax, 1729, [(1, 12), (9, 10)])
    # If it drew, there should be lines and scatter collections.
    assert len(ax.lines) >= 1
    assert len(ax.collections) >= 2  # halo + accent scatters
    plt.close(fig)


def test_grid_layout() -> None:
    use_publication_style()
    entries = [
        (1729, [(1, 12), (9, 10)]),
        (4104, [(2, 16), (9, 15)]),
    ]
    fig = plot_taxicab_grid(entries, ncols=2)
    axes = fig.axes
    assert len(axes) == 2
    plt.close(fig)


def test_grid_hides_unused_panels() -> None:
    use_publication_style()
    entries = [(1729, [(1, 12), (9, 10)])]  # one entry, 2x1 grid means 1 unused
    fig = plot_taxicab_grid(entries, ncols=2)
    # The unused panel should have its axis turned off.
    visible = [ax for ax in fig.axes if ax.axison]
    assert len(visible) == 1
    plt.close(fig)
