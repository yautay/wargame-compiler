"""Exact pinned private-byte audit and two repeats in assigned snapshot roots."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat

from wgc.inputs import snapshot as s

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
FROZEN = ROOT / "private/workflow/runs/IG-1B/attempt-20261012T182300Z"
INPUTS = ROOT / "private/ig/projects/spqr/inputs"
SOURCES = ROOT / "private/ig/projects/spqr/sources"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    # Independent, stdlib oracle for these integer-only manifest values.
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def names(directory):
    result = set()
    for current, dirs, files in os.walk(directory, followlinks=False):
        for name in dirs + files:
            path = Path(current) / name
            info = path.lstat()
            assert not stat.S_ISLNK(info.st_mode)
            assert not getattr(info, "st_file_attributes", 0) & 1024
        for name in files:
            result.add((Path(current) / name).relative_to(directory).as_posix())
    return result


def main():
    started = datetime.datetime.now(datetime.timezone.utc)
    req = json.loads((FROZEN / "input-request.json").read_bytes())
    assert req["game_root"] == "C:/repo/wargame-projects/games/spqr"
    assert req["registry_root"] == "C:/repo/wargame-compiler/private/ig/sources/spqr-5e"
    delivery = json.loads((FROZEN / "delivery.json").read_bytes())
    ids = delivery["snapshot_ids"]
    dirs = [INPUTS / ("sha256-" + ids["inputs"][7:]), SOURCES / ("sha256-" + ids["sources"][7:])]
    snapshots = [json.loads((p / "manifest.json").read_bytes()) for p in dirs]
    rows = []
    preserved = {}
    for directory, manifest, group in zip(dirs, snapshots, [req["game_files"], req["registry_files"]]):
        body = {k:v for k,v in manifest.items() if k != "snapshot_id"}
        assert manifest["snapshot_id"] == "sha256:" + digest(canonical(body))
        assert (directory / "manifest.json").read_bytes() == canonical(manifest) + b"\n"
        expected = {"manifest.json"}
        if manifest["kind"] == "source_snapshot":
            expected.add("source-pin.json")
        by_path = {entry["relative_path"]: entry for entry in group}
        for item in manifest["files"]:
            if item["availability"] == "missing":
                assert item["role"] == "configured_source"
                assert item["bytes"] is item["sha256"] is item["blob_path"] is None
                continue
            expected.add(item["blob_path"])
            origin = Path(manifest["origin_root"]) / item["path"]
            # Only individually pinned origins are opened; no auxiliary scan.
            assert item["path"] in by_path
            raw = origin.read_bytes()
            copied = (directory / item["blob_path"]).read_bytes()
            pin = by_path[item["path"]]
            assert raw == copied and len(raw) == item["bytes"] == pin["bytes"]
            assert digest(raw) == item["sha256"] == pin["sha256"]
            rows.append(dict(origin=str(origin), copy=str(directory / item["blob_path"]),
                             bytes=len(raw), sha256=digest(raw), matches=True))
        assert names(directory) == expected
        assert s.verify_snapshot(directory) == manifest
        for name in expected:
            path = directory / name
            preserved[path] = path.read_bytes()
    game_root = Path(req["game_root"])
    actual_wgu = (game_root / "wgu.yaml").read_text(encoding="utf-8")
    source_block = actual_wgu.split("\nsources:\n", 1)[1].split("\npdf:\n", 1)[0]
    current_paths = [(a or b.strip()) for a,b in
                     re.findall(r'^\s*-\s*\{path:\s*(?:"([^"]+)"|([^,]+))', source_block, re.M)]
    configured = req["historical_configured_sources"]
    assert set(current_paths) == {x["relative_path"] for x in configured}
    inventory = json.loads((ROOT / "private/ig/planning/wgu-spqr-2026-10-11/input-inventory.json").read_bytes())
    assert set(current_paths) == {x["configured_path"] for x in inventory["configured_sources"]}
    missing_rows = []
    for entry in configured:
        path = game_root / entry["relative_path"]
        try:
            path.lstat()
        except FileNotFoundError:
            missing_rows.append(dict(path=entry["relative_path"], availability="missing", checked=True))
        else:
            raise AssertionError("Historical configured source is now available: " + str(path))
    availability_path = SOURCES / "availability-d7d7370248aafe9fe4393c5e767264768d908a220f3ef7899de58078f57d1923.json"
    availability_raw = availability_path.read_bytes()
    availability = json.loads(availability_raw)
    assert digest(availability_raw) == availability_path.stem.removeprefix("availability-")
    assert availability_raw == canonical(availability) + b"\n"
    manifest_missing = [x for x in snapshots[0]["files"] if x["role"] == "configured_source"]
    assert availability["configured_sources"] == manifest_missing
    assert {x["path"] for x in manifest_missing} == set(current_paths)
    pin_raw = (dirs[1] / "source-pin.json").read_bytes()
    pin = json.loads(pin_raw)
    assert pin_raw == canonical(pin) + b"\n"
    assert pin == {**req["selection"], "source_snapshot_id": snapshots[1]["snapshot_id"],
                   "selection_purpose": "new_ig_source"}
    assert pin["identity_to_wgu_original"] == "unknown" and pin["semantic_acceptance"] == "not_granted"
    assert snapshots[0]["source_snapshot_id"] == snapshots[1]["snapshot_id"]
    repeats = []
    for index in [1, 2]:
        result = s.freeze_inputs(req, INPUTS, SOURCES)
        assert result["input_snapshot_id"] == ids["inputs"]
        assert result["source_snapshot_id"] == ids["sources"]
        assert all(path.read_bytes() == raw for path,raw in preserved.items())
        assert not list(INPUTS.glob(".pending-*")) and not list(SOURCES.glob(".pending-*"))
        repeats.append(dict(index=index, result=result, exact_prior_bytes_preserved=True))
    product = [a for a in delivery["artifacts"] if not a["path"].startswith("private/workflow/")]
    report = dict(started_utc=started.isoformat(), ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  copied_files=rows, copied_count=len(rows), copied_bytes=sum(x["bytes"] for x in rows),
                  game_file_count=len(req["game_files"]), registry_file_count=len(req["registry_files"]),
                  missing_count=len(missing_rows), missing_configured_sources=missing_rows,
                  exact_sealed_file_sets=True, no_extra_sealed_files_or_links=True,
                  canonical_manifest_ids_verified=True, source_pin=pin,
                  availability_report_canonical_and_matching=True, product_artifact_count=len(product),
                  product_artifact_paths=[x["path"] for x in product], repeats=repeats,
                  source_meaning_reviewed=False, semantic_acceptance_granted=False, executable_readiness_granted=False)
    (HERE / "private-audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:report[k] for k in ["copied_count", "copied_bytes", "game_file_count", "registry_file_count",
                                         "missing_count", "product_artifact_count", "exact_sealed_file_sets"]}))
    print("Two native private repeats preserve identical IDs, manifests and all copied bytes.")


if __name__ == "__main__":
    main()
