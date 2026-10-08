"""Local evidence for the prepared CC0 export, not a desktop round-trip."""
import importlib.metadata
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from wgc.canonical import sha256_hex
from wgc.desktop_export import export_package, verify_files

package_root = ROOT / "private/source-artifacts/SRC-desktop.rules/packages/mdesk2-p1-context2"
package = json.loads((package_root / "manifest.txt").read_text("utf-8"))
verify_files(package, package_root)
repeat_root = ROOT / ".glu/desktop-export-session/repeat-final-1"
repeat = export_package(ROOT / "bench/desktop-two-page/source.pdf", repeat_root,
                        doc="SRC-desktop.rules", target_pages=[1])
assert repeat == package
original_files = {p.name: p.read_bytes() for p in package_root.iterdir() if p.is_file()}
repeat_files = {p.name: p.read_bytes() for p in repeat_root.iterdir() if p.is_file()}
assert original_files == repeat_files
report = {"package": {"id": package["id"], "hash": package["hash"]},
          "target_pages": package["target_pages"], "context_pages": package["context_pages"],
          "repeat_bytes_equal": True, "files": {name: {"size": len(data), "hash": sha256_hex(data)}
                                                 for name, data in original_files.items()},
          "total_bytes": sum(map(len, original_files.values())),
          "libraries": {name: importlib.metadata.version(name)
                        for name in ("pdfplumber", "pdfminer.six", "pypdfium2", "Pillow")},
          "desktop_exchange": "awaiting human; no response received"}
report_path = ROOT / ".glu/desktop-export-session/trial-preparation.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in report.items() if k != "files"}, ensure_ascii=False, indent=2))
