"""Local package preparation evidence; no inference, responses, import or revision store."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from wgc import contracts
from wgc.desktop_export import export_package, verify_files

OUT = Path(__file__).resolve().parent
package_root = ROOT / "private/source-artifacts/SRC-spqr.rules/packages/mdesk2-spqr-p032-context031-033"
source = Path("C:/dev/spqr/sources/SPQR+Deluxe_Rule+book_WEB.pdf")
def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()
files = {p.name: p.read_bytes() for p in package_root.iterdir() if p.is_file()}
package = json.loads(files["manifest.txt"])
verify_files(package, package_root)
assert not contracts.errors(package)
assert package["target_pages"] == [32] and package["context_pages"] == [31, 33]
assert package["source"]["file_hash"] == digest(source.read_bytes())
assert files["desktop.schema.json"] == (ROOT / "contracts/schemas/desktop.schema.json").read_bytes()
assert not any(p.suffix.lower() == ".pdf" for p in package_root.iterdir())
preview = ROOT / "private/source-artifacts/SRC-spqr.rules/previews/spqr-5th-p032.png"
assert preview.read_bytes() == files["p032.png"]
repeat_root = OUT / "spqr-repeat-package"
repeat = export_package(source, repeat_root, doc="SRC-spqr.rules", target_pages=[32], context_pages=[31, 33])
assert repeat == package
assert files == {p.name: p.read_bytes() for p in repeat_root.iterdir() if p.is_file()}
private_root = package_root.parents[1]
responses = private_root / "responses"
responses.mkdir(exist_ok=True)
assert not list(responses.iterdir())
approval = {"date": "2026-10-06", "approval_source": "owner_statement_in_current_chat",
            "owner_statement": "ta jest ok", "target_pdf_page": 32, "printed_page": "32",
            "context_pdf_pages": [31, 33], "source_sha256": digest(source.read_bytes()),
            "preview_sha256": digest(preview.read_bytes()), "package": {"id": package["id"], "hash": package["hash"]},
            "approval_scope": "page selection for trial; no semantic approval"}
approval_path = private_root / "previews/approval-p032.json"
assert not approval_path.exists()
approval_path.write_text(json.dumps(approval, ensure_ascii=False, indent=2), encoding="utf-8")
report = {"date": "2026-10-06", "package": approval["package"], "target_pages": [32], "context_pages": [31, 33],
          "package_schema_valid": True, "manifest_and_asset_hashes_valid": True,
          "original_pdf_not_included": True, "approved_preview_bytes_match": True, "repeat_bytes_equal": True,
          "files": {name: {"bytes": len(data), "sha256": digest(data)} for name, data in files.items()},
          "total_bytes": sum(map(len, files.values())), "response_received": False,
          "manual_exchange": "pending; ChatGPT and Claude Desktop not tested"}
(OUT / "spqr-preparation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
private_report = private_root / "previews/package-preparation-p032.json"
assert not private_report.exists()
private_report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in report.items() if key != "files"}, ensure_ascii=False, indent=2))
print(json.dumps({"files": {name: len(data) for name, data in files.items()}}, ensure_ascii=False, indent=2))
