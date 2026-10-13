"""Offline source-IG structural validation and revision integrity checks.

This module does not evaluate rule descriptions or authorize gameplay. Its small
schema evaluator supports only the keywords used by the bundled source schema;
it rejects unsupported schema keywords rather than silently ignoring them.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "contracts/ig/source.schema.json"
SCHEMA_VERSION = "wgc-source-1"


class ContractError(ValueError):
    """Invalid source-contract bytes, shape or cross-record invariant."""


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _no_float(value: str) -> Any:
    raise ContractError(f"non-integer JSON number: {value}; use a rational")


def load_json(path: Path) -> Any:
    """Strict UTF-8 JSON; no duplicate keys, floats, BOM or nonfinite numbers."""
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                          parse_float=_no_float, parse_constant=_no_float)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ContractError(f"invalid UTF-8 JSON: {error}") from error


def canonical_bytes(value: Any) -> bytes:
    """WGC-C14N-1: integer-only JSON, scalar strings, ordered arrays, sorted keys."""
    def inspect(item: Any) -> None:
        if item is None or type(item) in (bool, int):
            return
        if isinstance(item, str):
            if any(0xD800 <= ord(char) <= 0xDFFF for char in item):
                raise ContractError("Unicode surrogate is not a scalar value")
            return
        if isinstance(item, list):
            for child in item:
                inspect(child)
            return
        if isinstance(item, dict) and all(isinstance(key, str) for key in item):
            for key, child in item.items():
                inspect(key)
                inspect(child)
            return
        raise ContractError("canonical content must contain only integer JSON values")
    inspect(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def content_hash(record: dict[str, Any]) -> str:
    body = {key: value for key, value in record.items()
            if key not in {"revision_id", "content_hash"}}
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def aspect_hash(aspect: dict[str, Any]) -> str:
    body = {key: value for key, value in aspect.items() if key != "aspect_hash"}
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def seal_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with computed hashes; does not validate or promote a record."""
    result = copy.deepcopy(record)
    if result.get("record_type") == "node":
        for aspect in result["data"]["aspects"]:
            aspect["aspect_hash"] = aspect_hash(aspect)
    result["content_hash"] = content_hash(result)
    result["revision_id"] = "sha256:" + result["content_hash"]
    return result


def storage_name(identity: str) -> str:
    """An injective Windows-safe filename, independent of identity semantics."""
    return "id-" + identity.encode("utf-8").hex() + ".json"


KEYWORDS = {"$schema", "$id", "title", "description", "$defs", "$ref", "type",
            "properties", "required", "additionalProperties", "const", "enum",
            "oneOf", "allOf", "if", "then", "items", "minItems", "minLength", "maxLength",
            "pattern", "minimum", "maximum"}


def _check_schema(schema: dict[str, Any], root: dict[str, Any]) -> None:
    if set(schema) - KEYWORDS:
        raise ContractError(f"unsupported schema keywords: {sorted(set(schema) - KEYWORDS)}")
    if "$ref" in schema:
        name = schema["$ref"]
        if not name.startswith("#/$defs/") or name[8:] not in root["$defs"]:
            raise ContractError("only existing local schema definitions are supported")
    for key in ("properties", "$defs"):
        for child in schema.get(key, {}).values():
            _check_schema(child, root)
    for key in ("oneOf", "allOf"):
        for child in schema.get(key, []):
            _check_schema(child, root)
    for key in ("items", "if", "then"):
        if key in schema:
            _check_schema(schema[key], root)


