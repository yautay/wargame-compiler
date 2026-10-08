"""CLI: `python -m wgc validate <ścieżki…> [--json]`, `python -m wgc source init|scan|extract|verify|render` and
`python -m wgc kb recover [--dry-run]` and `python -m wgc desktop export` (also installed as `wgc`)."""
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
        elif args.source_command == "render":
            messages = source.render(args.root, args.doc, args.segment, args.pages, args.scale)
        elif args.source_command == "hybrid":
            from wgc.ingest.pdf_hybrid import CodexProvider, CommandProvider, ReplayProvider
            if args.prepare:
                messages = source.hybrid_prepare(args.root, args.doc)
            else:
                provider = (ReplayProvider(args.replay_dir) if args.replay_dir else
                            CodexProvider() if args.codex else CommandProvider(args.provider_exe))
                messages = source.hybrid(args.root, args.doc, provider)
        else:
            messages = source.extract(args.root)
    except source.SourceError as e:
        print(f"BŁĄD: {e}", file=sys.stderr)
        return 2
    for m in messages:
        print(m)
    return 0


def _cmd_kb(args) -> int:
    from wgc import kb
    try:
        rec = kb.recover(args.root, dry_run=args.dry_run)
    except kb.KBError as e:
        print(f"BŁĄD: {e}", file=sys.stderr)
        return 2
    if not rec.actions:
        print("kb/ bez przerwanej partii: nic do zrobienia.")
        return 0
    what = {"orphan": "przerwane przygotowanie partii", "rollback": "wycofanie do starej treści",
            "forward": "dokończenie zatwierdzonej partii", "clean": "pliki tymczasowe"}[rec.state]
    print(("Plan recovery (bez zapisu): " if args.dry_run else "Recovery kb/: ") + what
          + (f", job {rec.job}" if rec.job else ""))
    for a in rec.actions:
        print(f"  {a}")
    print("Niczego nie zapisano." if args.dry_run else "kb/ jest w całości stara albo w całości nowa.")
    return 0


def _cmd_desktop(args) -> int:
    from pathlib import Path
    from wgc.desktop_export import ExportError, export_package, parse_pages
    try:
        context = None if args.context is None else [] if args.context == "none" else parse_pages(args.context)
        package = export_package(Path(args.pdf), Path(args.output), doc=args.doc,
                                 target_pages=parse_pages(args.pages), context_pages=context, scale=args.scale)
    except ExportError as error:
        print(f"BŁĄD: {error}", file=sys.stderr)
        return 2
    print(f"Pakiet: {Path(args.output).resolve()}\nID: {package['id']}\nHash: {package['hash']}")
    print(f"Strony docelowe: {package['target_pages']}; kontekst: {package['context_pages']}.")
    print("Dołącz manifest.txt i pliki z assets ręcznie w aplikacji; zapisz odpowiedź poza pakietem.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wgc", description="wargame-compiler: narzędzia domenowe (WGC).")
    sub = parser.add_subparsers(dest="command", required=True, metavar="polecenie")
    p = sub.add_parser("validate", help="waliduje pliki KB: schemat (L0), tożsamość i referencje (L1), provenance")
    p.add_argument("paths", nargs="+", metavar="ścieżka", help="plik YAML albo katalog (przeszukiwany rekurencyjnie)")
    p.add_argument("--json", action="store_true", help="raport jako JSON (lista diagnostyk)")
    p.set_defaults(func=_cmd_validate)

    p = sub.add_parser("desktop", help="jawna wymiana plików z aplikacją desktopową (bez inferencji)")
    dsub = p.add_subparsers(dest="desktop_command", required=True)
    d = dsub.add_parser("export", help="eksportuje wybrane strony PDF i osobny kontekst do nowego katalogu")
    d.add_argument("--pdf", required=True, metavar="plik", help="oryginalny PDF (nie jest dołączany do pakietu)")
    d.add_argument("--doc", required=True, metavar="SRC-id", help="jawne ID źródła, bez modyfikacji inwentarza")
    d.add_argument("--pages", required=True, metavar="zakres", help="strony docelowe, np. 1-2 albo 3,5")
    d.add_argument("--context", metavar="zakres|none", help="osobny kontekst; domyślnie bezpośredni sąsiedzi")
    d.add_argument("--output", required=True, metavar="nowy-katalog", help="nowy katalog pakietu (bez nadpisywania)")
    d.add_argument("--scale", type=float, default=2.0, help="skala PNG: 0.1–4, domyślnie 2 (144 dpi)")
    p.set_defaults(func=_cmd_desktop)

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
    s = ssub.add_parser("hybrid", parents=[common], help="jawny hybrydowy ingest PDF z propozycją stron i kontrolami")
    s.add_argument("--doc", required=True, metavar="SRC-id", help="dokument PDF z inwentarza")
    provider = s.add_mutually_exclusive_group(required=True)
    provider.add_argument("--replay-dir", metavar="katalog", help="pliki p001.json itd. z propozycjami stron")
    provider.add_argument("--provider-exe", metavar="program", help="program JSON stdin/stdout wywołujący LLM")
    provider.add_argument("--codex", action="store_true", help="używa zalogowanego Codex CLI bez osobnego klucza API")
    provider.add_argument("--prepare", action="store_true", help="eksportuje słowa i rendery do pracy asystenta w Codex/Claude Desktop")
    s = ssub.add_parser("verify", parents=[common], help="sprawdza inwentarz, hashe plików i segmentów oraz cache tekstu")
    s.add_argument("--json", action="store_true", help="raport jako JSON (lista diagnostyk)")
    s = ssub.add_parser("render", parents=[common],
                        help="renderuje strony PDF do .glu/source/<SRC-id>/pages/ (ręczna weryfikacja ekstrakcji)")
    s.add_argument("--doc", metavar="SRC-id", help="dokument PDF z inwentarza")
    s.add_argument("--segment", metavar="SEG-id", help="segment: renderuje jego strony (pole pages)")
    s.add_argument("--pages", metavar="zakres", help="strony, np. 3, 3-4 albo 1,3-4 (domyślnie strony segmentu "
                                                    "albo cały dokument)")
    s.add_argument("--scale", type=float, default=2.0, help="skala renderu, 1.0 = 72 dpi (domyślnie 2.0)")
    p.set_defaults(func=_cmd_source)

    p = sub.add_parser("kb", help="kb/ repo gry: recovery przerwanej partii zapisu (ADR-0031)")
    ksub = p.add_subparsers(dest="kb_command", required=True, metavar="podpolecenie")
    s = ksub.add_parser("recover", parents=[common], help="kończy albo wycofuje przerwaną partię plików kb/")
    s.add_argument("--dry-run", action="store_true", help="tylko plan; niczego nie zapisuje")
    p.set_defaults(func=_cmd_kb)
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
