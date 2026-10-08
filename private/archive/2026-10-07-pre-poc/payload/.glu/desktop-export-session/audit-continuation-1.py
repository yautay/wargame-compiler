"""Session evidence only; no inference, response generation, import or revisions."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from wgc import contracts
from wgc.desktop_export import export_package, verify_files

OUT = ROOT / ".glu/desktop-export-session/continuation-1"
OUT.mkdir(exist_ok=False)
git = ["git", "-c", "safe.directory=C:/dev/wargame-compiler", "-c", "core.excludesFile=NUL"]
paths = subprocess.check_output(git + ["ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
snapshot = {name: digest(ROOT / name) for name in paths if name and (ROOT / name).is_file()}
(OUT / "start-hashes.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
responses = ROOT / "private/source-artifacts/SRC-desktop.rules/responses"
assert responses.is_dir()
inventory = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "hash": digest(p)}
             for p in sorted(responses.rglob("*")) if p.is_file()]
assert not inventory, "Response appeared: stop and validate its original bytes separately."
package_root = ROOT / "private/source-artifacts/SRC-desktop.rules/packages/mdesk2-p1-context2"
package = json.loads((package_root / "manifest.txt").read_bytes())
assert not contracts.errors(package)
verify_files(package, package_root)
assert package["id"] == "desktop.54901819238b4534124fbd96513254aefcf079b48fbed33cbeb65d81475bb1be"
assert package["hash"] == "sha256:ae38b9e191629aa530f20e762aad2b87a4cf2d0dd6e959b7da3a97c6de2c8228"
assert package["target_pages"] == [1] and package["context_pages"] == [2]
assert (package_root / "desktop.schema.json").read_bytes() == (ROOT / "contracts/schemas/desktop.schema.json").read_bytes()
repeat = export_package(ROOT / "bench/desktop-two-page/source.pdf", OUT / "repeat-package",
                        doc="SRC-desktop.rules", target_pages=[1])
assert repeat == package
original_files = {p.name: p.read_bytes() for p in package_root.iterdir() if p.is_file()}
repeated_files = {p.name: p.read_bytes() for p in (OUT / "repeat-package").iterdir() if p.is_file()}
assert original_files == repeated_files
report = {"date": "2026-10-06", "responses_directory_exists": True, "responses": inventory,
          "response_json_schema_binding_structure": "not run: no actual response",
          "desktop_exchange": "no saved response or evidence; both applications untested in this session",
          "application": "unknown", "model": "unknown", "receipt_method": "none",
          "package": {"id": package["id"], "hash": package["hash"]},
          "package_schema_and_asset_hashes_valid": True, "repeat_bytes_equal": True,
          "files": {name: {"bytes": len(data), "hash": "sha256:" + hashlib.sha256(data).hexdigest()}
                    for name, data in original_files.items()},
          "total_bytes": sum(map(len, original_files.values())), "snapshot_files": len(snapshot)}
(OUT / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in report.items() if key != "files"}, ensure_ascii=False, indent=2))
