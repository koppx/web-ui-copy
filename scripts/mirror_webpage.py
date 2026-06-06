#!/usr/bin/env python3
"""Mirror a webpage shell and visual assets for high-fidelity UI cloning.

This script captures server-rendered HTML, downloads same-origin visual assets,
recurses CSS url(...) and JS static imports, removes common non-visual analytics
scripts when requested, and writes a manifest for debugging.

Examples:
  python scripts/mirror_webpage.py --url https://example.com --out clone-capture
  python scripts/mirror_webpage.py --url https://example.com --out clone-capture --keep-analytics
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import deque
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse, urldefrag, unquote
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
ASSET_EXTENSIONS = {
    ".css", ".js", ".mjs", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".avif",
    ".mp4", ".mov", ".webm", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".ico", ".json",
    ".map", ".xml", ".webmanifest",
}
ANALYTICS_PATTERNS = [
    r"/analytics?[/.-]", r"/metrics/", r"googletagmanager", r"google-analytics",
    r"doubleclick", r"facebook\.net", r"hotjar", r"segment\.com", r"amplitude",
]


def request_text(url: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as res:
        charset = res.headers.get_content_charset() or "utf-8"
        return res.read().decode(charset, errors="replace")


def download(url: str, target: Path, timeout: int) -> tuple[bool, str | None]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return True, None
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as res:
            target.write_bytes(res.read())
        return True, None
    except Exception as exc:  # noqa: BLE001 - report and continue mirroring what is available
        try:
            target.unlink(missing_ok=True)
        except Exception:
            pass
        return False, str(exc)


def normalize_url(base: str, value: str) -> str | None:
    if not value:
        return None
    value = unescape(value.strip().strip('"\''))
    if not value or value.startswith(("data:", "javascript:", "mailto:", "tel:", "#")):
        return None
    full = urljoin(base, value)
    full, _frag = urldefrag(full)
    parsed = urlparse(full)
    if parsed.scheme not in {"http", "https"}:
        return None
    return full


def is_likely_asset(url: str) -> bool:
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix.lower()
    return (
        ext in ASSET_EXTENSIONS
        or "/assets/" in parsed.path
        or "/static/" in parsed.path
        or "/images/" in parsed.path
        or "/img/" in parsed.path
        or "/fonts/" in parsed.path
        or "/scripts/" in parsed.path
        or "/styles/" in parsed.path
    )


def local_path(out_site: Path, url: str, root_netloc: str) -> Path:
    parsed = urlparse(url)
    path = unquote(parsed.path).lstrip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    # Same-origin keeps original root paths. Cross-origin assets are namespaced.
    if parsed.netloc != root_netloc:
        path = f"__external__/{parsed.netloc}/{path}"
    # Static servers cannot serve query-string filenames. Add a stable suffix for queried assets.
    if parsed.query:
        safe_query = re.sub(r"[^A-Za-z0-9._-]+", "_", parsed.query).strip("_")[:80]
        p = Path(path)
        path = str(p.with_name(f"{p.stem}__q_{safe_query}{p.suffix or '.asset'}"))
    return out_site / path


def extract_html_urls(html: str, base: str) -> Iterable[str]:
    attr_re = re.compile(r"""\b(?:href|src|poster|data-src|data-href|imagesrcset)=['\"]([^'\"]+)['\"]""", re.I)
    for match in attr_re.finditer(html):
        value = match.group(1)
        if "," in value and ("srcset" in match.group(0).lower() or "imagesrcset" in match.group(0).lower()):
            for part in value.split(","):
                maybe = normalize_url(base, part.strip().split()[0] if part.strip() else "")
                if maybe:
                    yield maybe
        else:
            maybe = normalize_url(base, value)
            if maybe:
                yield maybe
    for srcset in re.findall(r"""\b(?:srcset|imagesrcset)=['\"]([^'\"]+)['\"]""", html, re.I):
        for part in srcset.split(","):
            maybe = normalize_url(base, part.strip().split()[0] if part.strip() else "")
            if maybe:
                yield maybe
    yield from extract_css_urls(html, base)


