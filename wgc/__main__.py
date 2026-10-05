"""CLI: `python -m wgc validate <ścieżki…> [--json]` (also installed as `wgc`)."""
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


def _cmd_validate(args) -> int:
    report = validate(args.paths)
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_report(report)
    return 1 if any(d.severity == ERROR for d in report.diagnostics) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wgc", description="wargame-compiler: narzędzia domenowe (WGC).")
    sub = parser.add_subparsers(dest="command", required=True, metavar="polecenie")
    p = sub.add_parser("validate", help="waliduje pliki KB: schemat (L0), tożsamość i referencje (L1), provenance")
    p.add_argument("paths", nargs="+", metavar="ścieżka", help="plik YAML albo katalog (przeszukiwany rekurencyjnie)")
    p.add_argument("--json", action="store_true", help="raport jako JSON (lista diagnostyk)")
    p.set_defaults(func=_cmd_validate)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Polish messages on a cp1250/cp852 Windows console
    except (AttributeError, ValueError, OSError):
        pass
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
