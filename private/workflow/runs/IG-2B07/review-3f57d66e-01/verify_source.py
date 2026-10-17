"""Independent scoped original renders and complete serial evidence replays."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

R = Path(__file__).parent
A = Path('private/workflow/runs/IG-2B07/inventory-25-28-01')
S = Path('private/workflow/orchestrator/20261016T195516Z-332903f5/003-IG-2B07-reviewer-3f57d66e')
TASK = json.loads((S / 'task.json').read_text())
SOURCE = TASK['source_scope']['source_pdf']
META = {k: v for k, v in json.loads((R / 'checkpoint.json').read_text()).items() if k in ('role', 'actor', 'model', 'reasoning', 'configuration_evidence', 'configuration_sha256')}

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(p, value):
    Path(p).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

def render(reader, number, box, prefix, dpi=144):
    writer = PdfWriter()
    page = writer.add_page(reader.pages[number - 1])
    x0, y0, x1, y1 = box
    bounds = [612*x0/1000000, 792*(1-y1/1000000), 612*x1/1000000, 792*(1-y0/1000000)]
    page.mediabox = RectangleObject(bounds)
    page.cropbox = RectangleObject(bounds)
    with prefix.with_suffix('.pdf').open('xb') as f:
        writer.write(f)
    command = ['pdftoppm', '-f', '1', '-l', '1', '-singlefile', '-cropbox', '-r', str(dpi), '-png', str(prefix.with_suffix('.pdf')), str(prefix)]
    subprocess.run(command, check=True, capture_output=True)
    return command

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['originals', 'replay-1', 'replay-2'])
    mode = parser.parse_args().mode
    assert sha(SOURCE['path']) == SOURCE['sha256']
    reader = PdfReader(SOURCE['path'], strict=True)
    output = R / mode
    output.mkdir(exist_ok=False)
    results = []
    if mode == 'originals':
        originals = json.loads((A / 'original-page-inspection.json').read_text())['originals']
        for old in originals:
            if not old['path'].endswith('.png'):
                continue
            prefix = output / ('page-' + str(old['physical_page']))
            command = render(reader, old['physical_page'], old['box'], prefix)
            results.append({'page': old['physical_page'], 'box': old['box'], 'command': command, 'sha256': sha(prefix.with_suffix('.png')), 'frozen_image_equal': sha(prefix.with_suffix('.png')) == old['sha256']})
        render(reader, 28, [695000, 272000, 738000, 301000], output / 'p28-after-b-upper-arrow', 576)
        assert all(x['frozen_image_equal'] for x in results)
    else:
        rows = json.loads((A / 'region-ledger.json').read_text())['regions']
        assert len(rows) == 188 and len({x['region']['id'] for x in rows}) == 188
        for i, row in enumerate(rows, 1):
            prefix = output / row['key'].replace(':', '-')
            command = render(reader, row['page'], row['box'], prefix)
            with pdfplumber.open(prefix.with_suffix('.pdf')) as pdf:
                text = pdf.pages[0].crop(pdf.pages[0].bbox).extract_text(x_tolerance=3, y_tolerance=3, layout=False) or ''
            prefix.with_suffix('.txt').write_text(text, encoding='utf-8', newline='\n')
            result = {'id': row['region']['id'], 'key': row['key'], 'category': row['category'], 'command': command, 'exit_code': 0, 'payloads': {}}
            for suffix, field in [('.pdf', 'crop_pdf'), ('.txt', 'text'), ('.png', 'image')]:
                actual = sha(prefix.with_suffix(suffix))
                result['payloads'][field] = {'path': prefix.with_suffix(suffix).as_posix(), 'sha256': actual, 'frozen_equal': actual == row['evidence'][field]['sha256']}
            results.append(result)
            if i % 20 == 0:
                print(f'{mode}: {i}/188', flush=True)
        assert all(p['frozen_equal'] for x in results for p in x['payloads'].values())
    assert sha(SOURCE['path']) == SOURCE['sha256']
    write(R / (mode + '-verification.json'), dict(META, mode=mode, source=SOURCE, results=results, all_passed=True, serial=True))
    print(mode + ': all complete source payloads match frozen delivery', flush=True)

if __name__ == '__main__':
    main()
