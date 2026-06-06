#!/usr/bin/env python3
"""Create a layout blueprint from a reference screenshot.

This records manually supplied section/region boxes as pixels and percentages.
It is intentionally explicit: the agent/user marks important regions instead of
pretending computer vision can infer design intent reliably.

Example:
  python scripts/extract_layout_blueprint.py --src reference.png --out blueprint.json \
    --viewport-width 1440 --section hero:0,80,1440,820 --region heroTitle:120,180,760,290
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required for screenshot blueprints: python -m pip install Pillow") from exc


def parse_named_box(value: str) -> tuple[str, tuple[float, float, float, float], str | None]:
    if ":" not in value:
        raise argparse.ArgumentTypeError("box must be name:x1,y1,x2,y2 or name:x1,y1,x2,y2:fit")
    name, rest = value.split(":", 1)
    fit = None
    if ":" in rest:
        box_part, fit = rest.rsplit(":", 1)
    else:
        box_part = rest
    nums = [float(part.strip()) for part in box_part.split(",")]
    if len(nums) != 4:
        raise argparse.ArgumentTypeError("box must contain x1,y1,x2,y2")
    x1, y1, x2, y2 = nums
    if x2 <= x1 or y2 <= y1:
        raise argparse.ArgumentTypeError("box must have x2>x1 and y2>y1")
    return name.strip(), (x1, y1, x2, y2), fit.strip() if fit else None


def box_record(box: tuple[float, float, float, float], canvas_w: int, canvas_h: int, fit: str | None = None) -> dict[str, object]:
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    record: dict[str, object] = {
        "x": round(x1, 3), "y": round(y1, 3), "w": round(w, 3), "h": round(h, 3),
        "xPct": round(x1 / canvas_w, 6), "yPct": round(y1 / canvas_h, 6),
        "wPct": round(w / canvas_w, 6), "hPct": round(h / canvas_h, 6),
        "aspect": round(w / h, 6),
    }
    if fit:
        record["fit"] = fit
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Reference screenshot/design image")
    parser.add_argument("--out", required=True, help="Output blueprint JSON")
    parser.add_argument("--viewport-width", type=float, help="Target browser viewport width")
    parser.add_argument("--section", action="append", default=[], type=parse_named_box, help="name:x1,y1,x2,y2")
    parser.add_argument("--region", action="append", default=[], type=parse_named_box, help="name:x1,y1,x2,y2 or name:x1,y1,x2,y2:contain")
    args = parser.parse_args()

    src = Path(args.src)
    with Image.open(src) as img:
        canvas_w, canvas_h = img.size
    scale = args.viewport_width / canvas_w if args.viewport_width else None

    sections = []
    for name, box, fit in args.section:
        rec = box_record(box, canvas_w, canvas_h, fit)
        rec["name"] = name
        sections.append(rec)
    sections.sort(key=lambda item: (item["y"], item["x"]))

    regions = {name: box_record(box, canvas_w, canvas_h, fit) for name, box, fit in args.region}
    blueprint = {
        "sourceReference": str(src),
        "referenceCanvas": {"width": canvas_w, "height": canvas_h},
        "targetViewport": {"width": args.viewport_width} if args.viewport_width else None,
        "scale": round(scale, 6) if scale else None,
        "sections": sections,
        "regions": regions,
        "notes": [
            "Use this as screenshot-only or visual QA guidance, not as a replacement for source mirror mode.",
            "Prefer computed styles and real DOM measurements when a live source page is available.",
        ],
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(blueprint, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(blueprint, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
