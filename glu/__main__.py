"""CLI: `glu status`, `glu export`, `glu build` and `glu reconcile` (also `python -m glu`). Exit code 2 = operational
error (ADR-0002); `glu build` returns 1 when the build ends `failed`."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import yaml

from glu.store import Store, StoreError, db_path
from wgc.kb import KBError
from wgc.tasks import TaskError


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


def _cmd_build(args) -> int:
    from glu import exec as executor, planner
    from wgc import kb
    from wgc.canonical import content_hash
    from wgc.kb import Workspace

    root = Path(args.root)
    project = args.project or root.resolve().name
    ws = Workspace(root)
    plan = planner.plan(ws, args.stage, args.scope)
    if args.dry_run:
        print(f"Plan buildu (bez wykonania): projekt {project}, etap {plan.stage}, zakres {plan.scope}")
        for j in plan.jobs:
            key = content_hash(j.cache_key).split(":", 1)[1][:16]
            print(f"  {j.spec.name}  tier: {j.tier}  wejścia: {', '.join(j.inputs)}  klucz: {key}")
        for name in plan.skipped:
            print(f"  pominięte (brak implementacji Tier 0): {name}")
        if kb.pending_batch(root):
            print("  kb/ ma przerwaną partię zapisu: `glu build` najpierw ją uzgodni (podgląd: `glu reconcile --dry-run`)")
        print(f"Jobów: {len(plan.jobs)}. Niczego nie zapisano.")
        return 0
    with Store.at_root(root) as store:
        result = executor.run(store, ws, plan, project)
    for line in result.reconciled:
        print(f"Reconcile: {line}")
    m = result.metrics
    print(f"Build {result.id}: projekt {project}, etap {result.stage}, zakres {result.scope}, stan: {result.state}")
    for j in result.jobs:
        print(f"  {j.id}  {j.task}  {', '.join(j.inputs)}  stan: {j.state}"
              + (f"  rekordy: {', '.join(j.records)}" if j.records else ""))
        for issue in j.issues:
            print(f"    {issue}")
    for name in plan.skipped:
        print(f"  pominięte (brak implementacji Tier 0): {name}")
    print(f"Jobów: {m['jobs_total']} (udane {m['jobs_done']}, nieudane {m['jobs_failed']}); rekordy: nowe "
          f"{m['records_created']}, zmienione {m['records_updated']}, bez zmian {m['records_unchanged']}.")
    return 0 if result.state == "done" else 1


def _cmd_reconcile(args) -> int:
    from glu import reconcile
    from wgc import fsio
    root = Path(args.root)
    if args.dry_run or not db_path(root).is_file():  # no store: no builds to reconcile, only kb/, no lock file
        res = reconcile.reconcile(root, dry_run=args.dry_run)
    else:
        try:  # the start lock of builds: a build being created is never taken for a dead one (ADR-0031)
            with fsio.exclusive(root / reconcile.START_LOCK, reconcile.START_TIMEOUT):
                res = reconcile.reconcile(root)
        except fsio.LockBusy:
            raise StoreError(f"inny `glu build` tej gry startuje dłużej niż {reconcile.START_TIMEOUT:g} s "
                             f"({reconcile.START_LOCK.as_posix()}); ponów") from None
    if not res.actions:
        print("Nic do uzgodnienia: kb/ bez przerwanej partii, brak przerwanych buildów.")
        return 0
    print("Plan reconcile (bez zapisu):" if args.dry_run else "Reconcile:")
    for line in res.actions:
        print(f"  {line}")
    if args.dry_run:
        print("Niczego nie zapisano.")
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

    p = sub.add_parser("build", help="planuje i wykonuje joby etapu (Tier 0: zadania deterministyczne); zapis do kb/ "
                                     "tylko przez wgc.kb.accept")
    p.add_argument("--root", default=".", metavar="katalog", help="katalog repo gry (domyślnie bieżący)")
    p.add_argument("--stage", required=True, metavar="etap", help="etap, np. 1 albo stage1")
    p.add_argument("--scope", default="all", metavar="zakres",
                   help="all (domyślnie), chapter:<N> albo segment:<SEG-id>")
    p.add_argument("--project", metavar="nazwa", help="nazwa projektu w buildzie (domyślnie nazwa katalogu --root)")
    p.add_argument("--dry-run", action="store_true", help="tylko plan jobów; niczego nie zapisuje")
    p.set_defaults(func=_cmd_build)

    p = sub.add_parser("reconcile", help="recovery kb/ i uzgodnienie przerwanych buildów i jobów z kb/ (ADR-0031)")
    p.add_argument("--root", default=".", metavar="katalog", help="katalog repo gry (domyślnie bieżący)")
    p.add_argument("--dry-run", action="store_true", help="tylko plan; niczego nie zapisuje")
    p.set_defaults(func=_cmd_reconcile)
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
    except (StoreError, KBError, TaskError) as e:
        print(f"BŁĄD: {e}", file=sys.stderr)
        return 2
    except sqlite3.Error as e:  # e.g. `database is locked` after the store was opened
        print(f"BŁĄD: baza stanu GLU: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
