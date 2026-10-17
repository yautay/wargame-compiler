"""Read only the recorded incident crop; emit line geometry, never note text."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
tool = json.loads((ROOT / 'private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/toolchain.json').read_text(encoding='utf-8-sig'))
import os
sys.path.extend(tool['process_pythonpath'].split(os.pathsep))
import pdfplumber

rel = 'private/workflow/runs/IG-2B08/inventory-8d84cd90-01/original-pages/page-33-upper-edge/original-crop.pdf'
with pdfplumber.open(ROOT / rel) as pdf:
    page = pdf.pages[0]
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
    print(json.dumps({'width': page.width, 'height': page.height,
                      'first_three_line_geometry': lines[:3]}, indent=2))
