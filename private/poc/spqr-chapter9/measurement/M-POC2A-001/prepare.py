"""One-session source preparation; no inference or evaluation-content reads."""
from pathlib import Path
import hashlib
import json
import math
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone

import pdfplumber
from PIL import Image
import PIL

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = Path(__file__).resolve().parent
I = P / 'inputs/v1'
DPI = 200

def now():
    return datetime.now(timezone.utc).isoformat()

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def record(path, base=ROOT):
    data = path.read_bytes()
    return {'path': path.relative_to(base).as_posix(), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        if isinstance(value, str):
            f.write(value)
        else:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write('\n')

def verify(items, base=ROOT):
    for item in items:
        path = base / item['path']
        actual = record(path, base)
        assert actual == {k: item[k] for k in ('path', 'sha256', 'bytes')}, path

def baseline():
    assert not I.exists(), 'Do not overwrite an existing input version'
    freeze = load(P / 'evaluation/freeze-public-v1.json')
    assert freeze['frozen'] and freeze['scope_approved'] and freeze['freeze_authorized']
    manifest_path = P / 'evaluation/eval-v1/manifest.json'
    manifest = load(manifest_path)
    assert record(manifest_path)['sha256'] == freeze['manifest_sha256']
    verify(manifest['artifacts'] + [manifest['source'], manifest['owner_scope_decision'], manifest['owner_freeze_decision']])
    protected = [record(path) for path in sorted(P.rglob('*')) if path.is_file() and not path.is_relative_to(M)]
    protected += [record(path) for path in sorted((ROOT / 'docs/handoff').glob('*.md'))]
    protected += [record(ROOT / '.git/index')]
    write(M / 'baseline.json', {'recorded_at_utc': now(), 'files': protected, 'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'freeze': record(P / 'evaluation/freeze-public-v1.json'), 'bootstrap_before_first_clock': True})
    print('Baseline:', len(protected), 'protected files; freeze hashes verified')

def generate():
    source = load(P / 'source/source-v1.json')
    pdf_path = P / 'source/original-pdf-20261008-01.pdf'
    assert record(pdf_path)['sha256'] == source['source']['sha256']
    (I / 'pages').mkdir(parents=True, exist_ok=False)
    (I / 'regions').mkdir()
    command = ['pdftoppm', '-f', '31', '-l', '37', '-r', str(DPI), '-png', str(pdf_path), str(I / 'pages/pdf')]
    rendered = subprocess.run(command, capture_output=True, text=True, check=True)
    write(M / 'render-log.txt', rendered.stdout + rendered.stderr)
    renderer = subprocess.run(['pdftoppm', '-v'], capture_output=True, text=True, check=True)
    entries = []
    with pdfplumber.open(pdf_path) as pdf:
        assert len(pdf.pages) == source['source']['page_count']
        for n in range(31, 38):
            page = pdf.pages[n-1]
            assert (page.width, page.height) == (612, 792)
            regions = []
            if n == 31:
                regions = [('context-left', [45, 45, 297, 744], 'context'), ('context-right-before-9', [315, 45, 567, source['scope']['start']['core_bbox'][1]], 'context'), ('core-right', source['scope']['start']['core_bbox'], 'core')]
            elif n == 37:
                regions = [('core-left', source['scope']['end']['core_bbox'], 'core'), ('context-left-from-10', [45, source['scope']['end']['core_bbox'][3], 297, 744], 'context'), ('context-right', [315, 45, 567, 744], 'context')]
            else:
                regions = [('core-left', [45, 45, 297, 744], 'core'), ('core-right', [315, 45, 567, 744], 'core')]
            full_path = I / f'pages/pdf-{n}.png'
            with Image.open(full_path) as full:
                assert full.size == (1700, 2200)
                for label, bbox, role in regions:
                    pixels = [math.floor(bbox[0]*DPI/72), math.floor(bbox[1]*DPI/72), math.ceil(bbox[2]*DPI/72), math.ceil(bbox[3]*DPI/72)]
                    crop_path = I / f'regions/pdf-{n}-{label}.png'
                    assert not crop_path.exists()
                    full.crop(pixels).save(crop_path)
                    clipped = page.crop(tuple(bbox), strict=True)
                    text = clipped.extract_text(x_tolerance=2, y_tolerance=3) or ''
                    entries.append({'region_id': f'pdf-{n}-{label}', 'pdf_page': n, 'printed_page': str(n), 'role': role, 'pdf_bbox': bbox, 'pixel_bbox_on_full_page': pixels, 'image': crop_path.relative_to(P).as_posix(), 'image_sha256': record(crop_path)['sha256'], 'text': text})
    core = [entry for entry in entries if entry['role'] == 'core']
    context = [entry for entry in entries if entry['role'] == 'context']
    assert len(core) == 12 and len(context) == 4
    assert core[0]['text'].startswith('9.0') and '10.0 ROUT' not in core[-1]['text']
    scope = {'source_id': source['id'], 'source_sha256': source['source']['sha256'], 'source_page_count': 44, 'pdf_pages': list(range(31,38)), 'printed_labels': list(range(31,38)), 'coordinate_system': 'PDF points; top-left origin; x right, y down; page 612 x 792 pt; bounding boxes [x0,y0,x1,y1]', 'full_image_coordinates': 'pixels; top-left origin; x right, y down; 1700 x 2200 px at 200 dpi', 'reading_order': [entry['region_id'] for entry in core], 'core_start': source['scope']['start'], 'core_end': source['scope']['end'], 'regions': [{k:v for k,v in e.items() if k != 'text'} for e in entries], 'authority': 'Full-page renders preserve graphics, column gutters and all fine detail. Region crops are locators; consult full page for any object crossing a crop. Only core regions are extraction targets. Other boundary regions are supplied context and never core coverage.', 'auxiliary_text_limitations': 'Automatic pdfplumber text, not manually corrected. Hyphenation, typography, numbers, tables and diagram labels may be misordered or absent. Verify against renders; do not infer missing glyphs.'}
    write(I / 'scope.json', scope)
    write(I / 'helper-regions.json', {'source_id': source['id'], 'source_sha256': source['source']['sha256'], 'coordinate_system': scope['coordinate_system'], 'method': 'pdfplumber page.crop(...).extract_text(x_tolerance=2,y_tolerance=3)', 'regions': entries})
    def combined(items, role):
        return f'AUXILIARY TEXT ONLY / {role.upper()} / verify renders\n\n' + '\n\n'.join(f"[{e['region_id']} | PDF {e['pdf_page']} | {role} | bbox={e['pdf_bbox']}]\n{e['text']}" for e in items) + '\n'
    write(I / 'helper-core.txt', combined(core, 'core'))
    write(I / 'helper-boundary-context.txt', combined(context, 'context'))
    shutil.copyfile(P / 'evaluation/freeze-public-v1.json', I / 'freeze-public-v1.json')
    write(M / 'tools.json', {'python': sys.version, 'python_executable': sys.executable, 'platform': platform.platform(), 'pdfplumber': pdfplumber.__version__, 'Pillow': PIL.__version__, 'renderer': renderer.stderr + renderer.stdout, 'render_command': command, 'dpi': DPI, 'created_at_utc': now()})
    print('Generated: 7 full-page renders, 12 core and 4 boundary-context crops; helper text and scope')

def seal():
    assert not (I / 'manifest.json').exists()
    files = sorted([path for path in I.rglob('*') if path.is_file() and path.name not in {'manifest.json', 'transfer-list.txt'}] + [P / 'formats/proposal-format-v1.md', P / 'formats/synthetic-example-v1.json', P / 'prompts/first-v1.txt'])
    transfer_paths = ['inputs/v1/manifest.json', 'inputs/v1/transfer-list.txt'] + [path.relative_to(P).as_posix() for path in files]
    write(I / 'transfer-list.txt', '\n'.join(transfer_paths) + '\n')
    files.append(I / 'transfer-list.txt')
    write(I / 'manifest.json', {'id': 'SPQR-ch9-inputs-v1', 'run_id': 'first-001', 'created_at_utc': now(), 'source_id': 'SPQR-5E-ch9-source-v1', 'source_sha256': load(I / 'scope.json')['source_sha256'], 'evaluation_id': 'eval-v1', 'evaluation_manifest_sha256': load(I / 'freeze-public-v1.json')['manifest_sha256'], 'format_version': 'proposal-format-v1', 'path_base': 'package root containing inputs/, formats/, prompts/', 'page_scope': [31,37], 'additional_pages': 0, 'tools': {k:v for k,v in load(M / 'tools.json').items() if k not in {'render_command', 'python_executable'}}, 'artifacts': [record(path, P) for path in files], 'manifest_self_hash_policy': 'Manifest SHA-256 is recorded in the separate handoff and measurement seal, not recursively in itself.', 'scope_policy': 'Extract only core regions in scope.json. Boundary context is evidence only and never core inventory.', 'transfer_state': 'prepared_not_sent', 'evaluation_content_included': False, 'full_44_page_pdf_included': False})
    export = P / 'transfer/first-v1'
    export.mkdir(parents=True, exist_ok=False)
    for relative in transfer_paths:
        destination = export / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(P / relative, destination)
    write(M / 'package-seal.json', {'created_at_utc': now(), 'manifest': record(I / 'manifest.json'), 'transfer_list': record(I / 'transfer-list.txt'), 'export_root': export.relative_to(ROOT).as_posix(), 'files': [record(P / r, P) for r in transfer_paths], 'file_count': len(transfer_paths), 'total_bytes': sum((P / r).stat().st_size for r in transfer_paths), 'sent_to_extractor': False, 'inference_performed': False})
    print('Sealed and copied isolated package:', len(transfer_paths), 'files')

def audit():
    verify(load(M / 'baseline.json')['files'])
    manifest = load(I / 'manifest.json')
    verify(manifest['artifacts'], P)
    seal_record = load(M / 'package-seal.json')
    verify(seal_record['files'], P)
    export = ROOT / seal_record['export_root']
    verify(seal_record['files'], export)
    allowed = set((I / 'transfer-list.txt').read_text(encoding='utf-8').splitlines())
    assert {p.relative_to(export).as_posix() for p in export.rglob('*') if p.is_file()} == allowed
    assert all(not p.is_symlink() for p in export.rglob('*'))
    assert not any(part in {'evaluation', 'source', 'measurement', 'reports', 'reviews', 'runs'} for p in allowed for part in Path(p).parts)
    for relative in allowed:
        if Path(relative).suffix in {'.json', '.md', '.txt'} and Path(relative).name != 'freeze-public-v1.json':
            body = (export / relative).read_text(encoding='utf-8')
            assert not any(token in body for token in ('EXP-002', 'RQ-15e', 'SIT-07', 'review-catalog-final', 'owner-review-002', 'eval-v1-candidate'))
    freeze = load(export / 'inputs/v1/freeze-public-v1.json')
    assert set(freeze) == {'evaluation_id','frozen','frozen_at_utc','scope_approved','freeze_authorized','manifest_sha256','manifest_bytes','artifact_hashes','source_sha256','owner_scope_decision_id','owner_freeze_decision_id'}
    assert (export / 'inputs/v1/freeze-public-v1.json').read_bytes() == (P / 'evaluation/freeze-public-v1.json').read_bytes()
    write(M / 'artifact-audit.json', {'recorded_at_utc': now(), 'protected_files_unchanged': len(load(M / 'baseline.json')['files']), 'manifest_and_export_hashes_valid': True, 'exact_allowlist_export': True, 'no_symlinks': True, 'source_only_derivation': True, 'evaluation_metadata_only': True, 'private_evaluation_identifiers_scan': 'passed', 'scan_limitation': 'String scan is supplementary; main isolation proof is PDF-only derivation and exact allowlist, without copied assessment artifacts.', 'core_regions': 12, 'context_regions': 4, 'full_renders': 7, 'additional_pages': 0, 'sent': False, 'inference': False})
    print('Audit passed; baseline, input/export hashes and transfer isolation verified')

if __name__ == '__main__':
    {'baseline': baseline, 'generate': generate, 'seal': seal, 'audit': audit}[sys.argv[1]]()
