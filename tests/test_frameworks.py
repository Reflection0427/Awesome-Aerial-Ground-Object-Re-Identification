from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_KINDS = {"framework", "architecture", "pipeline", "overview", "taxonomy", "benchmark", "dataset"}


class FrameworkFigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = json.loads((ROOT / "data" / "frameworks.json").read_text(encoding="utf-8"))
        cls.datasets = json.loads((ROOT / "data" / "datasets.json").read_text(encoding="utf-8"))
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    def test_exactly_36_unique_original_figures(self) -> None:
        self.assertEqual(36, len(self.records))
        ids = [record["paper_id"] for record in self.records]
        self.assertEqual(len(ids), len(set(ids)))
        expected = {ROOT / record["figure"]["path"] for record in self.records}
        actual = set((ROOT / "assets" / "frameworks").glob("*.png"))
        self.assertEqual(expected, actual)
        self.assertFalse(list((ROOT / "assets" / "frameworks").glob("*.svg")))

    def test_metadata_is_complete_and_reproducible(self) -> None:
        for record in self.records:
            with self.subTest(record["paper_id"]):
                figure = record["figure"]
                self.assertIsInstance(record["authors"], list)
                self.assertTrue(record["authors"])
                self.assertEqual(f"assets/frameworks/{record['paper_id']}.png", figure["path"])
                self.assertTrue(figure["source_pdf_url"].startswith("https://"))
                self.assertRegex(figure["source_pdf_sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(figure["figure_label"], r"^Figure [1-9][0-9]*$")
                self.assertIn(figure["figure_kind"], ALLOWED_KINDS)
                self.assertGreaterEqual(figure["page"], 1)
                self.assertEqual(4, len(figure["crop_pt"]))
                x0, y0, x1, y1 = figure["crop_pt"]
                self.assertLess(x0, x1)
                self.assertLess(y0, y1)

    def test_images_are_readable_nonblank_and_web_sized(self) -> None:
        for record in self.records:
            path = ROOT / record["figure"]["path"]
            with self.subTest(record["paper_id"]), Image.open(path) as image:
                image.verify()
            with Image.open(path).convert("RGB") as image:
                self.assertGreaterEqual(min(image.size), 180)
                self.assertLessEqual(max(image.size), 2400)
                self.assertLessEqual(path.stat().st_size, 5 * 1024 * 1024)
                self.assertGreater(sum(ImageStat.Stat(image.resize((64, 64))).var), 20.0)

    def test_readmes_include_every_figure_and_no_curator_svg(self) -> None:
        for record in self.records:
            path = record["figure"]["path"]
            self.assertEqual(1, self.readme.count(path), path)
            self.assertEqual(1, self.readme_zh.count(path), path)
        self.assertIn("| Conference / Journal | Method | Title | Resources | Framework |", self.readme)
        self.assertIn("| 会议 / 期刊 | 方法 | 标题 | 资源 | 框架图 |", self.readme_zh)
        self.assertNotRegex(self.readme + self.readme_zh, r"CURATOR-DRAWN|assets/frameworks/[^)\" ]+\.svg")

    def test_dataset_and_sota_scope(self) -> None:
        self.assertEqual(6, len(self.datasets["datasets"]))
        self.assertEqual(
            ["AG-ReID", "AG-ReID.v2", "CARGO", "G2APS-ReID", "LAGPeR"],
            [row["dataset"] for row in self.datasets["sota"]],
        )
        for name in ["AG-ReID", "AG-ReID.v2", "CARGO", "G2APS-ReID", "LAGPeR", "CP2108"]:
            self.assertIn(f"**{name}**", self.readme)

    def test_generated_readmes_are_current(self) -> None:
        result = subprocess.run(
            ["python", "scripts/update_readmes.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
