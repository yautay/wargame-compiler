"""Bounded R01 report-only repair. Never write a prior attempt."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
OLD = ROOT / 'private/workflow/runs/IG-2B03/continuation-search-20261015-01'
SESSION = ROOT / 'private/workflow/orchestrator/20261015T175019Z-9761be5b/001-IG-2B03-executor-1dcc40e4'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


META = {key: load(RUN / 'claim.json')[key] for key in
        ['role', 'actor', 'task', 'model', 'reasoning',
         'configuration_evidence', 'configuration_sha256']}


def write(name, value):
    with (RUN / name).open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


# Inclusion: explicit rule/option citations, directional citations and labeled
# phase destinations. Ordinary mentions of gameplay terms are not new citations.
# Existing numeric citations and their associated names remain unchanged.
ADDITIONS = {
    'spqr5e:p11:492-bullet-3': ['Stacking rules'],
    'spqr5e:p11:50-introduction': ['Momentum rule', 'Trump Option'],
    'spqr5e:p12:528-item-2': ['Phase A'],
    'spqr5e:p12:528-closing': ['Rout and Reload Phase (D)'],
    'spqr5e:p12:53-play-note': ['Trumping, below'],
    'spqr5e:p12:532': ['Orders Phase (Phase B)'],
    'spqr5e:p12:533-bullet-9': ['Rout and Reload Phase (D)'],
}


def main():
    ledger = load(OLD / 'region-ledger.json')
    continuation = load(OLD / 'continuations.json')
    baseline_ledger = copy.deepcopy(ledger)
    baseline_continuation = copy.deepcopy(continuation)
    changes = []
    all_rows = []
    for row in ledger['regions']:
        region = row['region']
        assert row['pdf_page'] in [9, 10, 11, 12]
        additions = ADDITIONS.get(region['key'], [])
        raw_text = row['raw_extracted_text']
        collapsed = ' '.join(raw_text.split())
        offsets = []
        for literal in additions:
            assert literal in collapsed, (region['key'], literal)
            assert literal not in row['raw_cross_references']
            # Existing pinned extraction bytes are used, without new extraction.
            text_path = ROOT / row['evidence']['text']['path']
            assert pin(text_path) == row['evidence']['text']
            text = text_path.read_text(encoding='utf-8')
            assert text == raw_text
            start = text.find(literal)
            # Preserve exact source line wrapping when a name crosses a line.
            if start < 0:
                pieces = literal.split()
                start = text.index(pieces[0])
                end = start
                for piece in pieces:
                    at = text.index(piece, end)
                    assert not text[end:at].strip()
                    end = at + len(piece)
            else:
                end = start + len(literal)
            assert ' '.join(text[start:end].split()) == literal
            offsets.append({'literal': literal, 'start': start, 'end': end,
                            'unit': 'unicode_codepoints', 'bounds': 'half_open',
                            'exact_text_slice': text[start:end]})
        if additions:
            row['raw_cross_references'].extend(additions)
            existing = next((item for item in continuation['unfollowed_references']
                             if item['region_id'] == region['id']), None)
            if existing is None:
                continuation['unfollowed_references'].append(
                    {'region_id': region['id'], 'raw': list(additions)})
            else:
                existing['raw'].extend(additions)
            changes.append({'pdf_page': row['pdf_page'], 'region_id': region['id'],
                            'region_key': region['key'],
                            'region_revision': region['revision'],
                            'box': region['box'], 'page_basis_hash': row['page_basis_hash'],
                            'evidence_id': row['evidence']['id'],
                            'text_artifact': row['evidence']['text'],
                            'additions': additions, 'text_offsets': offsets,
                            'basis': 'Literal visible on the assigned original page and retained in existing pinned text; unresolved and unfollowed.'})
        all_rows.append({'pdf_page': row['pdf_page'], 'region_id': region['id'],
                         'region_key': region['key'],
                         'existing_references': baseline_ledger['regions'][len(all_rows)]['raw_cross_references'],
                         'added_references': additions,
                         'audit_result': 'Added explicit literal unresolved reference(s).' if additions else
                         'No further omitted explicit named citation observed on the original page.'})
    assert len(ledger['regions']) == 135
    assert len(changes) == len(ADDITIONS) == 7
    assert sum(len(change['additions']) for change in changes) == 8
    target = next(row for row in ledger['regions']
                  if row['region']['key'] == 'spqr5e:p11:492-bullet-3')
    assert target['region']['id'] == 'region:e9d78c99-a171-42c6-89f1-fe09b46c47e6'
    assert 'as per the\nStacking rules.' in target['raw_extracted_text']

    # Compare complete structures after stripping only additions. No geometry,
    # evidence, reading order, continuation, denominator or inventory edit.
    stripped = copy.deepcopy(ledger)
    for row in stripped['regions']:
        additions = ADDITIONS.get(row['region']['key'], [])
        if additions:
            assert row['raw_cross_references'][-len(additions):] == additions
            del row['raw_cross_references'][-len(additions):]
    assert stripped == baseline_ledger
    stripped_cont = copy.deepcopy(continuation)
    added_ids = {change['region_id'] for change in changes}
    stripped_cont['unfollowed_references'] = [item for item in
        stripped_cont['unfollowed_references'] if item['region_id'] not in added_ids]
    assert stripped_cont == baseline_continuation

    # New report provenance belongs to this observed executor. Historical visual
    # boundary assertions are not reissued: this repair audited references only.
    provenance = {'baseline': pin(OLD / 'region-ledger.json'),
                  'supersedes_only': 'raw_cross_references report index',
                  'scope': 'R01 literal reference-index additions only; unchanged boundary observations are preserved baseline data, not new boundary review claims.'}
    ledger.update(META)
    ledger['repair_provenance'] = provenance
    continuation.update(META)
    continuation['repair_provenance'] = {
        'baseline': pin(OLD / 'continuations.json'),
        'supersedes_only': 'unfollowed_references report index',
        'scope': 'All literal continuations, links, range boundaries and within-page order unchanged.'}
    write('region-ledger.json', ledger)
    write('continuations.json', continuation)
    scope = load(ROOT / 'private/workflow/runs/IG-2B03/preparation-r01-f684f3e2/repair-scope.json')
    write('reference-audit.json', {
        **META, 'format': 'wgc-reference-index-audit-1', 'finding': 'R01',
        'assigned_physical_pages': [9, 10, 11, 12],
        'original_page_images_inspected': scope['source_access']['existing_original_page_images'],
        'inspection': 'Executor visually inspected both columns, notes, exceptions, examples, counter areas, headings and editorial areas on each complete original assigned page for explicit named citations. Existing 135 region reference lists were compared in page reading order. This audit does not renew all prior boundary or semantic reviews.',
        'inclusion_policy': 'Literal rule/option citations, explicit directional citations and labeled phase destinations. Ordinary gameplay-term occurrences are not treated as citations. Existing numeric citations and associated names are retained. No number or target is inferred and no citation is followed.',
        'page_results': [
            {'pdf_page': 9, 'result': 'The two Line Command Eligibility Chart references are already indexed; no further omitted explicit named citation observed.'},
            {'pdf_page': 10, 'result': 'Leader Casualty Table is already indexed; ordinary Leader Casualty and humor rule mentions are not explicit named source citations. No further omitted explicit named citation observed.'},
            {'pdf_page': 11, 'result': 'Add Stacking rules, Momentum rule and Trump Option. Existing numeric exception references remain unchanged.'},
            {'pdf_page': 12, 'result': 'Add explicit labeled phase destinations and Trumping, below. Numeric citations and associated names remain unchanged.'}],
        'changes': changes, 'region_audit': all_rows,
        'changed_regions': 7, 'added_literals': 8, 'regions_audited': 135,
        'source_access_outside_assigned_pages': False,
        'new_extraction_or_rendering': False,
        'different_defect_found': False,
        'full_structure_comparison_except_reference_additions_and_provenance': True,
        'repaired_reports': [pin(RUN / 'region-ledger.json'), pin(RUN / 'continuations.json')],
        'semantic_acceptance_granted': False})
    print('Repaired 7 report rows with 8 literal unresolved references; full non-index structures preserved.')


if __name__ == '__main__':
    main()
