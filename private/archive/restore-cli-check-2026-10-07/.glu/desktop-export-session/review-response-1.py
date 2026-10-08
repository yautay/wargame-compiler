"""Read-only response validation and session evidence; no importer or revisions."""
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

OUT = ROOT / ".glu/desktop-export-session/response-review-1"
OUT.mkdir(exist_ok=False)
excludes = OUT / "empty-git-excludes"
excludes.write_bytes(b"")
git = ["git", "-c", "safe.directory=C:/dev/wargame-compiler", "-c", f"core.excludesFile={excludes}"]
names = subprocess.check_output(git + ["ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()
snapshot = {name: digest((ROOT / name).read_bytes()) for name in names if name and (ROOT / name).is_file()}
(OUT / "start-hashes.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
responses = ROOT / "private/source-artifacts/SRC-desktop.rules/responses"
originals = {p.relative_to(responses).as_posix(): p.read_bytes() for p in responses.rglob("*") if p.is_file()}
package_root = ROOT / "private/source-artifacts/SRC-desktop.rules/packages/mdesk2-p1-context2"
package_bytes = {p.relative_to(package_root).as_posix(): p.read_bytes() for p in package_root.rglob("*") if p.is_file()}
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
package = parse(package_bytes["manifest.txt"])
response = parse(originals["mdesk2-chatgpt.json"])
verify_files(package, package_root)
schema = parse(package_bytes["desktop.schema.json"])
supplied_errors = [{"path": list(e.absolute_path), "message": e.message}
                   for e in Draft202012Validator(schema).iter_errors(response)]
l0 = contracts.errors(response)
issues = check(package, response)
binding = {"id": package["id"], "hash": package["hash"]}
document = response["document"]
conversation = parse(originals["mdesk2-chatgpt-conversation.json"])
report = {"date": "2026-10-06", "response_file": "private/source-artifacts/SRC-desktop.rules/responses/mdesk2-chatgpt.json",
          "response_bytes": len(originals["mdesk2-chatgpt.json"]), "response_sha256": digest(originals["mdesk2-chatgpt.json"]),
          "strict_json_valid": True, "supplied_schema_errors": supplied_errors, "contracts_errors": l0,
          "desktop_check": [asdict(issue) for issue in issues], "package_files_valid": True,
          "package": binding, "response_binding_matches": response["package"] == binding,
          "document_binding_matches": document["package"] == binding, "source_matches": document["source"] == package["source"],
          "response_alias_identical": originals["response.json"] == originals["mdesk2-chatgpt.json"],
          "producer": response["producer"], "evidence_thread": conversation.get("thread", {}),
          "exchange_application_from_trial": "Codex desktop", "model_from_trial": "unknown",
          "receipt_method_from_trial": "Codex file tool; no confirmed manual copy or attachment download",
          "required_chatgpt_or_claude_exchange_proven": False, "semantic_approval_granted": False,
          "counts": {key: len(document[key]) for key in ("blocks", "relations", "evidence", "coverage")},
          "gaps": [area for area in document["coverage"] if area["classification"] == "gap"],
          "responses_original_hashes": {name: digest(data) for name, data in originals.items()},
          "package_original_hashes": {name: digest(data) for name, data in package_bytes.items()},
          "resolved_text": {e["ref"]: resolve_text(package, e)[0] for e in document["evidence"] if e["kind"] == "text_layer"} if not issues else {},
          "snapshot_files": len(snapshot)}
assert all((responses / name).read_bytes() == data for name, data in originals.items())
assert all((package_root / name).read_bytes() == data for name, data in package_bytes.items())
report["original_bytes_preserved"] = True
(OUT / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in report.items() if key not in {"evidence_thread", "responses_original_hashes", "package_original_hashes", "resolved_text", "gaps"}}, ensure_ascii=False, indent=2))
print(json.dumps({"resolved_text": report["resolved_text"], "gaps": report["gaps"]}, ensure_ascii=False, indent=2))
