import json
import subprocess
from collections import Counter
from pathlib import Path
from PIL import Image
from verify import ROOT, OLD, NEW, SESSION, read, pin, write

checks = []
for directory in ['final-verified', 'replay-a-verified', 'replay-b-verified', 'components', 'components-replay-a', 'components-replay-b']:
    command = ['.venv/Scripts/python.exe', '-B', '-m', 'wgc.sources', 'validate', (OLD/directory/'inventory.json').as_posix()]
    result = subprocess.run(command, capture_output=True)
    log = ROOT / ('root-' + directory + '.log')
    with log.open('xb') as f:
        f.write(result.stdout + result.stderr)
    assert result.returncode == 0, result.stderr.decode(errors='replace')
    data = json.loads(result.stdout)
    checks.append({'command':' '.join(command), 'exit_code':result.returncode, 'log':pin(log.relative_to(Path.cwd())) if log.is_absolute() else pin(log)})
    print(directory, 'validated', flush=True)

inventory = read(OLD/'final-verified/inventory.json')
inputs = read('private/workflow/runs/IG-2B03/preparation-003-e285fb76/input-pins.json')
baseline = read(inputs['files'][0]['path'])
assigned = {p['id'] for p in inventory['pages'] if p['pdf_page'] in [9,10,11,12]}
assert len(inventory['pages']) == len(baseline['pages']) == 44
for a,b in zip(baseline['pages'],inventory['pages'],strict=True):
    assert a == b or a['id'] in assigned
old_regions = {r['id']:r for r in baseline['regions']}
current_regions = {r['id']:r for r in inventory['regions']}
retired = [r['id'] for r in baseline['regions'] if r['page_id'] in assigned and r['denominator_role']=='inventory']
for rid,r in old_regions.items():
    if rid not in retired:
        assert current_regions[rid] == r
assert [r for r in inventory['evidence'] if r in baseline['evidence']] == baseline['evidence']
assert inventory['links'][:len(baseline['links'])] == baseline['links']
assert [rid for rid in inventory['reading_order'] if rid in old_regions] == [rid for rid in baseline['reading_order'] if rid not in retired]
def bindings(obj):
    # Compare persisted dictionaries recursively without interpreting source content.
    def subset(a,b):
        if isinstance(a,dict):
            return isinstance(b,dict) and all(k in b and subset(v,b[k]) for k,v in a.items())
        if isinstance(a,list):
            return isinstance(b,list) and all(x in b for x in a)
        return a==b
    return subset(obj['registry'], inventory['registry'])
assert bindings(baseline)
ledger = read(NEW/'region-ledger.json')
components = read(OLD/'component-ledger.json')
ids = {r['region']['id'] for r in ledger['regions']}
assert ids == {r['id'] for r in inventory['regions'] if r['page_id'] in assigned and r['denominator_role']=='inventory'}
locator_count = 0
for row in ledger['regions'] + components['components']:
    e = row['evidence']
    with Image.open(e['image']['path']) as image:
        pixels = list(image.size)
    assert pixels == row['actual_png_pixels'] == row['predicted_pixels']
    assert pixels == [e['render_parameters']['width_pixels'], e['render_parameters']['height_pixels']]
    text = Path(e['text']['path']).read_text(encoding='utf-8')
    offsets = e['text_offsets']
    assert len(text) == e['text_codepoints']
    assert offsets == {'start':0,'end':len(text),'unit':'unicode_codepoints','bounds':'half_open'}
    assert e['box'] == (row['region']['box'] if 'region' in row else row['box'])
    if 'raw_extracted_text' in row:
        assert text.strip() == row['raw_extracted_text']
    locator_count += 1
for row in ledger['regions']:
    assert current_regions[row['region']['id']] == row['region']
    assert all(v['status']=='unprocessed' and v['gap'] for v in row['region']['coverage'].values())
assert all(r['denominator_units']==0 for r in components['components'])
for dirname in ['replay-a-authored','replay-b-authored']:
    for filename in ['inventory.json','identity-registry.json']:
        assert (OLD/'authored'/filename).read_bytes() == (OLD/dirname/filename).read_bytes()
assert all(read(OLD/d/'identity-registry.json') == read(OLD/'final-verified/identity-registry.json') for d in ['replay-a-verified','replay-b-verified'])
write('validation.json', dict(format='wgc-independent-r01-validation-1', outcome='pass', checks=checks, locator_count=locator_count, task_region_count=len(ids), task_page_counts=dict(Counter(r['pdf_page'] for r in ledger['regions'])), accepted_nested_records_preserved=True, accepted_registry_bindings_and_retired_entries_preserved=True, prior_evidence_links_and_order_preserved=True, authored_replays_byte_identical=True, component_context_count=22, source_access='Six root structural validations open PDF geometry/counts only; no text/image extraction outside assigned pages.', semantic_acceptance_granted=False))
print('157 locators and exact prior scope preserved', flush=True)
