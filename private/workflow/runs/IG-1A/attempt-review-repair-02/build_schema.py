"""One-time schema construction for the IG-1A delivery (not a product API)."""
import json
from pathlib import Path


def obj(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}


def arr(items, minimum=0):
    return {"type": "array", "items": items, "minItems": minimum}


def enum(*values):
    return {"enum": list(values)}


def ref(name):
    return {"$ref": f"#/$defs/{name}"}


text = {"type": "string", "minLength": 1}
nullable_text = {"oneOf": [text, {"type": "null"}]}
integer = {"type": "integer", "minimum": 0}
positive = {"type": "integer", "minimum": 1}
sha = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
identity = {"type": "string", "maxLength": 100, "pattern": "^[a-z][a-z0-9_.-]*:[A-Za-z0-9][A-Za-z0-9_.:/-]*$(?![\\s\\S])"}
aspect_id = {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_.-]*$(?![\\s\\S])"}
revision = {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"}
types = ["source", "region", "evidence", "node", "relation", "gap", "origin_binding",
         "coverage", "profile", "run", "review", "snapshot", "identity_registry"]
defs = {}
active_props = {"mode": {"const": "active"}, "id": identity,
                "record_type": enum(*types), "aspect_id": aspect_id}
historical_props = {**active_props, "mode": {"const": "historical"}, "revision_id": revision}
defs["active_ref"] = obj(active_props, ["mode", "id", "record_type"])
defs["historical_ref"] = obj(historical_props, ["mode", "id", "record_type", "revision_id"])
defs["whole_historical_ref"] = obj({k: v for k, v in historical_props.items() if k != "aspect_id"},
                                    ["mode", "id", "record_type", "revision_id"])
defs["ref"] = {"oneOf": [ref("active_ref"), ref("historical_ref")]}
defs["content_ref"] = {"allOf": [ref("ref"), {"properties": {
    "record_type": enum("node", "evidence", "relation")}}]}
refs = arr(ref("ref"))
active_refs = arr(ref("active_ref"))
history_refs = arr(ref("historical_ref"))
defs["value"] = {"oneOf": [
    obj({"kind": {"const": "text"}, "text": text}),
    obj({"kind": {"const": "symbol"}, "symbol": text, "legend_refs": refs}),
    obj({"kind": {"const": "quantity"}, "amount": {"type": "integer"}, "unit": text}),
    obj({"kind": {"const": "rational"}, "numerator": {"type": "integer"},
         "denominator": positive, "unit": text}),
    obj({"kind": {"const": "reference"}, "target": ref("ref")}),
    obj({"kind": {"const": "opaque"}, "text": text, "execution_limitation": text})]}
statement_props = {"knowledge": enum("known", "established_absent", "unknown", "not_applicable"),
                   "representation": enum("literal", "normalized", "interpreted"),
                   "value": {"oneOf": [ref("value"), {"type": "null"}]},
                   "reason": nullable_text, "gap_refs": refs,
                   "evidence_refs": refs, "scope_refs": refs}
defs["statement"] = obj(statement_props)
defs["statement"]["allOf"] = [
    {"if": {"properties": {"knowledge": {"const": "known"}}},
     "then": {"properties": {"value": ref("value"), "evidence_refs": arr(ref("ref"), 1)}}},
    {"if": {"properties": {"knowledge": {"const": "unknown"}}},
     "then": {"properties": {"value": {"type": "null"}, "reason": text,
                             "gap_refs": arr(ref("ref"), 1)}}},
    {"if": {"properties": {"knowledge": {"const": "not_applicable"}}},
     "then": {"properties": {"value": {"type": "null"}, "reason": text}}},
    {"if": {"properties": {"knowledge": {"const": "established_absent"}}},
     "then": {"properties": {"value": {"type": "null"}, "reason": text,
                             "scope_refs": arr(ref("ref"), 1), "evidence_refs": arr(ref("ref"), 1)}}}]
statement = ref("statement")
facets = ["transcription", "condition", "effect", "parameter", "exception", "timing", "scope",
          "definition", "permission", "obligation", "prohibition", "trigger", "cost", "choice",
          "calculation", "transition", "duration", "aggregation", "visibility", "victory"]
defs["aspect"] = obj({"aspect_id": aspect_id, "aspect_hash": sha, "facet": enum(*facets),
                      "statement": statement, "normative": {"type": "boolean"},
                      "execution_impact": enum("formal", "informational", "blocking"),
                      "informational_review_ref": {"oneOf": [ref("ref"), {"type": "null"}]}})
defs["group"] = obj({"group_id": aspect_id, "operator": enum("all", "any", "sequence"),
                     "conditions": arr(aspect_id), "effects": arr(aspect_id),
                     "exceptions": arr(aspect_id), "timing": arr(aspect_id)})

# Fields are source descriptions with independent knowledge/evidence, not expressions.
mechanics = {
 "state_variable": ["value_type", "unit", "owner", "bounds", "reset"],
 "resource": ["unit", "owner", "pool_composition", "reset"],
 "event_type": ["cause_filter", "attempt_commit_invalidation", "read_moment", "ordered_writes", "limits", "reset_window"],
 "history": ["prior_positions", "first_occurrence", "attempts", "counters", "used_participants", "paid_costs"],
 "parameter": ["value_type", "unit", "domain", "comparison_operator", "temporal_bounds"],
 "action": ["actor", "guard", "parameters", "permission", "obligation", "prohibition", "effects"],
 "procedure": ["actor", "guard", "inputs", "outputs", "branches", "loops", "termination", "failure", "reaction_windows"],
 "step": ["actor", "guard", "ordered_writes", "completion", "failure"],
 "timing_window": ["instance_hierarchy", "opening", "closing", "counter_scope", "priority", "tie_breaker"],
 "reaction": ["trigger", "eligible_player", "opening", "closing", "attempt_limit", "resume_replace_cancel_restart", "surviving_effects_costs_history"],
 "continuation": ["invocation_frame", "local_environment", "return_point", "resume_policy"],
 "choice": ["owner", "selection_mode", "selector", "cardinality", "constraints", "binding_id", "lifetime", "reselection_policy", "eligible_selected_committed_participating_affected"],
 "selector": ["set", "filter", "binding_refs"],
 "cost": ["payer", "resource", "amount", "attempt_or_success", "payment_checkpoint", "pay_once_key", "cancellation_survival"],
 "geometry": ["map", "sheet", "hex_label", "occupied_hexes", "anchor", "orientation", "relative_zones", "pivot_policy", "hex_edge_terrain", "elevation", "infrastructure", "off_map_zones", "stack_constraints"],
 "spatial_policy": ["policy_kind", "metric", "endpoints", "rounding", "admissible_nodes_edges", "cost", "exceptions", "path_quantifier", "optimality", "tie_selection"],
 "calculation": ["ordered_operations", "unit", "comparison_operator", "rounding_stage", "rounding_method", "rounding_beneficiary", "modifier_order", "stacking"],
 "aggregation": ["set", "filter", "measure", "operator", "unit", "modifier_order"],
 "loss_allocation": ["deciding_player", "targets", "proportions", "overflow", "elimination_timing"],
 "duration": ["start", "expiry", "checkpoint", "snapshot_reads", "refresh"],
 "randomizer": ["physical_symbols", "symbol_meaning", "draw_count", "combination", "independence", "replacement", "pool_multiplicities_or_instances", "raw_modified_result", "draw_identity", "reroll_policy", "shared_targets"],
 "visibility": ["viewer", "state", "domains", "rejected_choices", "reason_codes", "proof_paths", "gaps", "identifiers", "cursor_metadata", "caches", "legal_attempts", "reveal_checkpoint"],
 "outcome": ["original_symbols", "ordered_conditional_effects", "triggered_procedures"],
 "victory": ["metric", "counted_set", "checkpoint", "comparison", "termination", "tie_rule", "control_history"]}
node_variants = []
for kind, fields in mechanics.items():
    node_variants.append(obj({"kind": {"const": kind}, **{f: statement for f in fields}}))
node_variants += [obj({"kind": {"const": kind}, "description": statement})
                  for kind in ["section", "clause", "concept", "diagram", "component"]]
node_variants.append(obj({"kind": {"const": "table"},
    "axes": arr(obj({"axis_id": aspect_id, "order": integer, "unit": statement,
                     "boundaries": statement}), 1),
    "cells": arr(obj({"cell_id": aspect_id, "axis_members": arr(aspect_id, 1),
                      "coordinates": arr(obj({"axis_id": aspect_id, "position": statement}), 1),
                      "value": statement, "merged_members": arr(aspect_id)})),
    "notes": arr(obj({"note_id": aspect_id, "cell_ids": arr(aspect_id),
                      "axis_ids": arr(aspect_id), "statement": statement})),
    **{f: statement for f in ["out_of_range", "missing_cell", "decorations", "legend", "participant_bindings"]}}))
defs["node_description"] = {"oneOf": node_variants}
data = {}
data["source"] = obj({"role": enum("rulebook", "errata", "faq", "scenario", "map", "counter_sheet", "player_aid", "other"),
 "publisher": text, "system": text, "edition": text, "language": text, "part": text,
 "media_type": text, "byte_count": {"oneOf": [integer, {"type": "null"}]},
 "sha256": {"oneOf": [sha, {"type": "null"}]},
 "availability": enum("available", "missing", "unreadable"),
 "compatibility": statement, "gap_refs": refs})
data["source"]["allOf"] = [
 {"if": {"properties": {"availability": {"const": "available"}}},
  "then": {"properties": {"byte_count": integer, "sha256": sha}}},
 {"if": {"properties": {"availability": enum("missing", "unreadable")}},
  "then": {"properties": {"gap_refs": arr(ref("ref"), 1)}}}]
data["region"] = obj({"source_ref": ref("historical_ref"), "pdf_page": positive,
 "printed_label": nullable_text, "reading_order": integer,
 "locator": {"oneOf": [
   obj({"kind": {"const": "box"}, "coordinate_convention": {"const": "normalized-top-left"},
        "x0": {"type": "integer", "minimum": 0, "maximum": 1000000},
        "y0": {"type": "integer", "minimum": 0, "maximum": 1000000},
        "x1": {"type": "integer", "minimum": 0, "maximum": 1000000},
        "y1": {"type": "integer", "minimum": 0, "maximum": 1000000}}),
   obj({"kind": {"const": "offset"}, "offset_convention": {"const": "unicode-codepoint-half-open"},
        "start": integer, "end": integer, "text_sha256": sha})]}})
data["evidence"] = obj({"region_refs": arr(ref("historical_ref"), 1),
 "role": enum("direct", "context", "counterevidence"), "literal_text": text,
 "normalized_text": nullable_text, "uncertain_symbols": arr(text)})
data["node"] = obj({"title": text, "editorial_parent_ref": {"oneOf": [ref("ref"), {"type": "null"}]},
 "aspects": arr(ref("aspect")), "semantic_groups": arr(ref("group")), "description": ref("node_description")})
relations = ["mention", "procedure_use", "table_use", "definition", "condition", "exception", "modifies",
 "applies_to", "illustrates", "precedes", "continuation", "reads", "writes", "triggers", "schedules",
 "resumes", "constrains", "uses_binding"]
data["relation"] = obj({"relation_type": enum(*relations), "from_ref": ref("ref"),
 "target_status": enum("resolved", "unresolved", "ambiguous", "unsupported"),
 "target_ref": {"oneOf": [ref("ref"), {"type": "null"}]},
 "raw_locator": nullable_text, "edition": text, "candidate_refs": refs, "gap_refs": refs,
 "applicability": statement, "evidence_refs": refs,
 "requirement": enum("required", "conditional", "informational"),
 "requirement_group": obj({"group_id": aspect_id, "operator": enum("all", "any")})})
data["relation"]["allOf"] = [
 {"if": {"properties": {"target_status": {"const": "resolved"}}}, "then": {"properties": {"target_ref": ref("ref")}}},
 {"if": {"properties": {"target_status": enum("unresolved", "ambiguous", "unsupported")}},
  "then": {"properties": {"target_ref": {"type": "null"}, "raw_locator": text, "gap_refs": arr(ref("ref"), 1)}}}]
data["gap"] = obj({"kind": enum("missing_source", "unreadable", "unprocessed", "ambiguity", "conflict", "unsupported_interpretation"),
 "reason": text, "affected_refs": refs, "blocked_operations": arr(enum("source_verification", "transcription", "semantic_acceptance", "formalization", "execution"), 1), "candidate_refs": refs})
data["origin_binding"] = obj({"input_snapshot_id": identity, "input_sha256": sha,
 "relative_path": text, "field_locator": text, "ig_refs": arr(ref("ref"), 1),
 "external_namespace": text, "external_id": nullable_text, "mapping_status": enum("exact", "partial", "conflict", "unprocessed")})
data["coverage"] = obj({"inventory_ref": ref("whole_historical_ref"), "region_ref": ref("historical_ref"),
 "level": enum("transcription", "descriptive_semantics", "formal_semantics"),
 "status": enum("represented", "partial", "unprocessed", "excluded"),
 "target_refs": arr(ref("content_ref")), "gap_refs": refs, "denominator_role": enum("inventory", "context"),
 "exclusion_reason": nullable_text, "scope_decision_ref": {"oneOf": [ref("historical_ref"), {"type": "null"}]}})
data["coverage"]["allOf"] = [
 {"if": {"properties": {"status": {"const": "represented"}}}, "then": {"properties": {"target_refs": arr(ref("content_ref"), 1)}}},
 {"if": {"properties": {"status": enum("partial", "unprocessed")}}, "then": {"properties": {"gap_refs": arr(ref("ref"), 1)}}},
 {"if": {"properties": {"status": {"const": "excluded"}}}, "then": {"properties": {"exclusion_reason": text, "scope_decision_ref": ref("historical_ref")}}}]
data["profile"] = obj({"system": text, "edition": text, "rules_mode": text,
 "options": arr(statement), "scenario": statement, "map_refs": refs, "counter_refs": refs,
 "material_refs": history_refs, "compatibility_decisions": arr(statement)})
data["run"] = obj({"context_manifest_sha256": sha, "raw_proposal_sha256": {"oneOf": [sha, {"type": "null"}]},
 "model": nullable_text, "reasoning": nullable_text, "configuration_evidence": text,
 "started_utc": text, "ended_utc": nullable_text,
 "measurements": obj({"wall_milliseconds": {"oneOf": [integer, {"type": "null"}]},
 "input_tokens": {"oneOf": [integer, {"type": "null"}]}, "output_tokens": {"oneOf": [integer, {"type": "null"}]}, "unknown_reason": nullable_text}),
 "expectation_basis": text})
data["review"] = obj({"kind": enum("transcription", "interpretation", "source_composition", "situation_outcome", "technical"),
 "actor": text, "actor_role": enum("human_owner", "human_reviewer", "model", "validator"),
 "authorization": nullable_text, "decision": enum("accepted", "rejected", "observation"),
 "decision_artifact": nullable_text, "targets": arr(ref("historical_ref"), 1), "basis": history_refs,
 "basis_completeness": enum("complete", "partial", "unknown"), "scope": text,
 "rationale": text, "supersedes_review_refs": history_refs})
data["review"]["properties"]["coverage_boundary"] = obj({
 "purpose": {"const": "coverage_exclusion"}, "inventory_ref": ref("whole_historical_ref"),
 "region_ref": ref("historical_ref"),
 "level": enum("transcription", "descriptive_semantics", "formal_semantics")})
data["review"]["allOf"] = [
 {"if": {"properties": {"decision": {"const": "accepted"}}},
  "then": {"properties": {"actor_role": enum("human_owner", "human_reviewer"),
                            "authorization": text, "decision_artifact": text}}},
 {"if": {"properties": {"basis_completeness": {"const": "complete"}}},
  "then": {"properties": {"basis": arr(ref("historical_ref"), 1)}}}]
selection = obj({"id": identity, "record_type": enum(*types), "revision_id": revision, "content_hash": sha})
data["snapshot"] = obj({"state": enum("draft", "sealed"), "selected": arr(selection, 1),
 "profile_ref": ref("active_ref"), "conflict_refs": refs,
 "assessments": obj({
   "import": obj({"status": enum("unassessed", "partial", "complete"), "basis_refs": refs}),
   "coverage_refs": active_refs,
   "semantic_review_refs": active_refs,
   "executable": obj({"status": enum("unassessed", "blocked"), "scope_refs": active_refs,
                       "blocker_refs": refs, "reason": text})})})
data["identity_registry"] = obj({"entries": arr(obj({"origin_key": text, "id": identity,
 "status": enum("assigned", "ambiguous"), "candidate_ids": arr(identity), "gap_refs": refs}))})
record_variants = []
for kind in types:
 defs[f"{kind}_data"] = data[kind]
 record_variants.append(obj({"id": identity, "record_type": {"const": kind},
  "schema_version": {"const": "wgc-source-1"}, "revision_id": revision,
  "content_hash": sha, "run_id": identity, "supersedes_refs": history_refs,
  "lineage_refs": history_refs,
  "data": ref(f"{kind}_data")}))
defs["record"] = {"oneOf": record_variants}
schema = {"$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "urn:wgc:ig:source:1", "title": "WGC source Instruction Graph contract",
 "description": "Source descriptions and revision-scoped evidence; no executable language or semantic approval by validation.",
 **obj({"schema_version": {"const": "wgc-source-1"}, "snapshot_id": identity,
        "records": arr(ref("record"), 1)}), "$defs": defs}
p=Path('contracts/ig/source.schema.json')
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(schema,indent=2)+'\n',encoding='utf-8')
print(p)
