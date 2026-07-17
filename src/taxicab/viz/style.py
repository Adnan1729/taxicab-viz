"""Publication style: classical scientific / mathematics journal aesthetic.

Modeled after AMS / LMS / Cambridge conventions: serif math typography,
black on white, distinctions by linestyle rather than color.
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Palette:
    """Restrained scientific palette.

    The default is monochrome. `accent_1` and `accent_2` are used sparingly
    for reference lines or when linestyle alone can't disambiguate.
    """

    primary: str = "#000000"        # black — main data
    secondary: str = "#555555"      # dark grey — secondary data
    tertiary: str = "#AAAAAA"       # light grey — gridlines, backdrops
    accent_1: str = "#8B0000"       # dark red — reference lines, sparingly
    accent_2: str = "#00008B"       # dark blue — when a second accent is needed
    background: str = "#FFFFFF"     # pure white
    text: str = "#000000"           # black


PALETTE = Palette()


def use_publication_style() -> None:
    """Apply the classical scientific style. Idempotent."""
    mpl.rcParams.update(
        {
            # Typography — serif, math-friendly
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman", "STIX", "DejaVu Serif"],
            "mathtext.fontset": "cm",  # Computer Modern for math
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "figure.titlesize": 12,
            # Colors — black on white, no exceptions
            "figure.facecolor": PALETTE.background,
            "axes.facecolor": PALETTE.background,
            "savefig.facecolor": PALETTE.background,
            "text.color": PALETTE.text,
            "axes.labelcolor": PALETTE.text,
            "axes.edgecolor": PALETTE.text,
            "xtick.color": PALETTE.text,
            "ytick.color": PALETTE.text,
            # Axes — thin, full frame (all four spines), no top-right removal
            "axes.spines.top": True,
            "axes.spines.right": True,
            "axes.linewidth": 0.6,
            "axes.grid": True,
            "grid.color": PALETTE.tertiary,
            "grid.linewidth": 0.3,
            "grid.linestyle": ":",
            "grid.alpha": 0.7,
            # Ticks — inward, small, both major and minor
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 3,
            "ytick.major.size": 3,
            "xtick.minor.size": 1.5,
            "ytick.minor.size": 1.5,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.minor.visible": True,
            "ytick.minor.visible": True,
            "xtick.top": True,      # ticks on all four sides
            "ytick.right": True,
            # Lines & markers — thin, precise
            "lines.linewidth": 0.9,
            "lines.markersize": 4,
            "patch.linewidth": 0.5,
            "patch.edgecolor": PALETTE.text,
            "patch.facecolor": PALETTE.background,  # unfilled bars by default
            # Legend — no frame, minimalist
            "legend.frameon": False,
            "legend.borderpad": 0.4,
            # Figure & layout
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            # SVG — editable text
            "svg.fonttype": "none",
        }
    )


def savefig(fig: plt.Figure, path: str, **kwargs: object) -> None:
    """Save as SVG with project defaults."""
    if not str(path).endswith(".svg"):
        raise ValueError(f"Publication figures must be SVG; got {path}")
    fig.savefig(path, format="svg", **kwargs)
