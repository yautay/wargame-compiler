"""Read-only review plus exact-byte archival copy; no importer, revisions or inference."""
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from jsonschema import Draft202012Validator
from wgc import contracts
from wgc.desktop import check, resolve_text
from wgc.desktop_export import verify_files

OUT = ROOT / ".glu/desktop-export-session/spqr-response-review-20261007-1"
OUT.mkdir(exist_ok=False)
excludes = OUT / "empty-git-excludes"
excludes.write_bytes(b"")
git = ["git", "-c", "safe.directory=C:/dev/wargame-compiler", "-c", f"core.excludesFile={excludes}"]
names = subprocess.check_output(git + ["ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()
snapshot = {name: digest((ROOT / name).read_bytes()) for name in names if name and (ROOT / name).is_file()}
(OUT / "start-hashes.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result
def no_constants(value):
    raise ValueError(f"Non-standard JSON constant: {value}")
def parse(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicates, parse_constant=no_constants)
folder = ROOT / "private/source-artifacts/SRC-spqr.rules/packages/mdesk2-spqr-p032-context031-033"
originals = {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}
data = originals["response.json"]
package, response = parse(originals["manifest.txt"]), parse(data)
verify_files(package, folder)
preparation = parse((ROOT / "private/source-artifacts/SRC-spqr.rules/previews/package-preparation-p032.json").read_bytes())
assert all(digest(originals[name]) == item["sha256"] for name, item in preparation["files"].items())
assert len(preparation["files"]) == 8
schema_errors = [{"path": list(e.absolute_path), "message": e.message}
                 for e in Draft202012Validator(parse(originals["desktop.schema.json"])).iter_errors(response)]
issues = check(package, response)
document = response["document"]
evidence = {e["ref"]: e for e in document["evidence"]}
resolved = {ref: resolve_text(package, e)[0] for ref, e in evidence.items() if e["kind"] == "text_layer"}
binding = {"id": package["id"], "hash": package["hash"]}
copies = ROOT / "private/source-artifacts/SRC-spqr.rules/responses"
copies.mkdir(exist_ok=True)
copy = copies / "spqr-p032-codex.json"
if copy.exists():
    assert copy.read_bytes() == data, "Existing response copy differs; do not overwrite."
else:
    copy.write_bytes(data)
report = {"date": "2026-10-07", "original_response_file": str((folder / "response.json").relative_to(ROOT)),
          "archival_copy": str(copy.relative_to(ROOT)), "response_bytes": len(data), "response_sha256": digest(data),
          "strict_json_valid": True, "supplied_schema_errors": schema_errors, "contracts_errors": contracts.errors(response),
          "desktop_check": [asdict(i) for i in issues], "desktop_diagnostic_count": len(issues),
          "diagnostic_counts_by_code": dict(Counter(i.code for i in issues)), "package_files_valid": True,
          "original_eight_package_assets_preserved": True, "unlisted_response_was_added_to_package": True,
          "package": binding, "response_binding_matches": response["package"] == binding,
          "document_binding_matches": document["package"] == binding, "source_matches": document["source"] == package["source"],
          "producer": response["producer"], "actual_application_from_thread": "Codex desktop",
          "evidence_thread_id": "01a11505-ed75-7d51-9ed2-7701c30c0b1a", "evidence_thread_title": "Przygotuj response dla PDF 32",
          "reasoning_effort_reported_by_owner_in_source_thread": "wysoki",
          "receipt_method_from_thread": "direct file write by Codex tool; no confirmed manual copy or attachment download",
          "required_chatgpt_or_claude_exchange_proven": False, "semantic_approval_granted": False,
          "counts": {k: len(document[k]) for k in ("blocks", "relations", "evidence", "coverage")},
          "tables": [b for b in document["blocks"] if b["type"] == "table"],
          "gaps": [c for c in document["coverage"] if c["classification"] == "gap"],
          "resolved_text": resolved, "image_evidence": [e for e in document["evidence"] if e["kind"] != "text_layer"],
          "preserved_original_files": {name: digest(content) for name, content in originals.items()},
          "snapshot_files": len(snapshot)}
assert all((folder / name).read_bytes() == content for name, content in originals.items())
assert copy.read_bytes() == data
report["original_bytes_preserved"] = True
(OUT / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
private_report = copies / "spqr-p032-codex-review-20261007-1.json"
assert not private_report.exists()
private_report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in report.items() if key not in {"desktop_check", "tables", "gaps", "resolved_text", "image_evidence", "preserved_original_files"}}, ensure_ascii=False, indent=2))