def _shape(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str) -> list[str]:
    errors = []
    if "$ref" in schema:
        errors += _shape(value, root["$defs"][schema["$ref"][8:]], root, path)
    if "oneOf" in schema:
        branches = [_shape(value, child, root, path) for child in schema["oneOf"]]
        if sum(not branch for branch in branches) != 1:
            closest = min(branches, key=len)
            errors.append(f"{path}: oneOf requires exactly one matching shape")
            errors += closest[:3]
    for child in schema.get("allOf", []):
        errors += _shape(value, child, root, path)
    if "if" in schema and not _shape(value, schema["if"], root, path):
        errors += _shape(value, schema.get("then", {}), root, path)
    # JSON equality must distinguish booleans from integers.
    same = lambda a, b: canonical_bytes(a) == canonical_bytes(b)
    if "const" in schema and not same(value, schema["const"]):
        errors.append(f"{path}: unexpected constant")
    if "enum" in schema and not any(same(value, choice) for choice in schema["enum"]):
        errors.append(f"{path}: unexpected enum value")
    kinds = {"object": isinstance(value, dict), "array": isinstance(value, list),
             "string": isinstance(value, str), "integer": type(value) is int,
             "boolean": type(value) is bool, "null": value is None}
    if "type" in schema and not kinds[schema["type"]]:
        return errors + [f"{path}: expected {schema['type']}"]
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key}")
        for key, child in value.items():
            if key in schema.get("properties", {}):
                errors += _shape(child, schema["properties"][key], root, f"{path}/{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if "items" in schema:
            for index, child in enumerate(value):
                errors += _shape(child, schema["items"], root, f"{path}/{index}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: string too long")
        if "pattern" in schema and not re.search(schema["pattern"], value, flags=re.ASCII):
            errors.append(f"{path}: invalid pattern")
    if type(value) is int:
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum")
    return errors


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def validate_bundle(bundle: dict[str, Any], schema_path: Path = SCHEMA_PATH) -> dict[str, Any]:
    """Check shapes, hashes, selected resolution and authority metadata.

    Review freshness is a structural comparison of pinned bases, not a truth or
    authority judgment. Unknown dependency completeness remains unknown.
    """
    canonical_bytes(bundle)
    schema = load_json(schema_path)
    _check_schema(schema, schema)
    errors = _shape(bundle, schema, schema, "$")
    if errors:
        raise ContractError("schema: " + "; ".join(errors[:8]))
    records = bundle["records"]
    store = {}
    identity_types = {}
    for record in records:
        key = (record["id"], record["revision_id"])
        if key in store:
            raise ContractError("duplicate identity/revision in revision store")
        if record["id"] in identity_types and identity_types[record["id"]] != record["record_type"]:
            raise ContractError("stable identity changed record type")
        identity_types[record["id"]] = record["record_type"]
        store[key] = record
        digest = content_hash(record)
        if digest != record["content_hash"] or record["revision_id"] != "sha256:" + digest:
            raise ContractError(f"revision hash mismatch: {record['id']}")
        if record["record_type"] == "node":
            seen = set()
            for aspect in record["data"]["aspects"]:
                if aspect["aspect_id"] in seen:
                    raise ContractError("duplicate stable aspect identity")
                seen.add(aspect["aspect_id"])
                if aspect_hash(aspect) != aspect["aspect_hash"]:
                    raise ContractError("changed aspect hash")

    snapshots = [r for r in records if r["id"] == bundle["snapshot_id"]]
    if len(snapshots) != 1 or snapshots[0]["record_type"] != "snapshot":
        raise ContractError("bundle must name exactly one snapshot revision")
    snapshot = snapshots[0]
    selected = {}
    for selection in snapshot["data"]["selected"]:
        if selection["id"] in selected:
            raise ContractError("duplicate identity in selected snapshot")
        record = store.get((selection["id"], selection["revision_id"]))
        if record is None or record["record_type"] != selection["record_type"] or record["content_hash"] != selection["content_hash"]:
            raise ContractError("selected revision/hash/type does not match store")
        if record["record_type"] == "snapshot":
            raise ContractError("snapshot selections cannot include snapshots")
        selected[selection["id"]] = record

    def resolve(reference: dict[str, Any], expected: str | None = None) -> dict[str, Any]:
        if reference["mode"] == "active":
            target = selected.get(reference["id"])
        else:
            target = store.get((reference["id"], reference["revision_id"]))
        if target is None:
            raise ContractError(f"dangling {reference['mode']} reference: {reference['id']}")
        if target["record_type"] != reference["record_type"] or (expected and target["record_type"] != expected):
            raise ContractError(f"typed reference mismatch: {reference['id']}")
        if "aspect_id" in reference:
            if target["record_type"] != "node" or not any(a["aspect_id"] == reference["aspect_id"] for a in target["data"]["aspects"]):
                raise ContractError("dangling stable aspect reference")
        return target

    def review_freshness(data: dict[str, Any]) -> str:
        stale = False
        for reference in [*data["targets"], *data["basis"]]:
            old = resolve(reference)
            current = selected.get(old["id"])
            if current is None:
                stale = True
            elif "aspect_id" in reference:
                old_aspect = next(a for a in old["data"]["aspects"] if a["aspect_id"] == reference["aspect_id"])
                current_aspect = next((a for a in current["data"]["aspects"] if a["aspect_id"] == reference["aspect_id"]), None)
                stale |= current_aspect is None or old_aspect["aspect_hash"] != current_aspect["aspect_hash"]
            else:
                stale |= old["revision_id"] != current["revision_id"]
        return "stale" if stale else ("current" if data["basis_completeness"] == "complete" else "unknown")

    # Historical edges always resolve in the immutable store. Active edges in old
    # unselected revisions belong to their original snapshots and are not activated.
    selected_keys = {(r["id"], r["revision_id"]) for r in selected.values()}
    for record in records:
        if identity_types.get(record["run_id"]) != "run":
            raise ContractError("run_id must identify a stored run")
        for item in _walk(record):
            if item.get("mode") == "historical":
                resolve(item)
        for previous in record["supersedes_refs"]:
            resolve(previous, record["record_type"])
            if previous["id"] != record["id"] or previous["revision_id"] == record["revision_id"]:
                raise ContractError("supersession requires a previous revision of the same identity")
        if record["record_type"] == "snapshot":
            manifest_ids = set()
            for entry in record["data"]["selected"]:
                if entry["id"] in manifest_ids:
                    raise ContractError("duplicate identity in selected snapshot")
                manifest_ids.add(entry["id"])
                target = store.get((entry["id"], entry["revision_id"]))
                if target is None or any(target[key] != entry[key] for key in ("record_type", "content_hash")):
                    raise ContractError("selected revision/hash/type does not match store")
                if target["record_type"] == "snapshot":
                    raise ContractError("snapshot selections cannot include snapshots")
    expected_ref_fields = {
        "gap_refs": "gap", "blocker_refs": "gap", "conflict_refs": "gap",
        "evidence_refs": "evidence", "coverage_refs": "coverage",
        "semantic_review_refs": "review", "supersedes_review_refs": "review",
        "region_refs": "region", "source_ref": "source", "region_ref": "region",
        "profile_ref": "profile", "inventory_ref": "node",
        "scope_decision_ref": "review", "informational_review_ref": "review",
        "material_refs": "source", "map_refs": "source", "counter_refs": "source",
    }
    for record in records:
        active_record = (record["id"], record["revision_id"]) in selected_keys or record is snapshot
        for item in _walk(record):
            if active_record and item.get("mode") == "active":
                resolve(item)
            for name, expected in expected_ref_fields.items():
                if name in item:
                    references = item[name] if isinstance(item[name], list) else [item[name]]
                    for reference in references:
                        if reference is not None:
                            if reference["record_type"] != expected:
                                raise ContractError(f"typed field reference mismatch: {name}")
                            if active_record or reference["mode"] == "historical":
                                resolve(reference, expected)
        data = record["data"]
        kind = record["record_type"]
        if kind == "region":
            loc = data["locator"]
            if (loc["kind"] == "box" and (loc["x0"] >= loc["x1"] or loc["y0"] >= loc["y1"])) or (loc["kind"] == "offset" and loc["start"] >= loc["end"]):
                raise ContractError("empty or inverted region locator")
        elif kind == "node":
            aspects = {a["aspect_id"]: a for a in data["aspects"]}
            groups = set()
            for group in data["semantic_groups"]:
                if group["group_id"] in groups:
                    raise ContractError("duplicate semantic group identity")
                groups.add(group["group_id"])
                if not group["effects"]:
                    raise ContractError("semantic group needs an effect")
                for role, facet in [("conditions", "condition"), ("effects", "effect"), ("exceptions", "exception"), ("timing", "timing")]:
                    if len(group[role]) != len(set(group[role])):
                        raise ContractError("duplicate semantic group member")
                    if any(member not in aspects or aspects[member]["facet"] != facet for member in group[role]):
                        raise ContractError("semantic group member has wrong aspect/facet")
            for aspect in aspects.values():
                value = aspect["statement"]["value"]
                if value and value["kind"] == "opaque" and aspect["normative"] and aspect["execution_impact"] != "blocking":
                    raise ContractError("opaque normative aspect requires execution blocker")
                if aspect["statement"]["knowledge"] == "unknown" and aspect["normative"] and aspect["execution_impact"] != "blocking":
                    raise ContractError("unknown normative aspect requires execution blocker")
                review_ref = aspect["informational_review_ref"]
                if aspect["normative"] and aspect["execution_impact"] == "informational" and active_record:
                    if review_ref is None:
                        raise ContractError("informational normative aspect needs a reviewed rationale")
                    review = resolve(review_ref, "review")["data"]
                    if review["decision"] != "accepted" or review_freshness(review) != "current" or not any(t["id"] == record["id"] and t.get("aspect_id") == aspect["aspect_id"] for t in review["targets"]):
                        raise ContractError("informational rationale does not accept this aspect")
            description = data["description"]
            if description["kind"] == "table":
                axis_ids = [a["axis_id"] for a in description["axes"]]
                cell_ids = [c["cell_id"] for c in description["cells"]]
                note_ids = [n["note_id"] for n in description["notes"]]
                orders = [a["order"] for a in description["axes"]]
                if any(len(values) != len(set(values)) for values in [axis_ids, cell_ids, note_ids, orders]):
                    raise ContractError("duplicate table address/order")
                for cell in description["cells"]:
                    if any(a not in axis_ids for a in cell["axis_members"]) or any(c not in cell_ids for c in cell["merged_members"]):
                        raise ContractError("dangling table axis/merged cell")
                    coordinate_ids = [c["axis_id"] for c in cell["coordinates"]]
                    if len(coordinate_ids) != len(set(coordinate_ids)) or set(coordinate_ids) != set(cell["axis_members"]):
                        raise ContractError("table coordinates do not match participating axes")
                for note in description["notes"]:
                    if not note["axis_ids"] and not note["cell_ids"]:
                        raise ContractError("table note requires explicit scope")
                    if any(a not in axis_ids for a in note["axis_ids"]) or any(c not in cell_ids for c in note["cell_ids"]):
                        raise ContractError("dangling table note scope")
        elif kind == "coverage":
            if data["status"] == "represented" and data["gap_refs"]:
                raise ContractError("represented coverage cannot count gaps")
            if data["status"] == "excluded" and active_record:
                review = resolve(data["scope_decision_ref"], "review")["data"]
                if review["decision"] != "accepted" or review_freshness(review) != "current":
                    raise ContractError("coverage exclusion needs an accepted scope decision")
        elif kind == "identity_registry":
            keys = set()
            for entry in data["entries"]:
                if entry["origin_key"] in keys:
                    raise ContractError("duplicate identity registry origin key")
                keys.add(entry["origin_key"])
                if entry["status"] == "assigned" and entry["id"] not in identity_types:
                    raise ContractError("registry identity is not stored")
                if entry["status"] == "ambiguous" and not entry["gap_refs"]:
                    raise ContractError("ambiguous identity needs a gap")
        elif kind == "origin_binding":
            path = data["relative_path"]
            if "\\" in path or ":" in path or path.startswith("/") or any(p in ("", ".", "..") for p in path.split("/")):
                raise ContractError("origin binding requires a safe relative POSIX path")

    # A coverage denominator is an inventory partition, never overlapping context.
    coverage_keys = set()
    boxes = {}
    coverage = {level: {status: 0 for status in ("represented", "partial", "unprocessed", "excluded")}
                for level in ("transcription", "descriptive_semantics", "formal_semantics")}
    for record in selected.values():
        if record["record_type"] != "coverage":
            continue
        data = record["data"]
        if data["denominator_role"] == "context":
            continue
        region = resolve(data["region_ref"], "region")
        key = (data["level"], region["id"], region["revision_id"])
        if key in coverage_keys:
            raise ContractError("duplicate coverage denominator region/level")
        coverage_keys.add(key)
        rd = region["data"]
        loc = rd["locator"]
        source_key = (data["level"], rd["source_ref"]["id"], rd["source_ref"]["revision_id"], rd["pdf_page"], loc["kind"])
        for previous in boxes.get(source_key, []):
            if loc["kind"] == "box":
                overlap = max(loc["x0"], previous["x0"]) < min(loc["x1"], previous["x1"]) and max(loc["y0"], previous["y0"]) < min(loc["y1"], previous["y1"])
            else:
                overlap = loc["text_sha256"] == previous["text_sha256"] and max(loc["start"], previous["start"]) < min(loc["end"], previous["end"])
            if overlap:
                raise ContractError("overlapping coverage denominator regions")
        boxes.setdefault(source_key, []).append(loc)
        coverage[data["level"]][data["status"]] += 1

    reviews = []
    for record in selected.values():
        if record["record_type"] != "review":
            continue
        data = record["data"]
        freshness = review_freshness(data)
        reviews.append({"id": record["id"], "decision": data["decision"], "kind": data["kind"],
                        "actor_role": data["actor_role"], "freshness": freshness,
                        "scope": data["scope"], "authority_authenticated": False})
    blockers = set()
    for record in selected.values():
        if record["record_type"] == "gap" and "execution" in record["data"]["blocked_operations"]:
            blockers.add(record["id"])
        if record["record_type"] == "node":
            if any(item.get("kind") == "opaque" or item.get("knowledge") == "unknown" for item in _walk(record["data"])) or any(a["execution_impact"] == "blocking" for a in record["data"]["aspects"]):
                blockers.add(record["id"])
        if record["record_type"] == "relation" and record["data"]["requirement"] != "informational":
            if record["data"]["target_status"] != "resolved" or record["data"]["applicability"]["knowledge"] == "unknown":
                blockers.add(record["id"])
    assessments = snapshot["data"]["assessments"]
    return {"structural_validation": "passed", "snapshot_id": snapshot["id"],
            "import": assessments["import"], "coverage_inventory_region_counts": coverage,
            "reviews": sorted(reviews, key=lambda r: r["id"]),
            "executable": {"status": "blocked" if blockers else assessments["executable"]["status"],
                           "source_blocker_ids": sorted(blockers),
                           "reason": assessments["executable"]["reason"]},
            "semantic_acceptance_granted": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    try:
        report = validate_bundle(load_json(args.bundle))
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    except (ContractError, OSError) as error:
        print(f"Invalid source IG: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
