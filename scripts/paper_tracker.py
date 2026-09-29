#!/usr/bin/env python3
"""Discover recent AG-ReID papers and produce a human-review report.

The tracker intentionally never edits README.md. A separate, manually triggered
workflow turns an approved candidate into a pull request.
"""

from __future__ import annotations

import argparse
import html
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


USER_AGENT = "awesome-agreid-paper-tracker/1.0 (+https://github.com/)"
ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
DOI_RE = re.compile(r"(?:doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s)\]}>]+)", re.I)
YEAR_RE = re.compile(r"\b(20\d{2})\b")


@dataclass
class Paper:
    title: str
    url: str
    published: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    venue: str = ""
    doi: str = ""
    arxiv_id: str = ""
    source_ids: dict[str, str] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    suggested_section: str = "More Related Exploration"

    @property
    def identifier(self) -> str:
        if self.arxiv_id:
            return f"arxiv:{self.arxiv_id.lower()}"
        if self.doi:
            return f"doi:{self.doi.lower()}"
        return f"title:{normalize_title(self.title)}"


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def normalize_title(value: str) -> str:
    value = compact(value).lower().replace("–", "-").replace("—", "-")
    return re.sub(r"[^a-z0-9]+", "", value)


def normalize_doi(value: str) -> str:
    value = compact(value).lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value.rstrip(".,;)")


def normalize_arxiv(value: str) -> str:
    match = ARXIV_RE.search(value or "")
    return match.group(1) if match else compact(value).removeprefix("arXiv:").split("v")[0]


def arxiv_from_doi(doi: str) -> str:
    prefix = "10.48550/arxiv."
    return normalize_arxiv(doi[len(prefix):]) if doi.lower().startswith(prefix) else ""


def iso_date(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        return value[:10]
    if isinstance(value, list) and value and isinstance(value[0], list):
        parts = value[0]
        return "-".join(str(x).zfill(2) for x in parts[:3])
    return ""


def request_bytes(base_url: str, params: dict[str, Any], accept: str, timeout: int = 15) -> bytes:
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, http.client.HTTPException, OSError, TimeoutError):
            if attempt:
                raise
            time.sleep(1)
    raise RuntimeError("unreachable")


def get_json(base_url: str, params: dict[str, Any], timeout: int = 15) -> dict[str, Any]:
    return json.loads(request_bytes(base_url, params, "application/json", timeout).decode("utf-8"))


def get_text(base_url: str, params: dict[str, Any], timeout: int = 15) -> str:
    return request_bytes(base_url, params, "application/atom+xml", timeout).decode("utf-8")


def fetch_arxiv(query: str, limit: int) -> list[Paper]:
    # Searching all fields gives better recall; local scoring removes broad matches.
    search = " AND ".join(f'all:"{word}"' for word in query.split())
    xml = get_text(
        "https://export.arxiv.org/api/query",
        {"search_query": search, "start": 0, "max_results": limit,
         "sortBy": "submittedDate", "sortOrder": "descending"},
    )
    root = ET.fromstring(xml)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ns):
        entry_id = compact(entry.findtext("atom:id", default="", namespaces=ns))
        arxiv_id = normalize_arxiv(entry_id)
        doi = normalize_doi(entry.findtext("arxiv:doi", default="", namespaces=ns))
        papers.append(Paper(
            title=compact(entry.findtext("atom:title", default="", namespaces=ns)),
            url=f"https://arxiv.org/abs/{arxiv_id}",
            published=iso_date(entry.findtext("atom:published", default="", namespaces=ns)),
            authors=[compact(a.findtext("atom:name", default="", namespaces=ns))
                     for a in entry.findall("atom:author", ns)],
            abstract=compact(entry.findtext("atom:summary", default="", namespaces=ns)),
            venue=compact(entry.findtext("arxiv:journal_ref", default="", namespaces=ns)),
            doi=doi,
            arxiv_id=arxiv_id,
            source_ids={"arxiv": arxiv_id},
            sources=["arXiv"],
        ))
    return papers


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    words: list[tuple[int, str]] = []
    for word, positions in index.items():
        words.extend((position, word) for position in positions)
    return " ".join(word for _, word in sorted(words))


