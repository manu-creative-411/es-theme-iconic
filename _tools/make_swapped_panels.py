#!/usr/bin/env python3
"""Generate the panel images used when "Game List Position" is set to "Left".

The 1920x1080 panels are drawn for the default layout (info area on the left half, game list on the
right half). To swap the halves, the content is simply shifted by half a screen:

  - game-details-panel-<scheme>.png -> game-details-panel-<scheme>-right.png (shifted +960 px)
  - gamelist-panel-<scheme>.png     -> gamelist-panel-<scheme>-left.png      (shifted -960 px)

The bottom fade of the grid is mirrored instead (soft edge on the side facing the info area):

  - fade-bottom-right-<scheme>.png  -> fade-bottom-left-<scheme>.png

Run it again whenever one of the source panels changes.
"""
from pathlib import Path

from PIL import Image, ImageOps

OTHER = Path(__file__).parent.parent / "_inc" / "other"
WIDTH, HEIGHT = 1920, 1080


def shift(src: Path, dst: Path, dx: int) -> None:
    img = Image.open(src).convert("RGBA")
    lost = img.crop((WIDTH - dx, 0, WIDTH, HEIGHT) if dx > 0 else (0, 0, -dx, HEIGHT))
    if lost.getchannel("A").getbbox() is not None:
        raise ValueError(f"{src.name}: content would be cut off by the shift")
    out = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    out.paste(img, (dx, 0))
    out.save(dst)


for scheme in ("dark", "light"):
    shift(OTHER / f"game-details-panel-{scheme}.png", OTHER / f"game-details-panel-{scheme}-right.png", WIDTH // 2)
    shift(OTHER / f"gamelist-panel-{scheme}.png", OTHER / f"gamelist-panel-{scheme}-left.png", -WIDTH // 2)
    ImageOps.mirror(Image.open(OTHER / f"fade-bottom-right-{scheme}.png").convert("RGBA")).save(
        OTHER / f"fade-bottom-left-{scheme}.png"
    )