def extract_css_urls(css: str, base: str) -> Iterable[str]:
    for raw in re.findall(r"url\(([^)]+)\)", css, re.I):
        maybe = normalize_url(base, raw)
        if maybe:
            yield maybe
    for raw in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css, re.I):
        maybe = normalize_url(base, raw)
        if maybe:
            yield maybe


def extract_js_urls(js: str, base: str) -> Iterable[str]:
    patterns = [
        r"\bfrom\s*['\"]([^'\"]+)['\"]",
        r"\bimport\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        r"new\s+URL\s*\(\s*['\"]([^'\"]+)['\"]",
    ]
    for pattern in patterns:
        for raw in re.findall(pattern, js):
            maybe = normalize_url(base, raw)
            if maybe:
                yield maybe


def remove_analytics(html: str) -> str:
    def strip_if_analytics(match: re.Match[str]) -> str:
        tag = match.group(0)
        lowered = tag.lower()
        return "" if any(re.search(p, lowered) for p in ANALYTICS_PATTERNS) else tag

    return re.sub(r"<script\b[^>]*\bsrc=['\"][^'\"]+['\"][^>]*>\s*</script>", strip_if_analytics, html, flags=re.I)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Source page URL")
    parser.add_argument("--out", required=True, help="Output capture directory")
    parser.add_argument("--max-assets", type=int, default=600, help="Safety cap for downloaded assets")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--include-cross-origin", action="store_true", help="Also mirror cross-origin assets")
    parser.add_argument("--keep-analytics", action="store_true", help="Do not strip common analytics scripts from index.html")
    args = parser.parse_args()

    source_url = args.url
    source_parsed = urlparse(source_url)
    if source_parsed.scheme not in {"http", "https"}:
        raise SystemExit("--url must be http(s)")

    out = Path(args.out)
    source_dir = out / "source-capture"
    site_dir = out / "site"
    source_dir.mkdir(parents=True, exist_ok=True)
    site_dir.mkdir(parents=True, exist_ok=True)

    print(f"GET HTML {source_url}")
    html = request_text(source_url, args.timeout)
    (source_dir / "source.html").write_text(html, encoding="utf-8")
    (site_dir / "index.html").write_text(html if args.keep_analytics else remove_analytics(html), encoding="utf-8")

    queue: deque[str] = deque()
    seen: set[str] = set()
    failures: dict[str, str] = {}
    downloaded: dict[str, str] = {}

    def enqueue(url: str) -> None:
        parsed = urlparse(url)
        if not args.include_cross_origin and parsed.netloc != source_parsed.netloc:
            return
        if not is_likely_asset(url):
            return
        if url not in seen:
            seen.add(url)
            queue.append(url)

    for url in extract_html_urls(html, source_url):
        enqueue(url)

    while queue and len(downloaded) < args.max_assets:
        url = queue.popleft()
        target = local_path(site_dir, url, source_parsed.netloc)
        ok, error = download(url, target, args.timeout)
        rel = str(target.relative_to(site_dir)).replace(os.sep, "/")
        if ok:
            downloaded[url] = rel
            suffix = target.suffix.lower()
            if suffix in {".css", ".js", ".mjs"}:
                try:
                    text = target.read_text(errors="ignore")
                except Exception:
                    continue
                base = urljoin(url, ".")
                next_urls = extract_css_urls(text, base) if suffix == ".css" else extract_js_urls(text, base)
                for next_url in next_urls:
                    enqueue(next_url)
        else:
            failures[url] = error or "download failed"

    manifest = {
        "source": source_url,
        "site": str(site_dir),
        "index": str(site_dir / "index.html"),
        "downloadedCount": len(downloaded),
        "failureCount": len(failures),
        "downloaded": downloaded,
        "failures": failures,
        "notes": [
            "Serve the site directory as web root, for example: python3 -m http.server 8080 -d site",
            "Some dynamic API endpoints, service workers, query-string routes, or JS-constructed media URLs may require manual capture.",
        ],
    }
    (out / "mirror-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"downloadedCount": len(downloaded), "failureCount": len(failures), "out": str(out)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
