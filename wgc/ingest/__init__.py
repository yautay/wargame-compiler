"""Deterministic source extractors (Stage 0, docs/DATA-CONTRACTS.md §9).

An extractor is a pure function: document bytes in, an ordered list of `Segment` out, no I/O. `wgc.source` turns
segments into inventory records (`SEG-<seg_prefix>.<key>`) and writes their text to `.glu/source/`. The registry maps
a file extension to the extractor name (recorded in `source_document.extractor`) and its function.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath
from typing import Callable


class IngestError(ValueError):
    """The document cannot be segmented deterministically (message in Polish)."""


@dataclass(frozen=True)
class Segment:
    key: str                 # label as printed ("3.4") or "u<n>" for the n-th unlabeled segment
    label: str | None
    segment_type: str
    text: str                # extracted text, before `wgc.canonical.normalize_text`
    parent_key: str | None
    order: int               # 1-based position in document order
    # Layout, for paged formats only (PDF): "3" or "3-4"; [x0, top, x1, bottom] on the first page; contract flags.
    pages: str | None = None
    bbox: tuple[float, float, float, float] | None = None
    visual_flags: tuple[str, ...] = ()


Extractor = Callable[[bytes], list[Segment]]


def _registry() -> dict[str, tuple[str, Extractor]]:
    from wgc.ingest import markdown, pdf
    return {".md": (markdown.NAME, markdown.extract), ".markdown": (markdown.NAME, markdown.extract),
            ".pdf": (pdf.NAME, pdf.extract)}


def extractor_for(path: str | PurePath) -> tuple[str, Extractor] | None:
    """(extractor name, function) for a document path, or None when no extractor handles its extension."""
    return _registry().get(PurePath(path).suffix.lower())
