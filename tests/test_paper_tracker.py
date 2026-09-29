import tempfile
import unittest
from pathlib import Path

from scripts.add_paper import insert_row
from scripts.paper_tracker import (
    Paper,
    already_listed,
    existing_index,
    markdown_report,
    merge_duplicates,
    score_paper,
    suggest_section,
)


class PaperTrackerTests(unittest.TestCase):
    def test_scores_relevant_agreid_paper(self):
        paper = Paper(
            title="Aerial-Ground Person Re-Identification with Cross-View Alignment",
            url="https://example.test/paper",
        )
        score, reasons = score_paper(paper)
        self.assertGreaterEqual(score, 11)
        self.assertIn("明确包含 aerial-ground", reasons)
        self.assertEqual(suggest_section(paper), "Image-based Person AG-ReID")

    def test_rejects_non_reidentification_paper(self):
        paper = Paper(title="Aerial-Ground 3D Reconstruction", url="https://example.test/paper")
        score, _ = score_paper(paper)
        self.assertEqual(score, 0)

    def test_downranks_visual_place_recognition(self):
        paper = Paper(
            title="Training-Free Aggregation for Visual Place Recognition",
            abstract="Retrieval across aerial, ground, and cross-view protocols.",
            url="https://example.test/paper",
        )
        score, reasons = score_paper(paper)
        self.assertLess(score, 7)
        self.assertTrue(any("降权" in reason for reason in reasons))

    def test_merges_doi_duplicates(self):
        first = Paper(title="One title", url="https://doi.org/10.1/x", doi="10.1/x", sources=["Crossref"])
        second = Paper(title="One title extended", url="https://example.test", doi="10.1/x", sources=["OpenAlex"])
        merged = merge_duplicates([first, second])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].sources, ["Crossref", "OpenAlex"])

    def test_detects_existing_arxiv_and_title(self):
        readme = "| **CVPR 2026** | X | Aerial Ground Person ReID | [Paper](https://arxiv.org/abs/2601.12345) |"
        index = existing_index(readme)
        self.assertTrue(already_listed(Paper(title="Different", url="", arxiv_id="2601.12345"), index))
        self.assertTrue(already_listed(Paper(title="Aerial Ground Person ReID", url=""), index))

    def test_detects_index_title_with_method_prefix(self):
        readme = "| **TIP 2026** | SD-ReID | View-Aware Stable Diffusion for Aerial-Ground Person Re-Identification | Link |"
        paper = Paper(title="SD-ReID: View-Aware Stable Diffusion for Aerial-Ground Person Re-Identification", url="")
        self.assertTrue(already_listed(paper, existing_index(readme)))

    def test_report_contains_stable_marker(self):
        report = markdown_report([], "2026-01-01", [])
        self.assertIn("paper-tracker:rolling-candidates", report)
        self.assertIn("候选数：0", report)

    def test_insert_row_after_table_separator(self):
        content = "# Test\n\n### Image-based Person AG-ReID\n\n| Venue | Method | Title | Resources |\n| --- | --- | --- | --- |\n| Old | X | Existing | Link |\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(content, encoding="utf-8")
            insert_row(path, "Image-based Person AG-ReID", "| New | Y | New Paper | Link |", "New Paper")
            updated = path.read_text(encoding="utf-8")
            self.assertLess(updated.index("New Paper"), updated.index("Existing"))


if __name__ == "__main__":
    unittest.main()
