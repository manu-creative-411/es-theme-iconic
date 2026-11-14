#!/usr/bin/env python3
"""Generate the bitmap (WebP) logo variants from the vector (SVG) ones.

The bitmap logos follow the very same organization as the vector ones, so the choice of the color
scheme and of the region works identically whether vector logos are enabled or not:

    logos-svg/<system>.svg                      ->  logos/<system>.webp
    logos-svg/<system>-<region>.svg             ->  logos/<system>-<region>.webp
    logos-svg/<system>/<scheme>[-<region>].svg  ->  logos/<system>/<scheme>[-<region>].webp
    logos-svg/<system>/<region>.svg             ->  logos/<system>/<region>.webp

(all paths are relative to the "_inc" folder)

Existing bitmap files are never overwritten unless "--force" is given, so hand-made bitmaps (or the
bitmaps this script already generated and that were then retouched) are preserved.

Requires "rsvg-convert" (librsvg) and Pillow.
"""

import argparse
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

MAX_WIDTH = 540
MAX_HEIGHT = 200


def _render(svg: Path) -> Image.Image:
    """Rasterize an SVG so that it fits in the maximum logo size, keeping its aspect ratio."""
    command = [
        "rsvg-convert",
        "--keep-aspect-ratio",
        "--width",
        str(MAX_WIDTH),
        "--height",
        str(MAX_HEIGHT),
        "--format",
        "png",
        str(svg),
    ]
    result = subprocess.run(command, check=True, capture_output=True)
    return Image.open(io.BytesIO(result.stdout)).convert("RGBA")


def _targets(inc_dir: Path):
    """Yield every (svg, webp) pair to generate."""
    svg_root = inc_dir / "logos-svg"
    webp_root = inc_dir / "logos"
    for svg in sorted(svg_root.rglob("*.svg")):
        yield svg, (webp_root / svg.relative_to(svg_root)).with_suffix(".webp")


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", maxsplit=1)[0])
    parser.add_argument("--force", action="store_true", help="overwrite existing bitmap logos")
    parser.add_argument("--system", help="only process this system (e.g. 'snes')")
    parser.add_argument("--dry-run", action="store_true", help="only list what would be generated")
    args = parser.parse_args()

    inc_dir = Path(__file__).resolve().parent.parent / "_inc"
    generated = skipped = 0

    for svg, webp in _targets(inc_dir):
        system = svg.parent.name if svg.parent.name != "logos-svg" else svg.stem
        if args.system and system != args.system:
            continue
        if not (inc_dir / "metadata" / f"{system}.xml").exists():
            print(f"skipping {svg.relative_to(inc_dir)}: no metadata for system '{system}'")
            continue
        if webp.exists() and not args.force:
            skipped += 1
            continue
        print(f"{svg.relative_to(inc_dir)} -> {webp.relative_to(inc_dir)}")
        generated += 1
        if args.dry_run:
            continue
        webp.parent.mkdir(parents=True, exist_ok=True)
        _render(svg).save(webp, "WEBP", lossless=True, method=6)

    print(f"{generated} generated, {skipped} already existing (kept)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
