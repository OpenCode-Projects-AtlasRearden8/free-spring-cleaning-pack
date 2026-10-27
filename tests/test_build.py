"""Tests for the Spring Cleaning Free Pack build.

Every source sheet must produce a valid, non-empty, Letter-size PDF.
The tests run the real build once into a temporary directory, so they
verify build.py end to end without touching the committed printables/.

Works with either runner:

    pytest -v
    python3 -m unittest discover -s tests -t . -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"

sys.path.insert(0, str(ROOT))
from build import build_all  # noqa: E402

from pypdf import PdfReader  # noqa: E402

EXPECTED_SHEETS = [
    "00-getting-started",
    "01-room-walkthroughs",
    "02-zone-timers",
    "03-declutter-decision-card",
    "04-drop-log",
    "05-deep-vs-daily",
    "06-windows-wet-weather",
    "07-big-ticket-wishlist",
]


class BuildTests(unittest.TestCase):
    """Build every sheet once into a fresh temp dir, then inspect the PDFs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.out_dir = Path(tempfile.mkdtemp(prefix="pack_test_", dir="/tmp/opencode")) / "out"
        cls.built = build_all(out_dir=cls.out_dir)
        cls.stems = sorted(p.stem for p in cls.built)

    def test_expected_sheets_exist_in_sources(self) -> None:
        stems = sorted(p.stem for p in SOURCES.glob("*.html"))
        self.assertEqual(stems, EXPECTED_SHEETS, f"unexpected sheet set: {stems}")

    def test_build_produces_one_pdf_per_sheet(self) -> None:
        self.assertEqual(self.stems, EXPECTED_SHEETS)
        for pdf in self.built:
            self.assertTrue(pdf.exists() and pdf.stat().st_size > 1_000, pdf)

    def test_every_pdf_is_valid_and_letter_sized(self) -> None:
        for pdf in self.built:
            self.assertEqual(pdf.read_bytes()[:5], b"%PDF-", f"{pdf.name}: not a PDF")
            reader = PdfReader(str(pdf))
            self.assertGreaterEqual(len(reader.pages), 1)
            for page in reader.pages:
                w, h = float(page.mediabox.width), float(page.mediabox.height)
                self.assertAlmostEqual(w, 612, delta=2)
                self.assertAlmostEqual(h, 792, delta=2)

    def test_every_pdf_has_extractable_text(self) -> None:
        for pdf in self.built:
            reader = PdfReader(str(pdf))
            text = "".join(p.extract_text() or "" for p in reader.pages)
            self.assertTrue(text.strip(), f"{pdf.name}: no extractable text")

    def test_committed_printables_match_sources(self) -> None:
        committed = ROOT / "printables"
        if not committed.exists():
            self.skipTest("printables/ not built yet")
        for stem in EXPECTED_SHEETS:
            with self.subTest(sheet=stem):
                committed_pdf = committed / f"{stem}.pdf"
                self.assertTrue(committed_pdf.exists())
                self.assertEqual(committed_pdf.read_bytes()[:5], b"%PDF-")
                self.assertEqual(
                    len(PdfReader(str(committed_pdf)).pages),
                    len(PdfReader(str(self.out_dir / f"{stem}.pdf")).pages),
                )


if __name__ == "__main__":
    unittest.main()
