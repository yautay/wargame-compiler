"""One-task coordinator refinement; never exposes dependency records or histories."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
RUN = ROOT / "private/workflow/runs/IG-2B07/coordinator-999c866b-01"
SESSION = ROOT / "private/workflow/orchestrator/20261016T195516Z-332903f5/001-IG-2B07-coordinator-999c866b"
ATTEMPT = "private/workflow/runs/IG-2B07/inventory-25-28-01"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path):
    p = ROOT / path
    return {"path": path, "sha256": sha(p), "bytes": p.stat().st_size}


def freeze(name, value):
    p = RUN / name
    with p.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    return pin(p.relative_to(ROOT).as_posix())


def main():
    initial = load(RUN / "checkpoint-initial.json")
    for rel, expected in initial["base_hashes"].items():
        assert sha(ROOT / rel) == expected, f"Concurrent change: {rel}"
    observed = load(SESSION / "runtime-configuration.json")
    assert (observed["status"], observed["model"], observed["reasoning"]) == ("confirmed", "gpt-6.1-sol", "high")
    common = {key: initial[key] for key in ("task", "role", "actor", "model", "reasoning", "configuration_evidence", "configuration_sha256")}
    assert sha(ROOT / common["configuration_evidence"]) == common["configuration_sha256"]
    dep = load(RUN / "dependency-inventory-projection.json")["data"]
    assert not (ROOT / ATTEMPT).exists(), "Executor attempt must be absent"
    source = dep["source"]
    input_pins = [dep["baseline_inventory"], dep["identity_registry"], source["pdf"], source["provenance"], *dep["reports"].values()]
    for p in input_pins:
        assert pin(p["path"]) == p
    spec = importlib.util.spec_from_file_location("task_workflow", ROOT / "scripts/workflow.py")
    w = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(w)
    queue_path = ROOT / w.QUEUE
    queue = load(queue_path)
    before = copy.deepcopy(queue)
    task = next(t for t in queue["tasks"] if t["id"] == "IG-2B07")
    original = load(SESSION / "task.json")
    assert {k: v for k, v in task.items() if k != "events"} == original
    assert task["status"] == "planned"
    assert all(next(t for t in queue["tasks"] if t["id"] == id)["status"] == "done" for id in task["depends"])
    refs = load(SESSION / "references.json")
    for id, event in refs["dependencies"].items():
        dependency = next(t for t in queue["tasks"] if t["id"] == id)
        assert dependency["events"][-1] == event
        assert sha(ROOT / event["evidence"]) == event["sha256"]

    inspection = freeze("coordinator-source-inspection.json", {
        **common, "format": "wgc-coordinator-source-inspection-1",
        "purpose": "Contract refinement only; executor and independent reviewer must inspect originals afresh.",
        "source": source["pdf"], "assigned_physical_pages": [25, 26, 27, 28],
        "viewed": [pin((RUN / f"original-page-{n}.png").relative_to(ROOT).as_posix()) for n in (25, 26, 27, 28)],
        "adjacent_context": [
            {"physical_page": 24, "box": [0, 666666, 1000000, 1000000], "purpose": "Entry procedure context only", "image": pin((RUN / "boundary-page-24.png").relative_to(ROOT).as_posix())},
            {"physical_page": 29, "box": [0, 0, 1000000, 333334], "purpose": "Exit example continuation only", "image": pin((RUN / "boundary-page-29.png").relative_to(ROOT).as_posix())},
        ],
        "observations": [
            "Pages 25-27 contain two-column text, headings, subordinate lists, notes, exceptions and examples; page 25 also contains artwork.",
            "Page 28 contains an extended example with two diagrams; account independently for counters, markers, letters/numbers, arrows and associated prose.",
            "Page 26 left-column opening continues page 25; page 27 left-column opening continues page 26; page 28 crosses columns and continues onto page 29.",
            "The dependency boundary projection is empty. This is not a claim of no continuation; preserve the inherited page-25 context record and inspect original boundary strips.",
        ],
        "semantic_acceptance": "none", "product_delivery": False,
    })
    deliverables = [
        f"{ATTEMPT}/final-verified/inventory.json",
        f"{ATTEMPT}/final-verified/identity-registry.json",
        *[f"{ATTEMPT}/{name}" for name in (
            "region-ledger.json", "continuations.json", "coverage-report.json", "source-pins.json", "toolchain.json",
            "original-page-inspection.json", "component-ledger.json", "preservation-report.json", "replay-report.json",
            "validation-report.json", "delivery-handoff.md")],
    ]
    scope = {
        "source_id": source["id"], "source_revision": source["sha256"], "source_page_count": 44,
        "assigned_physical_pages": [25, 26, 27, 28],
        "assigned_page_metadata": dep["assigned_page_metadata"],
        "replace_only_region_ids": [r["id"] for r in dep["assigned_region_metadata"] if r["key"].endswith(":unprocessed-placeholder")],
        "preserve_existing_assigned_page_context": [r for r in dep["assigned_region_metadata"] if r["denominator_role"] == "context"],
        "context_only_pages": [24, 29],
        "context_only_boxes": {"24": [0, 666666, 1000000, 1000000], "29": [0, 0, 1000000, 333334]},
        "context_limit": "Only the named boundary strips; do not analyze other adjacent-page text or diagrams. If insufficient, checkpoint a missing-context blocker for a new scoped session.",
        "baseline_inventory": dep["baseline_inventory"], "identity_registry": dep["identity_registry"],
        "source_pdf": source["pdf"], "source_provenance": source["provenance"], "current_reports": dep["reports"],
        "baseline_counts": dep["counts"], "attempt_root": ATTEMPT,
        "preservation": "Keep all 44 pages, all nonassigned region/link/evidence records and registry bindings unchanged. Remove only four assigned placeholder memberships; retain their old registry entries. Preserve the existing page-25 context record, its evidence and links. Append new assigned regions/evidence and narrowly scoped context regions; no ancestor baseline or report substitution.",
        "evidence_generation": "Generate every new region/component crop, text and image serially in the current Python process using installed tooling. No multiprocessing, worker pools or external service. Recheck source and input hashes before and after.",
        "replays": {"count": 2, "directories": [f"{ATTEMPT}/replay-1", f"{ATTEMPT}/replay-2"],
            "requirement": "Run two separate complete independent regenerations from the pinned author input and persisted registry into absent directories. Each replay regenerates the entire new region/component set, not a sample or copied evidence. Freeze exact commands, pins and output-set comparisons. Compare stable IDs, author fields, geometry, reading order, links, coverage and payload hashes after explicitly normalizing only output-path-dependent fields; preserve both raw outputs and explain any engine metadata differences."},
        "report_contracts": {
            "region-ledger.json": "Complete assigned-page region accounting: stable IDs/keys, kind, box, reading order, evidence IDs, coverage statuses, uncertain readings and all leftovers. Retain a structural preservation index for nonassigned entries without re-reading their source content.",
            "component-ledger.json": "Enumerate every visible component of both page-28 diagrams and any other assigned diagram/artwork/table: counters, markers, annotations, arrows, legends and labels. Pin parent region, box and fresh evidence per component. Nested component observations have zero additional inventory denominator and do not create overlapping inventory boxes.",
            "continuations.json": "Pin every within-page/column and cross-page continuation endpoint and evidence; preserve cross-batch links and inherited context. Include assigned_range_entry and assigned_range_exit with physical_page 25 and 28 respectively, explicit observation, exact endpoint IDs and page-24/page-29 context-only locators. Empty prior boundary projection is unknown, not absence.",
            "coverage-report.json": "Report separate full-44-page inventory, assigned-page inventory and context-only ID sets/counts; check set equality and disjointness where applicable. Preserve nonassigned unprocessed gaps; count exclusions and uncertainty visibly. Context contributes zero denominator. Geometry, substantive accounting, transcription, descriptive/formal semantics and executable readiness remain separate.",
            "source-pins.json": "Pin actual accepted baseline inventory/registry, every current report, original source/provenance, original-page render evidence, every fresh region/component evidence input and two replay outputs. Locators carry source SHA, physical page, region/component ID, box, exact path, bytes and SHA-256. No obsolete placeholder source paths.",
            "toolchain.json": "Pin actual interpreter, bundled process_pythonpath (both repo/src and bundled site-packages), process_path_prefix, resolved Poppler binaries and hashes, library/engine versions and rendering settings. Preserve process-local inherited settings; no installs or global changes.",
            "original-page-inspection.json": "Fresh executor visual inspection of all four original assigned pages, both columns, notes/examples/diagrams, proposed boundaries/components and exact permitted adjacent strips. Pin source/render hashes and observations. Coordinator observations do not transfer inspection claims.",
            "preservation-report.json": "Compare the complete baseline and result internally. Prove every nonassigned page and region, all inherited evidence/links, existing registry entries and bindings remain unchanged; assigned-page geometry/source identity unchanged. Show exactly four placeholder memberships retired, no other deletion, and new IDs/links/evidence restricted to the assigned/context scope. Freeze counts and hashes without dumping unassigned source text.",
            "replay-report.json": "Pin both complete independent replay command logs, all input/output hashes, complete target-set equality, component equality, stable registry identity and normalized comparison results; no partial/sampled replay.",
            "validation-report.json": "Freeze exact commands, exits and report/log hashes, full/task/context denominators, artifact validation and unresolved limits; green structure is not human semantic acceptance.",
        },
    }
    assert len(scope["replace_only_region_ids"]) == 4
    appended_acceptance = [
        "Use the hash-pinned accepted IG-2B06 full 44-page inventory and companion identity registry; preserve all nonassigned records, inherited evidence/links and registry bindings. Retire only the four pages-25-28 placeholder memberships without deleting registry entries.",
        "Freshly inspect every original assigned page, column, note, example, diagram and component; pin exact source/page/box evidence for all new regions and components, uncertainty and explicit gaps. Boundary context is limited to the authorized page-24 bottom and page-29 top strips and contributes zero denominator.",
        "Freeze final-verified/inventory.json and identity-registry.json plus all root reports named in the refined contract under the new owned inventory-25-28-01 attempt. Keep complete full/task/context denominators separate and retain the persisted registry binding.",
        "Generate evidence serially and complete two separate independent full replays, preserving every new region/component and checking complete target-set equality, stable IDs, evidence freshness, reading order, links and path-normalized output comparisons.",
        "Obtain fresh independent technical/source-accounting review against original assigned pages, the complete region/component ledgers and the entire frozen delivery. Preserve all human semantic gates; this inventory grants no gameplay legality or executable readiness.",
    ]
    commands = [
        f".venv/Scripts/python.exe -m wgc.sources validate {ATTEMPT}/final-verified/inventory.json",
        f".venv/Scripts/python.exe -m pytest -q tests/sources --basetemp {ATTEMPT}/pytest-sources -p no:cacheprovider --tb=short",
        "powershell -NoProfile -File scripts/check.ps1 -Task IG-2B07",
        "git diff --check",
    ]
    appended_tests = [
        "Verify every pinned input SHA-256 before/after execution; validate the final complete inventory against actual source bytes, all 44 physical page geometries, exact evidence and the companion registry.",
        "Compare baseline/result internally: unchanged nonassigned records/evidence/links and all existing registry entries; exactly four placeholder memberships removed; additions restricted to assigned/context scope; no stale source-reference index pins.",
        "Verify complete region/component and continuation endpoint sets, two independent replay target-set equalities, complete full/task/context denominators and zero context contribution; explicitly retain remaining unprocessed pages and all uncertainty.",
        "Run both complete serial evidence replays in separate fresh directories and freeze actual invocation commands, output hashes and comparison reports; review every original assigned page and every fresh region/component crop independently.",
        *commands,
    ]
    contract = freeze("refined-contract.json", {
        **common, "format": "wgc-inventory-batch-contract-1", "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": scope, "input_pins": input_pins, "deliverables": deliverables,
        "original_acceptance": original["acceptance"], "original_tests": original["tests"],
        "additional_acceptance": appended_acceptance, "additional_tests": appended_tests,
        "required_validation_commands": commands, "coordinator_inspection": inspection,
        "review_gate": "Fresh independent reviewer identity and configuration must assess the entire frozen manifest, original assigned pages and every criterion before acceptance. No coordinator/executor source-semantic acceptance is inherited.",
        "authorization_limits": "This refines readiness only. No product delivery, source-meaning acceptance, downstream work or executor launch is asserted.",
    })
    task["outputs"] = deliverables
    task["write_scope"] = [ATTEMPT + "/"]
    task["inputs"] = [f"{p['path']} (SHA-256 {p['sha256']})" for p in input_pins] + [
        "Assigned original physical pages 25-28 only; page-24 bottom third and page-29 top third solely for continuation context.",
        f"Refined contract: {contract['path']} (SHA-256 {contract['sha256']}).",
    ]
    task["context"] = ["docs/IG-WGU-ARCHITECTURE.md", "docs/IG-DATA-MODEL.md", source["provenance"]["path"], dep["reports"]["toolchain.json"]["path"], contract["path"]]
    task["source_scope"] = scope
    task["refinement_evidence"] = contract
    task["acceptance"] += appended_acceptance
    task["tests"] += appended_tests
    task["start_conditions"] += [
        "Verify exact accepted dependency pins and refined contract; the executor attempt must be absent before claim. Record a fresh checkpoint and observed gpt-6.1-sol/high configuration.",
        "Read only prepared dependency sections and the assigned source/page/ID scope. Preserve inherited process-local PYTHONPATH with both repo/src and bundled site-packages and installed Poppler paths.",
    ]
    task["handoff"] += ["Freeze all required root reports, final sidecar/registry and every original/region/component evidence and independent replay artifact in the entire delivery manifest; request independent original-page/accounting review."]
    task["exclusions"] += ["Unassigned source content, whole-PDF analysis, old dependency transcripts, evidence replay claims inherited from prior roles, worker-process pools and source-semantic acceptance by a model."]
    policy_path = ROOT / "docs/work/context-policy.json"
    policy = load(policy_path)
    policy_before = copy.deepcopy(policy)
    for rel in [*task["context"], *[p["path"] for p in input_pins], "src/wgc/sources/README.md", "src/wgc/sources/__init__.py", "src/wgc/sources/__main__.py", "src/wgc/sources/inventory.py", "src/wgc/sources/geometry.py", "src/wgc/sources/pdf.py", "contracts/ig/README.md", "contracts/ig/regions.schema.json"]:
        if rel not in policy["allow"]:
            policy["allow"].append(rel)
    assert all(t == next(x for x in queue["tasks"] if x["id"] == t["id"]) for t in before["tasks"] if t["id"] != task["id"])
    assert task["acceptance"][:len(original["acceptance"])] == original["acceptance"]
    assert task["tests"][:len(original["tests"])] == original["tests"]
    freeze("preserved-task-contract.json", {**common, "format": "wgc-coordinator-preservation-1", "untouched_other_tasks": True, "other_task_count": len(queue["tasks"]) - 1, "original_criteria_retained_verbatim": True, "original_tests_retained_verbatim": True, "human_gate_unchanged": task["semantic_acceptance_required"] == original["semantic_acceptance_required"], "policy_added_exact_paths": [p for p in policy["allow"] if p not in policy_before["allow"]]})
    policy_path.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert all(w.permitted(ROOT, p) and (ROOT / p).is_file() for p in task["context"])
    w.validate(queue, ROOT, check_views=False)
    readiness = freeze("ready.json", {
        **common, "summary": "IG-2B07 refined with accepted current baseline/source/report pins, exact pages/IDs, absent disjoint attempt, complete accounting/replays and fresh independent review requirements.",
        "criteria": ["Direct dependency is done and exact accepted pins verified locally.", "Full baseline and registry retained; exact assigned/context scope pinned.", "Original acceptance and required tests retained verbatim and strengthened.", "Exact context exists and is permitted; product execution and acceptance remain pending."],
        "artifacts": [contract, inspection, pin((RUN / "input-verification.json").relative_to(ROOT).as_posix()), pin((RUN / "preserved-task-contract.json").relative_to(ROOT).as_posix())],
        "checks": [{"command": "Coordinator local input/hash, contract preservation, context existence and workflow.validate(check_views=False)", "exit_code": 0}],
        "ready_scope": "Executor may claim only the new inventory-25-28-01 attempt after fresh configuration and checkpoint. Independent source-accounting review is a future acceptance gate.",
        "product_complete": False, "semantic_acceptance": "none", "tokens": None,
    })
    w.transition(queue, ROOT, task["id"], "ready", readiness["path"])
    queue["updated"] = datetime.now(timezone.utc).date().isoformat()
    assert sha(queue_path) == initial["base_hashes"]["docs/work/queue.json"]
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    w.render(queue, ROOT)
    w.validate(queue, ROOT)
    freeze("checkpoint-refined.json", {**common, "format": "wgc-coordinator-checkpoint-1", "base_hashes": initial["base_hashes"], "changed_hashes": {rel: sha(ROOT / rel) for rel in initial["base_hashes"]}, "contract": contract, "readiness": readiness, "completed_criteria": ["Selected task refinement", "Exact context policy update", "Ready transition and derived views"], "next_operation": "Run required unchanged validation commands; freeze final readiness-validation evidence."})
    print(json.dumps({"task": task["id"], "status": task["status"], "contract": contract, "readiness": readiness, "outputs": len(deliverables), "assigned_pages": [25, 26, 27, 28], "other_tasks_unchanged": True}))


if __name__ == "__main__":
    main()
