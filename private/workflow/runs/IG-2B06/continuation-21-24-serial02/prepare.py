"""Task-owned fresh continuation assembly and original-page geometry audit."""
import copy
import json
from pathlib import Path

import pdfplumber
from PIL import Image, ImageDraw
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import assemble, validate, file_pin

ROOT = Path.cwd()
OUT = Path('private/workflow/runs/IG-2B06/continuation-21-24-serial02')
SESSION = Path('private/workflow/orchestrator/20261016T182116Z-202cea4c/001-IG-2B06-executor-f2379326')
TASK = json.loads((SESSION / 'task.json').read_text())
CONTRACT = json.loads(Path(TASK['refinement_contract']['path']).read_text())
SCOPE = json.loads(Path(TASK['continuation_authorization']['scope']['path']).read_text())
BASE = json.loads(Path(CONTRACT['input_pins'][0]['path']).read_text())
REGISTRY = json.loads(Path(CONTRACT['input_pins'][1]['path']).read_text())
assert BASE['registry'] == REGISTRY
draft = json.loads(Path(SCOPE['drafts'][0]['path']).read_text())
draft_registry = json.loads(Path(SCOPE['drafts'][1]['path']).read_text())
candidate = json.loads(Path(SCOPE['drafts'][2]['path']).read_text())
assert draft['registry'] == draft_registry
assert draft['source'] == BASE['source'] and draft['pages'] == BASE['pages']
old_entries = {(e['kind'], e['key']): e['id'] for e in REGISTRY['entries']}
new_entries = {(e['kind'], e['key']): e['id'] for e in draft_registry['entries']}
assert all(new_entries[k] == v for k, v in old_entries.items())
targets = set(TASK['source_scope']['target_ids'])
pages = {p['id']: p['pdf_page'] for p in BASE['pages']}
chosen = [r for r in draft['regions'] if r['key'].startswith('ig2b06:')]
assert len(chosen) == 114
assert {r['id'] for r in chosen} == {r['region_id'] for r in candidate['regions']}
for r in chosen:
    if r['denominator_role'] == 'inventory':
        assert pages[r['page_id']] in [21, 22, 23, 24]
    else:
        assert (pages[r['page_id']], r['box']) in [(c['pdf_page'], c['box']) for c in CONTRACT['context_only_source_regions']]
    row = next(x for x in candidate['regions'] if x['region_id'] == r['id'])
    assert row['box'] == r['box'] and row['kind'] == r['kind']
    for component in row['components']:
        b, c = r['box'], component['box']
        assert b[0] <= c[0] < c[2] <= b[2] and b[1] <= c[1] < c[3] <= b[3]
retained = [r for r in BASE['regions'] if r['id'] not in targets]
order = []
selected_by_page = {n: [r['id'] for r in chosen if pages[r['page_id']] == n] for n in [21, 22, 23, 24]}
draft_order = draft['reading_order']
for n in selected_by_page:
    selected_by_page[n].sort(key=draft_order.index)
for rid in BASE['reading_order']:
    if rid in targets:
        old = next(r for r in BASE['regions'] if r['id'] == rid)
        order.extend(selected_by_page[pages[old['page_id']]])
    else:
        order.append(rid)
incoming = next(r['id'] for r in chosen if r['key'] == 'ig2b06:incoming-context')
outgoing = next(r['id'] for r in chosen if r['key'] == 'ig2b06:outgoing-context')
order.insert(order.index(selected_by_page[21][0]), incoming)
order.insert(order.index(selected_by_page[24][-1]) + 1, outgoing)
doc = assemble(BASE['source'], BASE['pages'], retained + chosen, draft_registry,
               reading_order=order, links=BASE['links'] + candidate['new_links'],
               evidence=BASE['evidence'], toolchain=BASE['toolchain'])
validate(doc, ROOT)
authored = OUT / 'authored'
authored.mkdir(exist_ok=False)
(authored / 'inventory.json').write_bytes(canonical_bytes(doc) + b'\n')
(authored / 'identity-registry.json').write_bytes(canonical_bytes(doc['registry']) + b'\n')
meta = {k: json.loads((OUT / 'claim.json').read_text())[k] for k in
        ('role','actor','model','reasoning','configuration_evidence','configuration_sha256','task')}
(OUT / 'author-regions.json').write_text(json.dumps({**meta, 'summary': 'Candidate regions revalidated against fresh original-page renders; no inherited inspection or checks.',
    'regions': candidate['regions'], 'new_links': candidate['new_links'],
    'coordinate_basis': 'Integer normalized half-open top-left page millionths',
    'semantic_acceptance': False, 'executable_readiness': False}, indent=2) + '\n', encoding='utf-8')

# Supplemental text-geometry check is independent of visual inspection. Source reads
# are limited to the four assigned pages; context is handled only through exact crops.
glyph_audit = []
with pdfplumber.open(BASE['source']['pdf']['path']) as pdf:
    for n in [21, 22, 23, 24]:
        page = pdf.pages[n - 1]
        regs = [r for r in chosen if pages[r['page_id']] == n]
        missing = []
        for char in page.chars:
            if char['text'].isspace():
                continue
            cx = (char['x0'] + char['x1']) / 2 / page.width * 1000000
            cy = (char['top'] + char['bottom']) / 2 / page.height * 1000000
            if not any(r['box'][0] <= cx < r['box'][2] and r['box'][1] <= cy < r['box'][3] for r in regs):
                missing.append({'text': char['text'], 'center_page_millionths': [round(cx), round(cy)]})
        glyph_audit.append({'pdf_page': n, 'nonspace_glyphs': sum(not c['text'].isspace() for c in page.chars), 'unassigned_glyph_centers': missing})
        image = Image.open(OUT / 'original-renders' / f'page-{n}.png').convert('RGB')
        draw = ImageDraw.Draw(image)
        for r in regs:
            b = r['box']; rect = [b[0]*image.width/1e6,b[1]*image.height/1e6,b[2]*image.width/1e6,b[3]*image.height/1e6]
            draw.rectangle(rect, outline='#cc2255', width=1)
        image.save(OUT / 'original-renders' / f'overlay-{n}.png')
(OUT / 'glyph-audit.json').write_text(json.dumps({**meta, 'summary': 'Supplemental glyph-center geometry audit; not a transcription or semantic acceptance.', 'pages': glyph_audit}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'authored_inventory': file_pin(ROOT, (authored / 'inventory.json').as_posix()), 'assigned_regions':112, 'context_regions':2, 'glyph_center_gaps': {p['pdf_page']:len(p['unassigned_glyph_centers']) for p in glyph_audit}}))