def fetch_openalex(query: str, since: str, limit: int) -> list[Paper]:
    params: dict[str, Any] = {
        "search": query,
        "filter": f"from_publication_date:{since}",
        "sort": "publication_date:desc",
        "per_page": min(limit, 100),
    }
    if os.getenv("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    data = get_json("https://api.openalex.org/works", params)
    papers: list[Paper] = []
    for item in data.get("results", []):
        ids = item.get("ids") or {}
        doi = normalize_doi(ids.get("doi", ""))
        arxiv_id = normalize_arxiv(ids.get("arxiv", "")) if ids.get("arxiv") else arxiv_from_doi(doi)
        location = item.get("best_oa_location") or item.get("primary_location") or {}
        url = ids.get("arxiv") or ids.get("doi") or location.get("landing_page_url") or item.get("id", "")
        source = (location.get("source") or {}).get("display_name", "")
        authors = [compact(a.get("author", {}).get("display_name", ""))
                   for a in item.get("authorships", [])]
        source_id = str(item.get("id", "")).rsplit("/", 1)[-1]
        papers.append(Paper(
            title=compact(item.get("display_name") or item.get("title", "")),
            url=url,
            published=iso_date(item.get("publication_date", "")),
            authors=[a for a in authors if a],
            abstract=reconstruct_abstract(item.get("abstract_inverted_index")),
            venue=compact(source),
            doi=doi,
            arxiv_id=arxiv_id,
            source_ids={"openalex": source_id},
            sources=["OpenAlex"],
        ))
    return papers


def crossref_date(item: dict[str, Any]) -> str:
    for key in ("published-online", "published-print", "published", "issued", "created"):
        parts = (item.get(key) or {}).get("date-parts")
        if parts:
            return iso_date(parts)
    return ""


def fetch_crossref(query: str, since: str, limit: int, email: str) -> list[Paper]:
    params: dict[str, Any] = {
        "query.bibliographic": query,
        "filter": f"from-pub-date:{since}",
        "rows": limit,
        "select": "DOI,title,author,abstract,container-title,published,published-online,published-print,issued,created,URL",
    }
    if email:
        params["mailto"] = email
    data = get_json("https://api.crossref.org/works", params)
    papers: list[Paper] = []
    for item in data.get("message", {}).get("items", []):
        title = compact((item.get("title") or [""])[0])
        doi = normalize_doi(item.get("DOI", ""))
        authors = [compact(" ".join(filter(None, (a.get("given"), a.get("family")))))
                   for a in item.get("author", [])]
        venue = compact((item.get("container-title") or [""])[0])
        papers.append(Paper(
            title=title,
            url=item.get("URL") or (f"https://doi.org/{doi}" if doi else ""),
            published=crossref_date(item),
            authors=[a for a in authors if a],
            abstract=compact(re.sub(r"<[^>]+>", " ", item.get("abstract", ""))),
            venue=venue,
            doi=doi,
            arxiv_id=arxiv_from_doi(doi),
            source_ids={"crossref": doi},
            sources=["Crossref"],
        ))
    return papers


def fetch_dblp(query: str, since: str, limit: int) -> list[Paper]:
    data = get_json("https://dblp.org/search/publ/api", {"q": query, "format": "json", "h": limit})
    raw_hits = data.get("result", {}).get("hits", {}).get("hit", [])
    if isinstance(raw_hits, dict):
        raw_hits = [raw_hits]
    papers: list[Paper] = []
    for hit in raw_hits:
        info = hit.get("info", {})
        year = str(info.get("year", ""))
        if year and f"{year}-12-31" < since:
            continue
        raw_authors = (info.get("authors") or {}).get("author", [])
        if isinstance(raw_authors, (str, dict)):
            raw_authors = [raw_authors]
        authors = [compact(a.get("text", "") if isinstance(a, dict) else str(a)) for a in raw_authors]
        doi = normalize_doi(info.get("doi", ""))
        key = compact(info.get("key", ""))
        ee = info.get("ee") or info.get("url", "")
        if isinstance(ee, list):
            ee = ee[0] if ee else ""
        papers.append(Paper(
            title=compact(re.sub(r"<[^>]+>", "", info.get("title", ""))),
            url=compact(ee),
            published=f"{year}-01-01" if year else "",
            authors=[a for a in authors if a],
            venue=compact(info.get("venue", "")),
            doi=doi,
            source_ids={"dblp": key},
            sources=["DBLP"],
        ))
    return papers


def score_paper(paper: Paper) -> tuple[int, list[str]]:
    text = f"{paper.title} {paper.abstract}".lower().replace("–", "-").replace("—", "-")
    score = 0
    reasons: list[str] = []

    strong_phrases = ("aerial-ground", "aerial ground", "ground-aerial", "ground aerial")
    strong_match = any(p in text for p in strong_phrases)
    if strong_match:
        score += 5
        reasons.append("明确包含 aerial-ground")

    identity = bool(re.search(r"\b(re[- ]?identification|reid|retrieval)\b", text))
    aerial = bool(re.search(r"\b(aerial|uav|drone|unmanned aerial)\b", text))
    ground = bool(re.search(r"\b(ground|terrestrial)\b", text))
    cross_view = bool(re.search(r"\b(cross[- ]?(view|platform|camera)|view[- ]invariant)\b", text))
    target = bool(re.search(r"\b(person|pedestrian|vehicle|object|animal)\b", text))

    for matched, points, reason in (
        (identity, 3, "ReID/检索任务"),
        (aerial, 2, "空中/UAV/无人机视角"),
        (ground, 2, "地面视角"),
        (cross_view, 1, "跨视角/跨平台"),
        (target, 1, "人员/车辆/目标对象"),
    ):
        if matched:
            score += points
            reasons.append(reason)

    # Re-identification is mandatory. Pure aerial detection/reconstruction is noise.
    if not identity:
        return 0, ["缺少 ReID/检索语义"]
    if not target and not strong_match:
        score -= 4
        reasons.append("降权：未识别到人员/车辆/目标对象")
    return score, reasons


def suggest_section(paper: Paper) -> str:
    text = f"{paper.title} {paper.abstract}".lower()
    if "challenge" in text or "workshop" in text:
        return "Challenges & Workshops"
    if "vehicle" in text:
        return "Image-based Vehicle AG-ReID"
    if "video" in text or "temporal" in text or "tracklet" in text:
        return "Video-based Person AG-ReID"
    if any(word in text for word in ("person", "pedestrian")):
        return "Image-based Person AG-ReID"
    return "More Related Exploration"


def same_paper(left: Paper, right: Paper) -> bool:
    if left.doi and right.doi and left.doi == right.doi:
        return True
    if left.arxiv_id and right.arxiv_id and left.arxiv_id == right.arxiv_id:
        return True
    a, b = normalize_title(left.title), normalize_title(right.title)
    return bool(a and b and (a == b or SequenceMatcher(None, a, b).ratio() >= 0.94))


def merge_two(target: Paper, other: Paper) -> Paper:
    target.sources = sorted(set(target.sources + other.sources))
    target.source_ids.update({k: v for k, v in other.source_ids.items() if v})
    target.authors = target.authors or other.authors
    target.abstract = max((target.abstract, other.abstract), key=len)
    target.venue = target.venue or other.venue
    target.doi = target.doi or other.doi
    target.arxiv_id = target.arxiv_id or other.arxiv_id
    target.published = target.published or other.published
    if target.arxiv_id:
        target.url = f"https://arxiv.org/abs/{target.arxiv_id}"
    elif target.doi:
        target.url = f"https://doi.org/{target.doi}"
    elif not target.url:
        target.url = other.url
    return target


def merge_duplicates(papers: Iterable[Paper]) -> list[Paper]:
    merged: list[Paper] = []
    for paper in papers:
        match = next((candidate for candidate in merged if same_paper(candidate, paper)), None)
        if match:
            merge_two(match, paper)
        else:
            merged.append(paper)
    return merged


def existing_index(readme: str) -> tuple[set[str], set[str], list[str]]:
    arxiv_ids = {m.group(1).lower() for m in ARXIV_RE.finditer(readme)}
    dois = {normalize_doi(m.group(1)) for m in DOI_RE.finditer(readme)}
    titles: list[str] = []
    for line in readme.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [compact(cell).strip("* ") for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and not cells[0].startswith(":") and cells[2].lower() != "title":
            normalized = normalize_title(cells[2])
            if len(normalized) >= 12:
                titles.append(normalized)
    return arxiv_ids, dois, titles


def already_listed(paper: Paper, index: tuple[set[str], set[str], list[str]]) -> bool:
    arxiv_ids, dois, titles = index
    if paper.arxiv_id and paper.arxiv_id.lower() in arxiv_ids:
        return True
    if paper.doi and paper.doi.lower() in dois:
        return True
    normalized = normalize_title(paper.title)
    # Index metadata often prefixes the method name (for example "SD-ReID:")
    # while the README stores that method in its own column.
    return any(SequenceMatcher(None, normalized, title).ratio() >= 0.94 for title in titles)


def confidence(score: int) -> str:
    return "高" if score >= 11 else "中" if score >= 8 else "低"


def markdown_report(papers: list[Paper], since: str, failures: list[str]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "<!-- paper-tracker:rolling-candidates -->",
        "## AG-ReID 自动发现候选论文",
        "",
        f"扫描时间：{now}　检索范围：{since} 至今　候选数：{len(papers)}",
        "",
        "> 这是机器筛选结果，并未自动写入正式清单。请检查任务相关性、重复版本、venue 和资源链接。",
        "",
    ]
    if not papers:
        lines += ["本轮没有发现尚未收录的候选论文。", ""]
    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper.authors[:8]) or "未知"
        if len(paper.authors) > 8:
            authors += ", et al."
        identifiers = []
        if paper.arxiv_id:
            identifiers.append(f"arXiv `{paper.arxiv_id}`")
        if paper.doi:
            identifiers.append(f"DOI `{paper.doi}`")
        identifiers.extend(f"{key} `{value}`" for key, value in paper.source_ids.items()
                           if value and key not in {"arxiv", "crossref"})
        lines += [
            f"### {i}. [{paper.title}]({paper.url})",
            "",
            f"- 置信度：**{confidence(paper.score)}**（{paper.score} 分）",
            f"- 建议分类：`{paper.suggested_section}`",
            f"- 日期 / Venue：{paper.published or '未知'} / {paper.venue or '待确认'}",
            f"- 作者：{authors}",
            f"- 数据来源：{', '.join(paper.sources)}",
            f"- 标识符：{' · '.join(identifiers) or '无'}",
            f"- 命中原因：{'；'.join(paper.reasons)}",
            "",
            "审核：- [ ] 收录　- [ ] 忽略　- [ ] 需要进一步核实",
            "",
        ]
    if failures:
        lines += ["## 数据源警告", ""] + [f"- {failure}" for failure in failures] + [""]
    lines += [
        "## 收录方法",
        "",
        "确认论文后，打开 Actions → **Accept paper candidate** → Run workflow，填写论文信息。",
        "自动化会新建一个修改中英文 README 的 PR；检查并合并后，趋势图会自动更新。",
        "",
        "如果决定永久忽略某项，请把它的 `arxiv:ID`、`doi:DOI` 或规范化标题加入 "
        "`config/paper-tracker.json` 的忽略列表。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def discover(config: dict[str, Any], readme: str) -> tuple[list[Paper], list[str], str]:
    since = (date.today() - timedelta(days=int(config["lookback_days"]))).isoformat()
    limit = int(config["max_results_per_query"])
    email = os.getenv("PAPER_TRACKER_EMAIL", "")
    collected: list[Paper] = []
    failures: list[str] = []
    fetchers = {
        "arxiv": lambda q: fetch_arxiv(q, limit),
        "openalex": lambda q: fetch_openalex(q, since, limit),
        "crossref": lambda q: fetch_crossref(q, since, limit, email),
        "dblp": lambda q: fetch_dblp(q, since, limit),
    }
    for source in config["sources"]:
        for query in config["queries"]:
            try:
                collected.extend(fetchers[source](query))
            except Exception as exc:
                failures.append(f"{source} / `{query}`：{type(exc).__name__}: {exc}")
                if isinstance(exc, (urllib.error.URLError, http.client.HTTPException, OSError,
                                    TimeoutError, json.JSONDecodeError)):
                    # Avoid waiting through every keyword when the whole provider is unavailable.
                    break
            # arXiv asks clients to leave a delay between repeated calls.
            if source == "arxiv" and os.getenv("PAPER_TRACKER_NO_DELAY") != "1":
                time.sleep(3)
            elif source == "dblp":
                time.sleep(1)

    index = existing_index(readme)
    ignored_ids = {compact(x).lower() for x in config.get("ignored_identifiers", [])}
    ignored_titles = {normalize_title(x) for x in config.get("ignored_titles", [])}
    candidates: list[Paper] = []
    for paper in merge_duplicates(collected):
        if paper.published and paper.published[:10] < since:
            continue
        paper.score, paper.reasons = score_paper(paper)
        paper.suggested_section = suggest_section(paper)
        if paper.score < int(config["minimum_score"]):
            continue
        if paper.identifier.lower() in ignored_ids or normalize_title(paper.title) in ignored_titles:
            continue
        if already_listed(paper, index):
            continue
        candidates.append(paper)
    candidates.sort(key=lambda p: (p.score, p.published, p.title), reverse=True)
    return candidates[: int(config.get("max_candidates", 30))], failures, since


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/paper-tracker.json")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--output", default=".paper-tracker/report.md")
    parser.add_argument("--json-output", default=".paper-tracker/candidates.json")
    parser.add_argument("--offline-input", help="Use a JSON list of Paper dictionaries instead of APIs")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    readme = Path(args.readme).read_text(encoding="utf-8")
    if args.offline_input:
        papers = [Paper(**item) for item in json.loads(Path(args.offline_input).read_text(encoding="utf-8"))]
        index = existing_index(readme)
        candidates = []
        for paper in merge_duplicates(papers):
            paper.score, paper.reasons = score_paper(paper)
            paper.suggested_section = suggest_section(paper)
            if paper.score >= int(config["minimum_score"]) and not already_listed(paper, index):
                candidates.append(paper)
        failures: list[str] = []
        since = "offline fixture"
    else:
        candidates, failures, since = discover(config, readme)

    output = Path(args.output)
    json_output = Path(args.json_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(candidates, since, failures), encoding="utf-8")
    json_output.write_text(json.dumps([asdict(p) for p in candidates], ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"candidate_count={len(candidates)}")
    print(f"failure_count={len(failures)}")
    if os.getenv("GITHUB_OUTPUT"):
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as github_output:
            github_output.write(f"candidate_count={len(candidates)}\n")
            github_output.write(f"failure_count={len(failures)}\n")
    if failures:
        print("\n".join(failures), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
