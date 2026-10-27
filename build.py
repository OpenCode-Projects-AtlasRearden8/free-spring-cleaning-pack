#!/usr/bin/env python3
"""Build the Spring Cleaning Free Pack.

Renders every HTML sheet in sources/ to an unbranded PDF in printables/
using WeasyPrint. Fully local: no network, no accounts, no secrets.

Usage:
    python3 build.py                # build all sheets into printables/
    python3 build.py --out DIR      # build into a different directory
    python3 build.py --strict       # fail on warnings as well as errors
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
DEFAULT_OUT = ROOT / "printables"

WEASY_LOGGER = logging.getLogger("weasyprint")


def build_all(out_dir: Path = DEFAULT_OUT, strict: bool = False) -> list[Path]:
    """Render every sources/*.html sheet to out_dir/*.pdf. Returns PDF paths."""
    from weasyprint import HTML  # imported lazily so --help needs no install

    sheets = sorted(SOURCES.glob("*.html"))
    if not sheets:
        raise SystemExit(f"No HTML sheets found in {SOURCES}")

    out_dir.mkdir(parents=True, exist_ok=True)

    class _Collector(logging.Handler):
        """Capture WeasyPrint warnings/errors so a bad sheet can fail the build."""

        def __init__(self, sink: list[str]) -> None:
            super().__init__()
            self.sink = sink

        def emit(self, record: logging.LogRecord) -> None:
            if record.levelno >= logging.WARNING or strict:
                self.sink.append(record.getMessage())

    built: list[Path] = []
    for sheet in sheets:
        pdf_path = out_dir / (sheet.stem + ".pdf")
        warnings: list[str] = []
        collector = _Collector(warnings)
        WEASY_LOGGER.addHandler(collector)
        try:
            html = HTML(filename=str(sheet), base_url=str(SOURCES))
            html.write_pdf(target=str(pdf_path))
        finally:
            WEASY_LOGGER.removeHandler(collector)

        size = pdf_path.stat().st_size
        print(f"built  {pdf_path.name}  ({size:,} bytes, "
              f"{len(warnings)} warning(s))")
        if warnings:
            for w in warnings:
                print(f"  warn: {w}")
        if strict and warnings:
            raise SystemExit(f"strict mode: warnings in {sheet.name}: {warnings}")

        # Sanity-check the artifact before declaring victory.
        magic = pdf_path.read_bytes()[:5]
        if magic != b"%PDF-":
            raise SystemExit(f"{pdf_path} is not a valid PDF (header {magic!r})")
        built.append(pdf_path)

    return built


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="output directory (default: printables/)")
    parser.add_argument("--strict", action="store_true",
                        help="treat CSS/layout warnings as errors")
    args = parser.parse_args(argv)

    built = build_all(out_dir=args.out, strict=args.strict)
    print(f"\nDone: {len(built)} PDF(s) in {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
