"""Contract registry: loads the JSON Schemas in `contracts/schemas/` and validates documents against them.

A document names its contract in the top-level `schema` field (e.g. `wgc/logic@0`). Cross-file `$ref`s
are resolved through a `referencing` registry, so no network access is needed.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "contracts" / "schemas"
BASE_URI = "https://wargame-compiler.local/schemas/"

# document `schema` value → schema file
CONTRACTS = {
    "wgc/desktop@0": "desktop.schema.json",
    "wgc/source@0": "source.schema.json",
    "wgc/logic@0": "logic.schema.json",
    "wgc/digital@0": "digital.schema.json",
    "wgc/gate@0": "gate.schema.json",
    "wgc/outputs@0": "outputs.schema.json",
    "wgc/proposal@0": "proposal.schema.json",
    "glu/exec@0": "glu.schema.json",
    # Wire protocol of the inference node. Registered here only so the shared loader and contract tests cover it;
    # WGC has no knowledge of inference infrastructure, and `igw` loads the same file without importing `wgc` (ADR-0016).
    "igw/api@0": "inference.schema.json",
}


@lru_cache(maxsize=1)
def registry() -> Registry:
    resources = []
    for f in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = json.loads(f.read_text(encoding="utf-8"))
        resources.append((BASE_URI + f.name, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def schema_for(contract: str) -> dict:
    if contract not in CONTRACTS:
        raise KeyError(f"unknown contract {contract!r}; known: {', '.join(sorted(CONTRACTS))}")
    return registry().contents(BASE_URI + CONTRACTS[contract])


def validator(contract: str) -> Draft202012Validator:
    return Draft202012Validator(schema_for(contract), registry=registry())


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def errors(doc: dict) -> list[str]:
    """Schema errors of one document (empty list = valid)."""
    contract = doc.get("schema") if isinstance(doc, dict) else None
    if not contract:
        return ["document has no top-level `schema` field"]
    out = []
    for e in sorted(validator(contract).iter_errors(doc), key=lambda e: list(e.absolute_path)):
        loc = "/".join(map(str, e.absolute_path)) or "<root>"
        out.append(f"{loc}: {e.message[:300]}")
    return out
