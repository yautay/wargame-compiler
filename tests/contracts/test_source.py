"""Oracles from the source proposal; fixtures are static, synthetic and public."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from wgc.contracts.source import (
    ContractError, aspect_hash, canonical_bytes, content_hash, load_json,
    seal_record, storage_name, validate_bundle,
)

FIXTURES = Path(__file__).parent / "fixtures"
CATALOG = json.loads((FIXTURES / "catalog.json").read_text())


@pytest.mark.parametrize("case", CATALOG["cases"], ids=lambda c: c["file"])
def test_independently_specified_contract_cases(case):
    assert case["expectation"] and case["basis"]
    bundle = load_json(FIXTURES / case["file"])
    if not case["valid"]:
        with pytest.raises(ContractError, match=case["error_contains"]):
            validate_bundle(bundle)
        return
    report = validate_bundle(bundle)
    assert report["semantic_acceptance_granted"] is False
    expected = case["report"]
    if "execution" in expected:
        assert report["executable"]["status"] == expected["execution"]
    if "review_freshness" in expected:
        assert report["reviews"][0]["freshness"] == expected["review_freshness"]
    if "transcription_represented" in expected:
        assert report["coverage_inventory_region_counts"]["transcription"]["represented"] == expected["transcription_represented"]
    if "transcription_excluded" in expected:
        assert report["coverage_inventory_region_counts"]["transcription"]["excluded"] == expected["transcription_excluded"]


def test_canonicalization_has_an_independent_byte_oracle():
    # WGC-C14N-1 explicitly orders keys by Unicode scalar and retains arrays/text.
    value = {"z": [2, 1], "é": "e\u0301", "a": "line\n"}
    expected = '{"a":"line\\n","z":[2,1],"é":"é"}'.encode("utf-8")
    assert canonical_bytes(value) == expected
    assert hashlib.sha256(canonical_bytes(value)).hexdigest() == "65f5ea322f3e8f6bd8f04b3b765ecd3ed4b552ff97e6f0f5b860d2d727e62f79"


def test_record_hash_excludes_exactly_the_two_derived_fields():
    record = {"id": "synthetic:test", "record_type": "node", "schema_version": "wgc-source-1",
              "run_id": "synthetic:run", "supersedes_refs": [], "lineage_refs": [],
              "data": {"aspects": []}, "revision_id": "ignored", "content_hash": "ignored"}
    # Independently serialized fixed bytes; no call to the hash helper as oracle.
    expected = b'{"data":{"aspects":[]},"id":"synthetic:test","lineage_refs":[],"record_type":"node","run_id":"synthetic:run","schema_version":"wgc-source-1","supersedes_refs":[]}'
    assert content_hash(record) == hashlib.sha256(expected).hexdigest()
    record["run_id"] = "synthetic:another-run"
    assert content_hash(record) != hashlib.sha256(expected).hexdigest()


@pytest.mark.parametrize("value", [1.0, float("nan"), "\ud800", {1: "non-string key"}])
def test_noncanonical_programmatic_values_are_rejected(value):
    with pytest.raises(ContractError):
        canonical_bytes(value)


@pytest.mark.parametrize("raw", ['{"a":1,"a":2}', '{"x":0.1}', '{"x":NaN}', '\ufeff{}', '{"x":"\\ud800"}'])
def test_strict_json_input(tmp_path, raw):
    path = tmp_path / "input.json"
    path.write_text(raw, encoding="utf-8")
    with pytest.raises(ContractError):
        value = load_json(path)
        canonical_bytes(value)


def test_anonymous_identity_survives_record_reordering_and_windows_encoding():
    bundle = load_json(FIXTURES / "valid-source.json")
    before = validate_bundle(bundle)
    bundle["records"].reverse()
    assert validate_bundle(bundle) == before
    registry = next(r for r in bundle["records"] if r["record_type"] == "identity_registry")
    assert registry["data"]["entries"][0]["id"] == "synthetic:clause"
    filename = storage_name("synthetic:clause")
    assert filename == "id-73796e7468657469633a636c61757365.json"
    assert storage_name("synthetic:clause") != storage_name("synthetic/clause")


def test_every_required_mechanism_has_named_source_fields_and_addressable_examples():
    bundle = load_json(FIXTURES / "valid-source.json")
    descriptions = {r["data"]["description"]["kind"]: r["data"]["description"]
                    for r in bundle["records"] if r["record_type"] == "node"}
    # Expectations come from IG-MECHANICS-PROFILES, not schema introspection.
    required = {
        "state_variable": ["value_type", "unit", "bounds", "reset"],
        "history": ["prior_positions", "attempts", "paid_costs"],
        "event_type": ["cause_filter", "read_moment", "ordered_writes"],
        "parameter": ["unit", "comparison_operator", "temporal_bounds"],
        "choice": ["binding_id", "lifetime", "reselection_policy"],
        "reaction": ["trigger", "attempt_limit", "surviving_effects_costs_history"],
        "continuation": ["invocation_frame", "local_environment", "return_point"],
        "cost": ["attempt_or_success", "payment_checkpoint", "pay_once_key"],
        "geometry": ["map", "occupied_hexes", "anchor", "orientation", "off_map_zones"],
        "spatial_policy": ["metric", "path_quantifier", "optimality"],
        "table": ["axes", "cells", "notes", "legend", "participant_bindings"],
        "randomizer": ["physical_symbols", "pool_multiplicities_or_instances", "replacement", "draw_identity"],
        "visibility": ["domains", "rejected_choices", "reason_codes", "proof_paths", "cursor_metadata", "caches"],
        "calculation": ["rounding_stage", "rounding_method", "modifier_order"],
        "victory": ["checkpoint", "termination", "tie_rule", "control_history"],
    }
    for kind, fields in required.items():
        assert all(field in descriptions[kind] for field in fields)
        assert "payload" not in descriptions[kind]
    assert descriptions["choice"]["binding_id"]["value"]["text"] == "selected-copper-token"
    assert descriptions["choice"]["lifetime"]["value"]["text"] == "This procedure invocation."
    assert "multiplicity two" in descriptions["randomizer"]["pool_multiplicities_or_instances"]["value"]["text"]
    assert descriptions["parameter"]["unit"]["knowledge"] == "unknown"


def test_page_numbers_are_not_printed_labels_and_evidence_spans_pages():
    bundle = load_json(FIXTURES / "valid-source.json")
    evidence = next(r for r in bundle["records"] if r["record_type"] == "evidence")
    assert len(evidence["data"]["region_refs"]) == 2
    regions = [r for r in bundle["records"] if r["record_type"] == "region"]
    assert [(r["data"]["pdf_page"], r["data"]["printed_label"]) for r in regions] == [(1, "6"), (2, "7")]


def test_cross_section_exception_retains_source_direction():
    bundle = load_json(FIXTURES / "valid-cross-section-exception.json")
    link = next(r for r in bundle["records"] if r["id"] == "synthetic:cross-section-exception")
    assert link["data"]["relation_type"] == "exception"
    assert link["data"]["from_ref"]["id"] == "synthetic:exception-clause"
    assert link["data"]["target_ref"]["id"] == "synthetic:clause"
    assert link["data"]["requirement"] == "conditional"


def test_import_coverage_semantics_and_execution_are_independent():
    report = validate_bundle(load_json(FIXTURES / "valid-source.json"))
    assert report["import"]["status"] == "complete"
    assert report["coverage_inventory_region_counts"]["transcription"]["represented"] == 2
    assert report["coverage_inventory_region_counts"]["formal_semantics"]["represented"] == 0
    assert report["reviews"][0]["scope"] == "Only the lit-condition aspect; not the effect."
    assert report["reviews"][0]["authority_authenticated"] is False
    assert "synthetic:clause" in report["executable"]["source_blocker_ids"]
    assert report["executable"]["status"] == "blocked"


def test_schema_evaluator_fails_closed_on_unsupported_keywords(tmp_path):
    schema = tmp_path / "schema.json"
    schema.write_text('{"$defs":{},"unevaluatedProperties":false}')
    with pytest.raises(ContractError, match="unsupported schema keywords"):
        validate_bundle(load_json(FIXTURES / "valid-source.json"), schema)


@pytest.mark.parametrize("filename,exit_code", [("valid-source.json", 0), ("invalid-model-approval.json", 1)])
def test_cli_is_local_and_has_meaningful_exit_status(filename, exit_code):
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parents[2] / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([sys.executable, "-m", "wgc.contracts.source", str(FIXTURES / filename)],
                            env=env, text=True, capture_output=True, check=False)
    assert result.returncode == exit_code
    if exit_code == 0:
        assert json.loads(result.stdout)["structural_validation"] == "passed"
    else:
        assert "Invalid source IG" in result.stderr


def test_sealing_is_a_pure_hash_operation_not_acceptance():
    bundle = load_json(FIXTURES / "valid-source.json")
    original = next(r for r in bundle["records"] if r["record_type"] == "node")
    before = copy.deepcopy(original)
    sealed = seal_record(original)
    assert original == before
    assert sealed == before
    assert all(aspect_hash(a) == a["aspect_hash"] for a in sealed["data"]["aspects"])
