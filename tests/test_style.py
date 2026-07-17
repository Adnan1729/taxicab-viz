"""Smoke test for viz.style — confirms the style applies without error."""

import matplotlib as mpl

from taxicab.viz.style import PALETTE, use_publication_style


def test_style_applies() -> None:
    use_publication_style()
    assert mpl.rcParams["figure.facecolor"] == PALETTE.background
    assert mpl.rcParams["svg.fonttype"] == "none"


def test_palette_has_valid_hex_colors() -> None:
    for color in [
        PALETTE.primary,
        PALETTE.secondary,
        PALETTE.tertiary,
        PALETTE.accent,
        PALETTE.background,
        PALETTE.text,
        PALETTE.muted_text,
    ]:
        assert color.startswith("#")
        assert len(color) == 7
        int(color[1:], 16)  # valid hex, raises if not
