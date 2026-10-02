#!/usr/bin/env python3
"""Synchronize framework cells and dataset/SOTA tables in both READMEs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_SECTIONS = {
    "Image-based Person AG-ReID",
    "Image-based Vehicle AG-ReID",
    "Video-based Person AG-ReID",
    "基于图像的行人 AG-ReID",
    "基于图像的车辆 AG-ReID",
    "基于视频的行人 AG-ReID",
}


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def framework_cell(record: dict, chinese: bool) -> str:
    figure = record["figure"]
    label = figure["figure_label"]
    source = figure["source_pdf_url"]
    image = figure["path"]
    alt = f"{record['title']} — {label}"
    license_link = ""
    if figure.get("license_url"):
        license_text = "许可证" if chinese else "License"
        license_link = f" · [{license_text}]({figure['license_url']})"
    if chinese:
        note = f"论文原图：[ {label} ]({source}) · 来源：官方 PDF。<br>© 论文作者/出版方，权利归原权利人所有{license_link}"
    else:
        note = f"Original paper figure: [{label}]({source}) · Source: official PDF.<br>© Paper authors/publisher. All rights remain with the original owner{license_link}"
    return f'<img src="{image}" width="320" alt="{alt}"><br><sub>{note}</sub>'


def update_framework_tables(text: str, records: list[dict], chinese: bool) -> str:
    lookup = {normalized(record["title"]): record for record in records}
    current_section = ""
    seen: set[str] = set()
    output: list[str] = []
    for line in text.splitlines():
        if line.startswith("### "):
            current_section = line[4:].strip()
        if current_section not in CORE_SECTIONS or not line.startswith("|"):
            output.append(line)
            continue
        cells = [cell.strip() for cell in line.strip()[1:-1].split("|")]
        if len(cells) < 4:
            output.append(line)
            continue
        if ("Conference / Journal" in cells[0] or "会议" in cells[0]) and ("Method" in cells[1] or "方法" in cells[1]):
            framework_header = "框架图" if chinese else "Framework"
            output.append("| " + " | ".join(cells[:4] + [framework_header]) + " |")
        elif all(set(cell) <= {":", "-", " "} for cell in cells[:4]):
            output.append("| " + " | ".join(cells[:4] + [":---:"]) + " |")
        else:
            key = normalized(cells[2])
            if key not in lookup:
                raise ValueError(f"no framework metadata for README title: {cells[2]}")
            record = lookup[key]
            seen.add(record["paper_id"])
            output.append("| " + " | ".join(cells[:4] + [framework_cell(record, chinese)]) + " |")
    if seen != {record["paper_id"] for record in records}:
        missing = sorted({record["paper_id"] for record in records} - seen)
        raise ValueError(f"framework metadata not used in README: {missing}")
    return "\n".join(output) + "\n"


def dataset_block(data: dict, chinese: bool) -> str:
    if chinese:
        heading = "## 💾 数据集"
        intro = "以下统计来自各数据集论文；A/G/W 分别表示空中、地面和可穿戴相机。"
        headers = ["数据集", "来源", "ID 数", "图像数", "数据来源", "场景", "相机", "属性", "文本描述", "光照", "跨时间", "季节", "高度", "下载"]
        yes, no, link = "✓", "×", "链接"
        sota_heading = "### 当前 SOTA（前五个公开基准）"
        extra_heading = "#### 其他相关数据集"
        extra_headers = ["数据集", "来源", "类别", "下载"]
        sota_intro = f"截至 **{data['verified_on']}**，下表按各论文报告的标准协议汇总；每个协议按最高报告 mAP 选择方法，数值为该方法的 **mAP / Rank-1（%）**（Rank-1 不一定是该列单项最高），结果未独立复现。"
        sota_headers = ["数据集", "方法", "标准协议结果（mAP / Rank-1）", "来源"]
    else:
        heading = "## 💾 Datasets"
        intro = "Statistics are taken from the dataset papers; A/G/W denote aerial, ground, and wearable cameras."
        headers = ["Dataset", "Source", "IDs", "Images", "Data", "Scenes", "Cameras", "Attributes", "Captions", "Illumination", "Cross-Time", "Season", "Altitude", "Download"]
        yes, no, link = "✓", "×", "Link"
        sota_heading = "### Current SOTA on the first five public benchmarks"
        extra_heading = "#### Other related datasets"
        extra_headers = ["Dataset", "Source", "Category", "Download"]
        sota_intro = f"Verified on **{data['verified_on']}** from reported standard protocols. For each protocol, the method is selected by the highest reported mAP; the paired value is that same method's **mAP / Rank-1 (%)** (so Rank-1 is not necessarily the standalone maximum). Results have not been independently reproduced."
        sota_headers = ["Dataset", "Method(s)", "Standard-protocol result (mAP / Rank-1)", "Source"]
    lines = [heading, "", intro, "", "| " + " | ".join(headers) + " |", "| " + " | ".join([":---"] * len(headers)) + " |"]
    for item in data["datasets"]:
        values = [
            f"**{item['name']}**", item["source"], str(item["ids"]), str(item["images"]), item["data_source"],
            str(item["scenarios"]), item["cameras"], str(item["attributes"]), yes if item["captions"] else no,
            item["illumination"], yes if item["cross_time"] else no, item["season"], item["altitude"],
            f"[{link}]({item['download_url']})",
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines.extend(["", extra_heading, "", "| " + " | ".join(extra_headers) + " |", "| " + " | ".join([":---"] * len(extra_headers)) + " |"])
    for item in data["additional_datasets"]:
        lines.append(f"| **{item['name']}** | {item['source']} | {item['category']} | [{link}]({item['download_url']}) |")
    lines.extend(["", sota_heading, "", sota_intro, "", "| " + " | ".join(sota_headers) + " |", "| " + " | ".join([":---"] * len(sota_headers)) + " |"])
    for item in data["sota"]:
        sources = " · ".join(f"[{source['label']}]({source['url']})" for source in item["sources"])
        lines.append(f"| **{item['dataset']}** | {item['methods']} | {item['results']} | {sources} |")
    return "\n".join(lines)


def update_dataset_section(text: str, data: dict, chinese: bool) -> str:
    heading = "## 💾 数据集" if chinese else "## 💾 Datasets"
    start = text.index(heading)
    end = text.index("\n---", start)
    return text[:start] + dataset_block(data, chinese) + "\n" + text[end:]


def render(path: Path, records: list[dict], datasets: dict, chinese: bool) -> str:
    text = path.read_text(encoding="utf-8")
    text = update_framework_tables(text, records, chinese)
    return update_dataset_section(text, datasets, chinese)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    records = json.loads((ROOT / "data" / "frameworks.json").read_text(encoding="utf-8"))
    datasets = json.loads((ROOT / "data" / "datasets.json").read_text(encoding="utf-8"))
    changed = []
    for name, chinese in (("README.md", False), ("README.zh-CN.md", True)):
        path = ROOT / name
        updated = render(path, records, datasets, chinese)
        if updated != path.read_text(encoding="utf-8"):
            changed.append(name)
            if not args.check:
                path.write_text(updated, encoding="utf-8")
    if args.check and changed:
        print("README files are stale: " + ", ".join(changed))
        return 1
    if not args.check:
        print("Updated: " + ", ".join(changed or ["nothing (already current)"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
