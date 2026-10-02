#!/usr/bin/env python3
"""Reproduce author-original figure crops from pinned paper PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

import pymupdf
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data" / "frameworks.json"
DEFAULT_CACHE = ROOT / ".figure-work" / "pdfs"
ALLOWED_KINDS = {"framework", "architecture", "pipeline", "overview", "taxonomy", "benchmark", "dataset"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Awesome-AG-ReID figure curator/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response, target.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)


def render(record: dict, cache_dir: Path, dpi: int, force_download: bool) -> Path:
    figure = record["figure"]
    if figure["figure_kind"] not in ALLOWED_KINDS:
        raise ValueError(f"invalid figure_kind for {record['paper_id']}")

    pdf_path = cache_dir / f"{record['paper_id']}.pdf"
    if force_download or not pdf_path.exists():
        fetch(figure["source_pdf_url"], pdf_path)
    actual_hash = sha256(pdf_path)
    if actual_hash != figure["source_pdf_sha256"]:
        raise ValueError(f"PDF hash mismatch for {record['paper_id']}: {actual_hash}")

    document = pymupdf.open(pdf_path)
    page_index = int(figure["page"]) - 1
    if not 0 <= page_index < document.page_count:
        raise ValueError(f"page out of range for {record['paper_id']}")
    x0, y0, x1, y1 = map(float, figure["crop_pt"])
    clip = pymupdf.Rect(x0, y0, x1, y1)
    if clip.is_empty or not document[page_index].rect.contains(clip):
        raise ValueError(f"invalid crop for {record['paper_id']}: {clip}")

    scale = dpi / 72.0
    pixmap = document[page_index].get_pixmap(matrix=pymupdf.Matrix(scale, scale), clip=clip, alpha=False)
    output_path = ROOT / figure["path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pixmap.save(output_path)
    document.close()

    with Image.open(output_path) as image:
        if max(image.size) > 2400:
            image.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
            image.save(output_path, format="PNG", optimize=True)
        elif output_path.stat().st_size > 5 * 1024 * 1024:
            image.save(output_path, format="PNG", optimize=True)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paper_ids", nargs="*", help="Only regenerate these paper IDs")
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--dpi", type=int, default=220)
    parser.add_argument("--force-download", action="store_true")
    args = parser.parse_args()
    records = json.loads(args.metadata.read_text(encoding="utf-8"))
    selected = set(args.paper_ids)
    unknown = selected - {record["paper_id"] for record in records}
    if unknown:
        parser.error(f"unknown paper IDs: {', '.join(sorted(unknown))}")
    for record in records:
        if selected and record["paper_id"] not in selected:
            continue
        print(render(record, args.cache_dir, args.dpi, args.force_download).relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
