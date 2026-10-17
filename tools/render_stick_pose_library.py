#!/usr/bin/env python3
"""Render editable, hand-authored 2D stick-pose guides from joint coordinates."""

import argparse
import hashlib
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


DEFAULT = Path(__file__).resolve().parents[1] / "devdocs/art/pose_library/v1"
COLORS = {"near": "#183b56", "far": "#7195a6", "spine": "#237e88", "hips": "#bd783c"}


def primitives(pose):
    joints = pose["joints"]
    items = []
    for side in ("far", "near"):
        for chain in ((f"shoulder_{side}", f"elbow_{side}", f"wrist_{side}"),
                      (f"hip_{side}", f"knee_{side}", f"ankle_{side}", f"heel_{side}", f"toe_{side}")):
            for start, end in zip(chain, chain[1:]):
                items.append(("line", joints[start], joints[end], COLORS[side], side == "far"))
    neck, pelvis = joints["neck"], joints["pelvis"]
    middle = pose.get("spine_mid", [(neck[0] + pelvis[0]) / 2, (neck[1] + pelvis[1]) / 2])
    for start, end in ((neck, middle), (middle, pelvis),
                       (joints["shoulder_far"], joints["shoulder_near"])):
        items.append(("line", start, end, COLORS["spine"], False))
    for side in ("far", "near"):
        items.append(("line", pelvis, joints[f"hip_{side}"], COLORS["hips"], False))
        items.append(("line", neck, joints[f"shoulder_{side}"], COLORS["spine"], False))
    head = joints["head"]
    vx, vy = head[0] - neck[0], head[1] - neck[1]
    length = math.hypot(vx, vy)
    vx, vy = vx / length, vy / length
    ux, uy = -vy, vx
    outline = [[head[0] + ux * 31 * math.cos(t) + vx * 42 * math.sin(t),
                head[1] + uy * 31 * math.cos(t) + vy * 42 * math.sin(t)]
               for t in [index * 2 * math.pi / 72 for index in range(73)]]
    items.append(("polyline", outline, None, COLORS["near"], False))
    items.append(("line", neck, [head[0] - vx * 38, head[1] - vy * 38], COLORS["near"], False))
    look = pose["look_direction"]
    look_length = math.hypot(*look)
    nose = [head[0] + look[0] * 25 / look_length, head[1] + look[1] * 25 / look_length]
    items.append(("line", head, nose, COLORS["hips"], False))
    for name, point in joints.items():
        if name not in ("head", "neck") and not name.startswith(("toe_", "heel_")):
            items.append(("joint", point, 5 if name.endswith("_far") else 7,
                          COLORS["far"] if name.endswith("_far") else COLORS["near"], False))
    return items


def dashed(start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    for offset in range(0, math.ceil(length), 20):
        finish = min(offset + 12, length)
        yield ([start[0] + dx * offset / length, start[1] + dy * offset / length],
               [start[0] + dx * finish / length, start[1] + dy * finish / length])


def render(pose, destination, size):
    scale = 3
    image = Image.new("RGBA", (size[0] * scale, size[1] * scale))
    draw = ImageDraw.Draw(image)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 {size[0]} {size[1]}">',
           f'<title>{escape(pose["title"])}</title>', '<g fill="none" stroke-linecap="round" stroke-linejoin="round">']
    for kind, a, b, color, is_far in primitives(pose):
        if kind == "line":
            for start, end in dashed(a, b) if is_far else [(a, b)]:
                draw.line([(round(x * scale), round(y * scale)) for x, y in (start, end)], fill=color, width=5 * scale)
            dash = ' stroke-dasharray="12 8"' if is_far else ''
            svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{color}" stroke-width="5"{dash}/>')
        elif kind == "joint":
            x, y = a
            draw.ellipse(((x - b) * scale, (y - b) * scale, (x + b) * scale, (y + b) * scale), fill=color)
            svg.append(f'<circle cx="{x}" cy="{y}" r="{b}" fill="{color}"/>')
        else:
            draw.line([(round(x * scale), round(y * scale)) for x, y in a], fill=color, width=4 * scale, joint="curve")
            points = " ".join(f"{x:.2f},{y:.2f}" for x, y in a)
            svg.append(f'<polyline points="{points}" stroke="{color}" stroke-width="4"/>')
    svg.append('</g></svg>')
    png = destination / "png" / f'{pose["id"]}.png'
    svg_path = destination / "svg" / f'{pose["id"]}.svg'
    image = image.resize(tuple(size), Image.Resampling.LANCZOS)
    image.save(png, optimize=True)
    svg_path.write_text("\n".join(svg) + "\n", encoding="utf-8")
    return image, {"id": pose["id"], "npc": pose["suggested_npc"], "png": str(png.relative_to(destination)),
                   "svg": str(svg_path.relative_to(destination)),
                   "png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
                   "svg_sha256": hashlib.sha256(svg_path.read_bytes()).hexdigest()}


def main(library):
    data = json.loads((library / "poses.json").read_text(encoding="utf-8"))
    for name in ("png", "svg"):
        (library / name).mkdir(parents=True, exist_ok=True)
    entries = []
    cell_w, cell_h = 300, 375
    sheet = Image.new("RGB", (1200, 1430), "#f4f2ed")
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.load_default(size=28)
    body_font = ImageFont.load_default(size=15)
    small_font = ImageFont.load_default(size=13)
    draw.text((24, 17), "NPC stick-pose library / 16 joint guides", font=title_font, fill="#183b56")
    draw.text((24, 57), "Solid: near limbs   Dashed: far limbs   Orange head line: facing direction", font=body_font, fill="#435a66")
    for index, pose in enumerate(data["poses"]):
        im, entry = render(pose, library, data["canvas"])
        entries.append(entry)
        x, y = index % 4 * cell_w, 80 + index // 4 * cell_h
        height = 220 if index >= 12 else cell_h
        draw.rounded_rectangle((x + 8, y + 6, x + 292, y + height - 8), radius=12, fill="#ffffff", outline="#d8dfe1")
        draw.text((x + 20, y + 15), pose["suggested_npc"].capitalize(), font=body_font, fill="#183b56")
        draw.text((x + 20, y + 37), pose["title"], font=small_font, fill="#435a66")
        thumb = im.crop(im.getbbox())
        thumb.thumbnail((250, height - 90), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x + (cell_w - thumb.width) // 2, y + 64 + (height - 90 - thumb.height) // 2), thumb)
    sheet.save(library / "pose_library_preview.jpg", quality=94)
    (library / "manifest.json").write_text(json.dumps({"canvas": data["canvas"], "count": len(entries), "poses": entries}, indent=2) + "\n")
    print(json.dumps({"poses": len(entries), "library": str(library)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, default=DEFAULT)
    main(parser.parse_args().library.resolve())
