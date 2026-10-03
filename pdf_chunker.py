#!/usr/bin/env python3
"""
PDF Chunker for AI
===========
Split PDFs into AI-ready chunks under page & size limits.

For every ``Something.pdf`` in the input folder this tool:

1. Creates a folder ``Something/``
2. Splits the PDF into chunks that are **at most N pages** *and*
   **at most M megabytes**
3. Names each chunk ``Something_p001-015.pdf``, ``Something_p016-030.pdf``, …
4. Writes the chunks into that folder

Default limits (15 pages / 15 MB) match common AI-assistant upload caps.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pymupdf as fitz


DEFAULT_INPUT_DIR = "./pdfs"
DEFAULT_MAX_PAGES = 15
DEFAULT_MAX_MB = 15.0


def chunk_pdf(
    pdf_path: Path,
    out_root: Path,
    max_pages: int,
    max_bytes: int,
) -> int:
    """
    Split one PDF. Returns the number of chunks written.
    """
    stem = pdf_path.stem
    dest_dir = out_root / stem
    dest_dir.mkdir(parents=True, exist_ok=True)

    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        print(f"  ERROR opening {pdf_path.name}: {exc}")
        return 0

    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        return 0

    chunks_written = 0
    start = 0  # 0-based

    while start < total_pages:
        # Grow the chunk one page at a time until we would exceed limits
        end = start  # exclusive end in the loop below
        while end < total_pages and (end - start) < max_pages:
            # Probe: would adding page `end` keep us under max_bytes?
            probe = fitz.open()
            probe.insert_pdf(doc, from_page=start, to_page=end)
            size = len(probe.tobytes(deflate=True, garbage=3))
            probe.close()

            if size > max_bytes and end > start:
                # last successful size was end-1; stop growing
                break
            end += 1
            if size > max_bytes:
                # single page already over limit – still emit it
                break

        # end is exclusive; write pages start .. end-1
        if end <= start:
            end = start + 1  # safety: always emit at least one page

        chunk = fitz.open()
        chunk.insert_pdf(doc, from_page=start, to_page=end - 1)

        # 1-based page numbers for the filename
        p_from = start + 1
        p_to = end
        name = f"{stem}_p{p_from:03d}-{p_to:03d}.pdf"
        out_path = dest_dir / name
        chunk.save(out_path, deflate=True, garbage=3)
        chunk.close()

        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"  → {name}  ({p_to - start} pp, {size_mb:.1f} MB)")
        chunks_written += 1
        start = end

    doc.close()
    return chunks_written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Split PDFs into ≤N-page / ≤M-MB chunks for AI uploads.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--input-dir", "-i",
        default=DEFAULT_INPUT_DIR,
        help="Folder containing source PDFs",
    )
    p.add_argument(
        "--output-dir", "-o",
        default=None,
        help="Root folder for per-document subfolders (default: same as input)",
    )
    p.add_argument(
        "--max-pages", "-p",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help="Maximum pages per chunk",
    )
    p.add_argument(
        "--max-mb", "-m",
        type=float,
        default=DEFAULT_MAX_MB,
        help="Maximum size per chunk in megabytes",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    max_bytes = int(args.max_mb * 1024 * 1024)

    if not input_dir.is_dir():
        print(f"Input directory not found: {input_dir}", file=sys.stderr)
        return 1

    pdfs = sorted(input_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {input_dir}")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    total_chunks = 0

    for pdf in pdfs:
        print(f"Chunking {pdf.name} …")
        n = chunk_pdf(pdf, output_dir, args.max_pages, max_bytes)
        total_chunks += n

    print(f"\nDone. {total_chunks} chunk(s) written under {output_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
