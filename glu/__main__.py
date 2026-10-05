"""CLI: `glu status` and `glu export` (also `python -m glu`). Exit code 2 = operational error (ADR-0002)."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import yaml

from glu.store import Store, StoreError


def _summary(store: Store, build: dict, with_jobs: bool) -> dict:
    out = {"id": build["id"], "project": build["project"], "target": build["target"], "state": build["state"],
           "started_at": build["started_at"], "finished_at": build.get("finished_at"),
           "jobs": store.job_counts(build["id"])}
    if with_jobs:
        out["job_list"] = [{"id": j["id"], "task": j["task"], "state": j["state"], "tier": j.get("tier"),
                            "attempts": len(j.get("attempts", []))} for j in store.jobs(build["id"])]
    return out


def _print_status(path: Path, builds: list[dict]) -> None:
    if not builds:
        print(f"Brak buildów w {path}.")
        return
    for b in builds:
        target = " ".join(filter(None, [b["target"]["stage"], b["target"].get("scope")]))
        end = f", koniec {b['finished_at']}" if b["finished_at"] else ""
        print(f"{b['id']}  {b['project']}  {target}  stan: {b['state']}  (start {b['started_at']}{end})")
        counts = ", ".join(f"{state} {n}" for state, n in b["jobs"].items())
        print(f"  joby: {sum(b['jobs'].values())}" + (f" ({counts})" if counts else ""))
        for j in b.get("job_list", []):
            print(f"  {j['id']}  {j['task']}  stan: {j['state']}  tier: {j['tier'] or '-'}  próby: {j['attempts']}")


def _cmd_status(args) -> int:
    with Store.at_root(args.root, create=False) as store:
        builds = [store.build(args.build)] if args.build else store.builds()
        rows = [_summary(store, b, with_jobs=bool(args.build)) for b in builds]
        path = store.path
    if args.json:
        print(json.dumps({"db": str(path), "builds": rows}, ensure_ascii=False, indent=2))
    else:
        _print_status(path, rows)
    return 0


def _cmd_export(args) -> int:
    with Store.at_root(args.root, create=False) as store:
        doc = store.export(args.build)
    text = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120)
    if args.out:
        out = Path(args.out)
        try:
            out.write_text(text, encoding="utf-8", newline="\n")
        except OSError as e:
            raise StoreError(f"nie można zapisać {out}: {e}") from e
        print(f"Zapisano {len(doc['records'])} rekordów glu/exec@0 do {out}.")
    else:
        sys.stdout.write(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="glu", description="wargame-compiler: wykonanie i orkiestracja (GLU).")
    sub = parser.add_subparsers(dest="command", required=True, metavar="polecenie")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=".", metavar="katalog", help="katalog repo gry (domyślnie bieżący)")
    common.add_argument("--build", metavar="build_id", help="tylko ten build")

    p = sub.add_parser("status", parents=[common], help="stan buildów i jobów z .glu/state.db")
    p.add_argument("--json", action="store_true", help="wynik jako JSON")
    p.set_defaults(func=_cmd_status)

    p = sub.add_parser("export", parents=[common], help="eksport rekordów stanu wykonania jako dokument glu/exec@0")
    p.add_argument("--out", metavar="plik", help="plik YAML (domyślnie standardowe wyjście)")
    p.set_defaults(func=_cmd_export)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Polish messages on a cp1250/cp852 Windows console
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):
        pass
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except StoreError as e:
        print(f"BŁĄD: {e}", file=sys.stderr)
        return 2
    except sqlite3.Error as e:  # e.g. `database is locked` after the store was opened
        print(f"BŁĄD: baza stanu GLU: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
