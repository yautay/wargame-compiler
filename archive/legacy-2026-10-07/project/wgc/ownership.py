"""Persistent output sets of task families and logical input scopes (ADR-0035).

One manifest per owner lives in kb/outputs/. It is committed in the same KB batch as the records it owns.
`retired` is a tombstone history; retired records are absent from canonical KB. The manifest survives loss of .glu/.
"""
from __future__ import annotations

from pathlib import Path

from wgc.canonical import content_hash
from wgc.tasks import Inputs, TaskSpec

SCHEMA = "wgc/outputs@0"


def owner(ws, spec: TaskSpec, inputs: Inputs) -> dict:
    scope = spec.ownership_scope(ws, inputs) if spec.ownership_scope else tuple(sorted(inputs))
    if not scope or len(set(scope)) != len(scope) or not all(isinstance(i, str) for i in scope):
        raise ValueError(f"Niepoprawny zakres ownership zadania {spec.name}: {scope!r}.")
    return {"task": spec.id, "scope": list(scope)}


def path(root: str | Path, task: str, scope: tuple[str, ...]) -> Path:
    key = content_hash({"task": task, "scope": list(scope)}).removeprefix("sha256:")
    return Path(root) / "kb" / "outputs" / f"{key}.yaml"


def exists(root: str | Path, task: str, scope: tuple[str, ...]) -> bool:
    return path(root, task, scope).is_file()
