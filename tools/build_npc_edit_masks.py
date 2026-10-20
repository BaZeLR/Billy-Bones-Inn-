#!/usr/bin/env python3
"""Build registered garment-region editing masks; never change source sprites."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "devdocs/art/npc_sprites/v1/card_game/edit_masks/clara/regions.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(spec_path):
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    destination = spec_path.parent
    entries = []
    previews = []
    for pose in spec["poses"]:
        source_path = ROOT / pose["source"]
        source = Image.open(source_path).convert("RGBA")
        if list(source.size) != spec["canvas"]:
            raise ValueError(f"Unexpected source dimensions: {source_path}")
        if digest(source_path) != pose["source_sha256"]:
            raise ValueError(f"Source sprite has changed: {source_path}")
        combined = Image.new("L", source.size)
        # Limit selections to purple fabric; preserve skin, hair and light trim.
        fabric = Image.new("L", source.size)
        pixels = source.tobytes()
        fabric.putdata([
            255 if pixels[index + 2] > pixels[index + 1] + 5 and pixels[index + 3] else 0
            for index in range(0, len(pixels), 4)
        ])
        for name, polygons in pose["regions"].items():
            scale = 4
            large = Image.new("L", (source.width * scale, source.height * scale))
            drawing = ImageDraw.Draw(large)
            for polygon in polygons:
                drawing.polygon([(x * scale, y * scale) for x, y in polygon], fill=255)
            selection = large.resize(source.size, Image.Resampling.LANCZOS)
            # Clip to visible pixels; a mask cannot select outside its source.
            selection = ImageChops.multiply(selection, source.getchannel("A"))
            selection = ImageChops.multiply(selection, fabric)
            selection = selection.point(lambda value: 0 if value < 4 else value)
            if not selection.getbbox():
                raise ValueError(f"Empty selection: {pose['state']}/{name}")
            patch = Image.new("RGBA", source.size, (0, 0, 0, 0))
            patch.putalpha(selection)
            stem = f"clara_cards_{pose['state']}_{name}"
            rgba_path = destination / f"{stem}_black_rgba.png"
            gray_path = destination / f"{stem}_selection.png"
            patch.save(rgba_path, optimize=True)
            selection.save(gray_path, optimize=True)
            combined = ImageChops.lighter(combined, selection)
            entries.append({
                "state": pose["state"], "region": name,
                "source": pose["source"], "source_sha256": pose["source_sha256"],
                "canvas": spec["canvas"], "placement": [0, 0],
                "bounds": list(selection.getbbox()),
                "black_rgba": {"file": rgba_path.name, "sha256": digest(rgba_path)},
                "selection": {"file": gray_path.name, "sha256": digest(gray_path)},
            })

        # The preview uses the actual delivered selection pixels at reduced opacity.
        background = Image.new("RGBA", source.size, (234, 235, 240, 255))
        background.alpha_composite(source)
        tint = Image.new("RGBA", source.size, (12, 185, 225, 0))
        tint.putalpha(combined.point(lambda value: round(value * 0.6)))
        background.alpha_composite(tint)
        previews.append((pose["state"], background))

    manifest = {
        "version": 1, "kind": "editor_garment_selection_masks",
        "canvas": spec["canvas"], "origin": "top-left", "placement": [0, 0],
        "rgba_convention": "Black selected pixels; transparent unselected pixels.",
        "selection_convention": "White selects; black preserves; gray is edge antialiasing.",
        "limitations": "Visible fabric regions only. Hidden anatomy is not inferred.",
        "masks": entries,
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    sheet = Image.new("RGB", (1280, 840), (234, 235, 240))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)
    for index, (name, preview) in enumerate(previews):
        sheet.paste(preview.convert("RGB"), (index * 640, 40))
        draw.text((index * 640 + 24, 12), f"Clarissa / {name} / selected fabric in cyan", font=font, fill=(25, 34, 48))
    sheet.save(destination / "alignment_preview.jpg", quality=92)
    print(json.dumps({"mask_pairs": len(entries), "destination": str(destination)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    build(parser.parse_args().spec)
