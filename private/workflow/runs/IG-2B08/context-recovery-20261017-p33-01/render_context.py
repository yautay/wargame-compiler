"""Render only the corrected page-33 context rectangle for read-only assessment."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

prep = Path(__file__).resolve().parent
tool = w.read_json(ROOT / 'private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/toolchain.json')
sys.path.extend(tool['process_pythonpath'].split(os.pathsep))
import pdfplumber

source = ROOT / 'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'
assert w.digest(source) == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
box = [45, 50, 306, 80]
with pdfplumber.open(source) as pdf:
    page = pdf.pages[32].crop(tuple(box), strict=True)
    chars = page.chars
    assert chars and all(45 <= c['x0'] <= c['x1'] <= 306 and 50 <= c['top'] <= c['bottom'] <= 80 for c in chars)
    assert len({round(c['top'], 2) for c in chars}) == 2
    assert max(c['bottom'] for c in chars) < 77
    assert max(c['x1'] for c in chars) < 300
    text = page.extract_text(x_tolerance=3, y_tolerance=3, layout=False)
    assert len(text.splitlines()) == 2
with (prep / 'page-33-continuation-only.txt').open('x', encoding='utf-8', newline='\n') as f:
    f.write(text + '\n')
exe = shutil.which('pdftoppm', path=o.native_path_prefix(tool['process_path_prefix']) + os.pathsep + os.environ.get('PATH', ''))
assert exe
prefix = prep / 'page-33-continuation-only'
assert not prefix.with_suffix('.png').exists()
argv = [exe, '-f', '33', '-l', '33', '-singlefile', '-cropbox', '-r', '144',
        '-x', '90', '-y', '100', '-W', '522', '-H', '60', '-png', str(source), str(prefix)]
subprocess.run(argv, capture_output=True, check=True)
result = {'physical_page': 33, 'frame': 'unrotated effective crop top-left, PDF points',
    'box_points': box, 'box_normalized_outward': [73529, 63131, 500000, 101011],
    'source_sha256': w.digest(source), 'dpi': 144,
    'complete_continuation_lines': 2, 'continuation_max_right': max(c['x1'] for c in chars),
    'continuation_max_bottom': max(c['bottom'] for c in chars),
    'next_note_first_glyph_top': 84.507,
    'argv': argv, 'artifacts': []}
for name in ('page-33-continuation-only.png', 'page-33-continuation-only.txt'):
    p = prep / name
    result['artifacts'].append({'path': p.relative_to(ROOT).as_posix(), 'sha256': w.digest(p), 'bytes': p.stat().st_size})
with (prep / 'context-boundary-verification.json').open('x', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps({'box_points': box, 'line_count': 2, 'max_bottom': result['continuation_max_bottom'],
                  'next_note_first_glyph_top': 84.507, 'render': str(prefix.with_suffix('.png'))}))
