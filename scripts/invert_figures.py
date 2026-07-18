"""Invert light-mode SVG figures into dark-mode versions.

Reads every .svg in figures/, swaps light/dark colors, injects an explicit
white-text rule (matplotlib emits text without a fill attribute, so it
inherits SVG's default black), writes to figures_dark/.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "figures"
DST_DIR = REPO_ROOT / "figures_dark"

COLOR_MAP: dict[str, str] = {
    "#ffffff": "#000000",
    "#fafaf7": "#000000",
    "#000000": "#ffffff",
    "#aaaaaa": "#555555",
    "#555555": "#aaaaaa",
    "#8b0000": "#d96a6a",
    "#00008b": "#7a9ed8",
    "white": "black",
    "black": "white",
}

TEXT_STYLE_RULE = '<style type="text/css">text { fill: #ffffff; }</style>\n'


def invert_svg_text(text: str) -> str:
    """Color-swap with sentinels to prevent double-substitution."""
    sentinels = {src: f"__COLOR_SENTINEL_{i}__" for i, src in enumerate(COLOR_MAP)}
    for src, sentinel in sentinels.items():
        pattern = re.compile(re.escape(src), re.IGNORECASE)
        text = pattern.sub(sentinel, text)
    for src, dst in COLOR_MAP.items():
        text = text.replace(sentinels[src], dst)
    return text


def inject_text_color(svg: str) -> str:
    """Insert a CSS rule forcing all <text> elements to render white.

    Matplotlib SVGs let text inherit color, and SVG's default is black.
    After the color swap the background becomes black too, so text disappears.
    Injecting a global CSS rule is the least invasive fix.
    """
    # Prefer inserting inside <defs>...</defs> since it always exists in
    # matplotlib output. Fall back to right after the opening <svg ...>.
    if "</defs>" in svg:
        return svg.replace("</defs>", TEXT_STYLE_RULE + "</defs>", 1)
    return re.sub(r"(<svg[^>]*>)", r"\1\n" + TEXT_STYLE_RULE, svg, count=1)


def main() -> None:
    if not SRC_DIR.exists():
        raise SystemExit(f"Source directory not found: {SRC_DIR}")
    DST_DIR.mkdir(parents=True, exist_ok=True)

    svgs = sorted(SRC_DIR.glob("*.svg"))
    if not svgs:
        raise SystemExit(f"No SVGs found in {SRC_DIR}")

    for src_path in svgs:
        dst_path = DST_DIR / src_path.name
        text = src_path.read_text(encoding="utf-8")
        inverted = inject_text_color(invert_svg_text(text))
        dst_path.write_text(inverted, encoding="utf-8")
        print(f"{src_path.name} -> {dst_path}")

    print(f"\nWrote {len(svgs)} inverted figure(s) to {DST_DIR}")


if __name__ == "__main__":
    main()
