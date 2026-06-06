#!/usr/bin/env python3
"""Compare two web-ui-copy style snapshots.

The snapshots should be JSON objects produced by scripts/style_snapshot.js.
The report highlights font/style/geometry mismatches for clone debugging.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_TOLERANCE = 1.0
IMPORTANT_STYLE_KEYS = [
    "fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "color",
    "backgroundColor", "backgroundImage", "borderTopColor", "borderTopWidth",
    "borderTopStyle", "borderRadius", "boxShadow", "paddingTop", "paddingRight",
    "paddingBottom", "paddingLeft", "display", "gap", "gridTemplateColumns",
    "justifyContent", "alignItems", "textAlign",
]


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rect_delta(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    return {key: round(float(b.get(key, 0)) - float(a.get(key, 0)), 3) for key in ("x", "y", "w", "h")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Original page style snapshot JSON")
    parser.add_argument("--copy", required=True, help="Copied page style snapshot JSON")
    parser.add_argument("--out", help="Optional report JSON path")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE, help="Geometry tolerance in px")
    parser.add_argument("--ignore-text", action="store_true", help="Do not report text differences")
    args = parser.parse_args()

    source = load(args.source)
    copy = load(args.copy)
    source_targets = source.get("targets", [])
    copy_targets = copy.get("targets", [])
    by_key = {(item.get("selector"), item.get("index", 0)): item for item in copy_targets}

    checks = []
    for src in source_targets:
        key = (src.get("selector"), src.get("index", 0))
        dst = by_key.get(key)
        item: dict[str, Any] = {"selector": key[0], "index": key[1], "status": "ok", "differences": []}
        if not src.get("found"):
            item["status"] = "source-missing"
        elif not dst or not dst.get("found"):
            item["status"] = "copy-missing"
        else:
            if not args.ignore_text and src.get("text") != dst.get("text"):
                item["differences"].append({"type": "text", "source": src.get("text"), "copy": dst.get("text")})
            for style_key in IMPORTANT_STYLE_KEYS:
                a = src.get("style", {}).get(style_key)
                b = dst.get("style", {}).get(style_key)
                if a != b:
                    item["differences"].append({"type": "style", "property": style_key, "source": a, "copy": b})
            delta = rect_delta(src.get("rect", {}), dst.get("rect", {}))
            if any(abs(v) > args.tolerance for v in delta.values()):
                item["differences"].append({"type": "rect", "delta": delta, "source": src.get("rect"), "copy": dst.get("rect")})
            if item["differences"]:
                item["status"] = "diff"
        checks.append(item)

    report = {
        "sourceUrl": source.get("url"),
        "copyUrl": copy.get("url"),
        "sourceViewport": source.get("viewport"),
        "copyViewport": copy.get("viewport"),
        "total": len(checks),
        "diffCount": sum(1 for item in checks if item["status"] != "ok"),
        "checks": checks,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
