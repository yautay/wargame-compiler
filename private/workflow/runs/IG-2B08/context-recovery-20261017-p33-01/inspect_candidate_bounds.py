"""Measure only the incident rectangle, clipping before releasing characters."""
import hashlib
import json
from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[5]
tool = json.loads((ROOT / 'private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/toolchain.json').read_text(encoding='utf-8-sig'))
sys.path.extend(tool['process_pythonpath'].split(os.pathsep))
import pdfplumber

source = ROOT / 'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'
with source.open('rb') as f:
    assert hashlib.file_digest(f, 'sha256').hexdigest() == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
with pdfplumber.open(source) as pdf:
    page = pdf.pages[32].crop((45, 50, 306, 80), strict=True)
    lines = []
    for c in sorted(page.chars, key=lambda c: (round(c['top'], 1), c['x0'])):
        if not lines or abs(c['top'] - lines[-1]['top']) > 1:
            lines.append({'top': c['top'], 'bottom': c['bottom'], 'x0': c['x0'], 'x1': c['x1'], 'chars': 1})
        else:
            line = lines[-1]
            line['bottom'] = max(line['bottom'], c['bottom'])
            line['x0'] = min(line['x0'], c['x0'])
            line['x1'] = max(line['x1'], c['x1'])
            line['chars'] += 1
    print(json.dumps({'physical_page': 33, 'authorized_assessment_box': list(page.bbox),
                      'first_three_line_geometry': lines[:3]}, indent=2))
