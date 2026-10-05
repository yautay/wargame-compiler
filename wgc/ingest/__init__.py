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


Extractor = Callable[[bytes], list[Segment]]


def _registry() -> dict[str, tuple[str, Extractor]]:
    from wgc.ingest import markdown
    return {".md": (markdown.NAME, markdown.extract), ".markdown": (markdown.NAME, markdown.extract)}


def extractor_for(path: str | PurePath) -> tuple[str, Extractor] | None:
    """(extractor name, function) for a document path, or None when no extractor handles its extension."""
    return _registry().get(PurePath(path).suffix.lower())
