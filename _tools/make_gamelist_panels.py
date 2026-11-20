#!/usr/bin/env python3
"""Generate the game list panel images for every supported number of rows.

The game list panel ("gamelist-panel-<scheme>.png") has the row separators baked in. They match a
text list of 15 rows, so the number of rows cannot change without redrawing them. This script takes
that panel as the master image, erases its separators and draws new ones for each supported number
of rows, in both the default layout and the swapped one ("Game List Position" set to "Left"):

  - _inc/other/gamelist-rows/<rows>/gamelist-panel-<scheme>.png       (list on the right)
  - _inc/other/gamelist-rows/<rows>/gamelist-panel-<scheme>-left.png  (shifted -960 px)

The separators are placed on the row boundaries of the "gamelist" text list (see
"gamelist-textlist.xml"): it starts at y = 0.09 and is 0.7519 high, relative to the screen height.

Run it again whenever the master panels change, or when a value is added to GAMELIST_ROWS (which
must be kept in sync with the "gamelist-rows" subset in "theme-config.xml").
"""
from pathlib import Path

from PIL import Image

OTHER = Path(__file__).parent.parent / "_inc" / "other"
OUTPUT = OTHER / "gamelist-rows"
WIDTH, HEIGHT = 1920, 1080
SCHEMES = ("dark", "light")
# Odd numbers only: the text list centers the selected row, so even numbers would show half rows.
GAMELIST_ROWS = (7, 9, 11, 13, 15, 17, 19, 21)

# Geometry of the "gamelist" text list, in pixels of the 1920x1080 panel.
LIST_TOP = 0.09 * HEIGHT
LIST_HEIGHT = 0.7519 * HEIGHT
# Horizontal extent and thickness of the separators drawn in the master panel.
SEPARATOR_LEFT, SEPARATOR_RIGHT = 1104, 1799
SEPARATOR_THICKNESS = 2
# Column used to find the separators of the master panel, and range of rows where they are.
PROBE_X = SEPARATOR_LEFT
PROBE_TOP, PROBE_BOTTOM = int(LIST_TOP) + 5, int(LIST_TOP + LIST_HEIGHT) + 5


def find_separator_rows(img: Image.Image) -> tuple[list[int], tuple, tuple]:
    """Return the rows covered by separators, the panel color and the separator color."""
    background = img.getpixel((PROBE_X, PROBE_TOP))
    rows = [y for y in range(PROBE_TOP, PROBE_BOTTOM) if img.getpixel((PROBE_X, y)) != background]
    if not rows:
        raise ValueError("no separator found in the master panel")
    return rows, background, img.getpixel((PROBE_X, rows[0]))


def fill_rows(img: Image.Image, rows: list[int], color: tuple) -> None:
    """Paint the given rows of the separators area with a solid color."""
    for y in rows:
        img.paste(color, (SEPARATOR_LEFT, y, SEPARATOR_RIGHT, y + 1))


def separator_rows(rows_count: int) -> list[int]:
    """Return the pixel rows of the separators between the rows of the list."""
    row_height = LIST_HEIGHT / rows_count
    rows = []
    for index in range(1, rows_count):
        top = round(LIST_TOP + index * row_height)
        rows.extend(range(top, top + SEPARATOR_THICKNESS))
    return rows


def shift_left(img: Image.Image) -> Image.Image:
    """Move the panel to the left half of the screen."""
    dx = WIDTH // 2
    if img.crop((0, 0, dx, HEIGHT)).getchannel("A").getbbox() is not None:
        raise ValueError("panel content would be cut off by the shift")
    out = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    out.paste(img, (-dx, 0))
    return out


def main() -> None:
    """Generate the panels of every color scheme and number of rows."""
    for scheme in SCHEMES:
        master = Image.open(OTHER / f"gamelist-panel-{scheme}.png").convert("RGBA")
        old_rows, background, separator = find_separator_rows(master)
        blank = master.copy()
        fill_rows(blank, old_rows, background)
        for rows_count in GAMELIST_ROWS:
            panel = blank.copy()
            fill_rows(panel, separator_rows(rows_count), separator)
            folder = OUTPUT / str(rows_count)
            folder.mkdir(parents=True, exist_ok=True)
            panel.save(folder / f"gamelist-panel-{scheme}.png", optimize=True)
            shift_left(panel).save(folder / f"gamelist-panel-{scheme}-left.png", optimize=True)


if __name__ == "__main__":
    main()
