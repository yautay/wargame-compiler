"""CLI: `python -m wgc validate <ścieżki…> [--json]` and `python -m wgc source init|scan|extract|verify` (also installed as `wgc`)."""
from __future__ import annotations

import argparse
import json
import sys

from wgc.validate import ERROR, Report, validate

SEVERITY_PL = {"error": "BŁĄD", "warning": "OSTRZEŻENIE"}


def _print_report(report: Report) -> None:
    for d in report.diagnostics:
        where = f"  [{d.location}]" if d.location else ""
        print(f"{SEVERITY_PL.get(d.severity, d.severity)} {d.code} {d.subject}: {d.message}{where}")
    status = "OK" if report.ok else "NIEPOPRAWNE"
    print(f"{status}: pliki {report.files}, rekordy {report.records}, błędy {len(report.errors)}, "
          f"ostrzeżenia {len(report.warnings)}.")


def _emit(report: Report, as_json: bool) -> int:
    if as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_report(report)
    return 1 if any(d.severity == ERROR for d in report.diagnostics) else 0


def _cmd_validate(args) -> int:
    return _emit(validate(args.paths), args.json)


def _doc_arg(value: str) -> tuple[str, str]:
    role, sep, path = value.partition(":")
    if not sep or not role or not path:
        raise argparse.ArgumentTypeError(f"oczekiwano rola:ścieżka, otrzymano {value!r}")
    return role, path


def _cmd_source(args) -> int:
    from wgc import source
    try:
        if args.source_command == "verify":
            return _emit(source.verify(args.root), args.json)
        if args.source_command == "init":
            messages = source.init(args.root, args.game, args.doc)
        elif args.source_command == "scan":
            messages = source.scan(args.root)
        else:
            messages = source.extract(args.root)
    except source.SourceError as e:
        print(f"BŁĄD: {e}", file=sys.stderr)
        return 2
    for m in messages:
        print(m)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wgc", description="wargame-compiler: narzędzia domenowe (WGC).")
    sub = parser.add_subparsers(dest="command", required=True, metavar="polecenie")
    p = sub.add_parser("validate", help="waliduje pliki KB: schemat (L0), tożsamość i referencje (L1), provenance")
    p.add_argument("paths", nargs="+", metavar="ścieżka", help="plik YAML albo katalog (przeszukiwany rekurencyjnie)")
    p.add_argument("--json", action="store_true", help="raport jako JSON (lista diagnostyk)")
    p.set_defaults(func=_cmd_validate)

    p = sub.add_parser("source", help="Stage 0: inwentarz źródeł (source/inventory.yaml) i tekst segmentów (.glu/source/)")
    ssub = p.add_subparsers(dest="source_command", required=True, metavar="podpolecenie")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=".", metavar="katalog", help="katalog repo gry (domyślnie bieżący)")
    s = ssub.add_parser("init", parents=[common], help="tworzy inwentarz z listą dokumentów źródłowych")
    s.add_argument("--game", required=True, metavar="kod", help="kod gry w ID (SRC-<kod>.<rola>, SEG-<kod>.<etykieta>)")
    s.add_argument("--doc", action="append", default=[], type=_doc_arg, metavar="rola:ścieżka",
                   help="dokument źródłowy (ścieżka względem --root); można powtarzać")
    ssub.add_parser("scan", parents=[common], help="odświeża present, file_hash i extractor dokumentów")
    ssub.add_parser("extract", parents=[common], help="scan + segmentacja: rekordy SEG- w inwentarzu, tekst w .glu/source/")
    s = ssub.add_parser("verify", parents=[common], help="sprawdza inwentarz, hashe plików i segmentów oraz cache tekstu")
    s.add_argument("--json", action="store_true", help="raport jako JSON (lista diagnostyk)")
    p.set_defaults(func=_cmd_source)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Polish messages on a cp1250/cp852 Windows console
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):
        pass
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
