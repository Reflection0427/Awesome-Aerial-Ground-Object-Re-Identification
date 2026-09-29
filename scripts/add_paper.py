#!/usr/bin/env python3
"""Insert one human-approved paper into the English and Chinese README tables."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SECTIONS = {
    "image-person": ("Image-based Person AG-ReID", 4),
    "image-vehicle": ("Image-based Vehicle AG-ReID", 4),
    "video-person": ("Video-based Person AG-ReID", 4),
    "challenges": ("Challenges & Workshops", 3),
    "related": ("More Related Exploration", 3),
}


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().replace("|", "\\|")


def resources(args: argparse.Namespace, chinese: bool) -> str:
    labels = {
        "paper_url": "论文" if chinese else "Paper",
        "code_url": "代码" if chinese else "Code",
        "dataset_url": "数据集" if chinese else "Dataset",
        "project_url": "项目" if chinese else "Project",
    }
    links = []
    for field, label in labels.items():
        url = getattr(args, field)
        if url:
            links.append(f"[{label}]({url})")
    return " · ".join(links)


def make_row(args: argparse.Namespace, chinese: bool, columns: int) -> str:
    venue = f"**{clean_cell(args.venue_year)}**"
    title = clean_cell(args.title)
    link_text = resources(args, chinese)
    if columns == 4:
        return f"| {venue} | {clean_cell(args.method or '—')} | {title} | {link_text} |"
    return f"| {venue} | {title} | {link_text} |"


def insert_row(path: Path, section: str, row: str, title: str) -> None:
    text = path.read_text(encoding="utf-8")
    normalized_title = re.sub(r"[^a-z0-9]+", "", title.lower())
    normalized_readme = re.sub(r"[^a-z0-9]+", "", text.lower())
    if normalized_title in normalized_readme:
        raise ValueError(f"{title!r} already appears in {path}")

    heading = f"### {section}"
    start = text.find(heading)
    if start < 0:
        raise ValueError(f"section {heading!r} not found in {path}")
    table_start = text.find("\n|", start)
    if table_start < 0:
        raise ValueError(f"table not found under {heading!r} in {path}")
    separator_end = text.find("\n", text.find("\n", table_start + 1) + 1)
    if separator_end < 0:
        raise ValueError(f"table separator not found under {heading!r} in {path}")
    updated = text[: separator_end + 1] + row + "\n" + text[separator_end + 1 :]
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=sorted(SECTIONS), required=True)
    parser.add_argument("--venue-year", required=True, help="For example: CVPR 2027 or ArXiv 2027")
    parser.add_argument("--method", default="—")
    parser.add_argument("--title", required=True)
    parser.add_argument("--paper-url", required=True)
    parser.add_argument("--code-url", default="")
    parser.add_argument("--dataset-url", default="")
    parser.add_argument("--project-url", default="")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--readme-zh", default="README.zh-CN.md")
    args = parser.parse_args()

    section, columns = SECTIONS[args.section]
    insert_row(Path(args.readme), section, make_row(args, False, columns), args.title)
    insert_row(Path(args.readme_zh), section, make_row(args, True, columns), args.title)
    print(f"Added {args.title!r} to {section!r} in both README files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
