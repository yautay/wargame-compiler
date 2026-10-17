"""Fresh task-owned deterministic rebuild from pinned baseline and explicit author data."""
import copy
import json
from pathlib import Path
import sys
import time

from wgc.sources.inventory import assemble, file_pin, make_region, seal, validate
from wgc.sources.pdf import extract_evidence

ROOT = Path('private/workflow/runs/IG-2B04/continuation-13-16-rg04')
CONTRACT = Path('private/workflow/runs/IG-2B04/rg-recovery-20261016-01/execution-contract.json')

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    mode = sys.argv[1]
    assert mode in ('final-verified', 'replay-a', 'replay-b')
    target = ROOT/mode
    assert not target.exists(), 'Fresh output directory required'
    contract = load(CONTRACT)
    for pin in contract['inputs'].values():
        assert file_pin(Path.cwd(), pin['path']) == pin
    baseline = load(contract['inputs']['baseline_inventory']['path'])
    registry = load(ROOT/'authored-registry.json')
    authored = load(ROOT/'authored-regions.json')['regions']
    pages = copy.deepcopy(baseline['pages'])
    by_page = {p['pdf_page']: p for p in pages}
    new = []
    for item in authored:
        region = make_region(registry, item['key'], by_page[item['pdf_page']], item['box'], kind=item['kind'],
                             reason='Source inventory only; no accepted descriptive or formal semantics.')
        region['uncertainty'] = ['Fresh visual inventory and machine extraction; no verified exact transcription or source-meaning acceptance.']
        region['coverage']['transcription'] = {
            'status': 'partial', 'gap': True, 'boundary': None,
            'reason': 'Complete visual component and machine text captured; exact transcription has not been independently verified.'}
        region = seal(region)
        assert region['id'] == item['id']
        new.append(region)
    retired = set(contract['target_ids'])
    assert {r['id'] for r in baseline['regions'] if r['id'] in retired} == retired
    regions = [r for r in baseline['regions'] if r['id'] not in retired] + new
    order = []
    for identity in baseline['reading_order']:
        if identity not in retired:
            order.append(identity)
        else:
            old = next(r for r in baseline['regions'] if r['id']==identity)
            order.extend(r['id'] for r in new if r['page_id']==old['page_id'])
    by_key = {r['key']:r['id'] for r in new}
    links = copy.deepcopy(baseline['links'])
    def link(kind, left, right, reason):
        links.append({'kind':kind,'from':by_key[left],'to':by_key[right],'reason':reason})
    for left,right in [
        ('b04:p13:5.44-opening','b04:p13:5.44-continuation'),
        ('b04:p13:example-5.53-start','b04:p14:example-5.53-end'),
        ('b04:p15:6.32-opening','b04:p15:6.32-phalanx'),
        ('b04:p15:6.51-start','b04:p16:6.51-continuation'),
        ('b04:p16:6.55-opening','b04:p16:6.55-mounted-archers')]:
        link('continuation',left,right,'Direct visible same-unit continuation within assigned pages; structural observation only.')
    for p,left,right in [
        (13,'design-note-trump','heading-5.4'), (13,'play-note-no-momentum','5.44-opening'),
        (13,'design-note-elite','heading-5.5'), (14,'design-note-movement','heading-6.1'),
        (14,'play-note-moved','6.13'),(14,'historical-note-terrain','heading-6.2'),
        (14,'play-note-terrain','6.22'),(14,'historical-note-cannae','6.24'),
        (15,'historical-note-phalanx','heading-6.4'),(15,'design-note-phalanx','heading-6.4'),
        (15,'play-note-withdrawal','6.5-intro'),(16,'play-note-two-hexes','6.51-continuation'),
        (16,'historical-note-withdrawal','6.52-intro'),(16,'play-note-6.55','6.55-opening')]:
        link('note_for',f'b04:p{p}:{left}',f'b04:p{p}:{right}','Visible note placement and label; no gameplay interpretation.')
    for p,left,right in [(13,'marker-no-momentum','5.44-opening'),(14,'marker-moved','play-note-moved'),
                         (15,'diagram-front-to-flank','6.43'),(16,'diagram-withdrawal','example-6.51-3')]:
        link('illustrates',f'b04:p{p}:{left}',f'b04:p{p}:{right}','Complete visible graphic associated with this assigned source component.')
    document = assemble(baseline['source'],pages,regions,registry,reading_order=order,links=links,
                        evidence=copy.deepcopy(baseline['evidence']),toolchain=baseline['toolchain'])
    # Cropping depends on source/page/region bases, not previously generated artifacts.
    # Validate that fixed full-page/full-region basis for each crop, then validate all
    # retained and regenerated evidence together in the complete final inventory.
    label_evidence = {p['label']['evidence'] for p in pages if p['label']['status']=='verified'}
    extraction_basis = assemble(baseline['source'],pages,regions,registry,reading_order=order,links=links,
                                evidence=[e for e in baseline['evidence'] if e['id'] in label_evidence],
                                toolchain=baseline['toolchain'])
    target.mkdir()
    evidence_root = ROOT/'evidence' if mode=='final-verified' else target/'evidence'
    start=time.monotonic()
    for i,region in enumerate(new,1):
        evidence=extract_evidence(extraction_basis,region['id'],Path.cwd(),(evidence_root/region['key'].replace(':','-')).as_posix(),dpi=144)
        document['evidence'].append(evidence)
        document=seal(document)
        if i%10==0 or i==len(new): print(f'{mode}: rebuilt {i}/{len(new)} regions ({time.monotonic()-start:.1f}s)',flush=True)
    report=validate(document,Path.cwd())
    write(target/'inventory.json',document)
    write(target/'identity-registry.json',registry)
    base={k:v for k,v in load(ROOT/'claim.json').items() if k not in ('summary','criteria','artifacts','checks','utc')}
    write(target/'build-report.json',{**base,'mode':mode,'assigned_regions':len(new),'elapsed_seconds':time.monotonic()-start,
        'independent_start':contract['inputs'],'inventory':file_pin(Path.cwd(),(target/'inventory.json').as_posix()),
        'registry':file_pin(Path.cwd(),(target/'identity-registry.json').as_posix()),'coverage':report,
        'source_meaning_acceptance':False})
    print(f'{mode}: complete and validated',flush=True)

if __name__=='__main__': main()
