"""Publication style: fonts, colors, sizes.

Import `use_publication_style()` at the top of any plotting module or script
to apply the styling globally. All figures should look consistent afterwards.
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Palette:
    """Minimalist monochromatic palette anchored on #003840.

    Use `primary` for the main data, `secondary`/`tertiary` for supporting
    elements, `accent` sparingly for highlighting. All chosen for legibility
    on `background` with `text` at any weight.
    """

    primary: str = "#003840"       # deep teal — main data
    secondary: str = "#3A6B72"     # lighter tint — secondary data
    tertiary: str = "#8AA9AC"      # lightest tint — gridlines, subtle
    accent: str = "#8B3A1F"        # muted burnt sienna — for highlights only
    background: str = "#FAFAF7"    # warm off-white
    text: str = "#1A1A1A"          # near-black
    muted_text: str = "#5A5A5A"    # for captions, annotations


PALETTE = Palette()


def use_publication_style() -> None:
    """Apply the project-wide matplotlib style.

    Call once at the top of any script or notebook that produces figures.
    Idempotent — safe to call multiple times.
    """
    mpl.rcParams.update(
        {
            # Fonts
            "font.family": "sans-serif",
            "font.sans-serif": ["Inter", "Helvetica", "Arial", "DejaVu Sans"],
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "figure.titlesize": 13,
            # Math text — match the sans-serif look
            "mathtext.fontset": "dejavusans",
            # Colors
            "figure.facecolor": PALETTE.background,
            "axes.facecolor": PALETTE.background,
            "savefig.facecolor": PALETTE.background,
            "text.color": PALETTE.text,
            "axes.labelcolor": PALETTE.text,
            "axes.edgecolor": PALETTE.text,
            "xtick.color": PALETTE.text,
            "ytick.color": PALETTE.text,
            # Axes — minimalist: no top/right spines, thin edges
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "grid.color": PALETTE.tertiary,
            "grid.linewidth": 0.4,
            "grid.alpha": 0.5,
            # Ticks
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 3,
            "ytick.major.size": 3,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            # Lines & markers
            "lines.linewidth": 1.4,
            "lines.markersize": 5,
            "patch.linewidth": 0.6,
            # Figure & layout
            "figure.dpi": 120,        # on-screen preview
            "savefig.dpi": 300,       # embedded raster fallback (rare for SVG)
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            # SVG — keep text as text, not paths (editable in Inkscape/Illustrator)
            "svg.fonttype": "none",
        }
    )


def savefig(fig: plt.Figure, path: str, **kwargs: object) -> None:
    """Save a figure as SVG with project defaults.

    Wrapper over `fig.savefig` to enforce SVG output and keep call sites clean.
    """
    if not str(path).endswith(".svg"):
        raise ValueError(f"Publication figures must be SVG; got {path}")
    fig.savefig(path, format="svg", **kwargs)
