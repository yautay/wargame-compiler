"""Offline docket assembly; copies data and trace, never judges or changes answers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = Path(__file__).resolve().parent
OUT = P / 'reviews/semantic-01'
OUT.mkdir(exist_ok=True)
assert not (OUT / 'checklist.json').exists(), 'New docket only; do not overwrite review history'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ref(path):
    path = Path(path)
    data = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data))

def read(path):
    return json.loads((P / path).read_bytes())

def save(path, obj):
    assert not path.exists(), path
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def resolve(obj, pointer):
    for key in pointer.lstrip('/').split('/') if pointer else []:
        key = key.replace('~1', '/').replace('~0', '~')
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj

# Snapshot all protected trees before any docket assembly, including nonmanifest files.
trees = ['source', 'runs', 'proposals', 'reports', 'inputs', 'context', 'transfer', 'evaluation/eval-v1', 'reviews/context-source-01']
protected = [ref(f) for t in trees for f in sorted((P / t).rglob('*')) if f.is_file()]
sessions = (P / 'measurement/sessions.jsonl').read_bytes()
save(M / 'start.json', dict(id='M-POC5A.1-start', card='M-POC5A', part='M-POC5A.1',
    first_recorded_clock_utc='2026-10-10T18:24:51+00:00', bootstrap_start='unknown',
    recorded_at_utc=datetime.now(timezone.utc).isoformat(), protected=protected,
    sessions_before=dict(bytes=len(sessions), sha256=sha(sessions)),
    split_before_semantic_assessment=True, active_user_time='unknown', active_model_time='unknown',
    time_budget_compliance='unknown'))

required = ['source/source-v1.json', 'source/original-pdf-20261008-01.pdf',
    'inputs/v1/manifest.json', 'context/pass-01/manifest.json', 'context/pass-01/freeze-v1.json',
    'transfer/context-v1/context/pass-01/manifest.json', 'evaluation/eval-v1/manifest.json',
    'evaluation/eval-v1/expectations.json', 'evaluation/eval-v1/inventory.json',
    'evaluation/eval-v1/dependencies.json', 'evaluation/eval-v1/measurement-policy.json',
    'reports/context-01/context-comparison.json',
    'measurement/M-POC4B-context-01/report-reference-supplement.json',
    'reviews/context-source-01/decision-01.json', 'reviews/context-source-01/review-closure-01.json']
for run in ['first-001', 'context-01']:
    required += [f'runs/{run}/run.json', f'runs/{run}/session-evidence.txt',
                 f'proposals/{run}/proposal.json', f'proposals/{run}/provenance.json']
    required += [f'reports/{run}/{name}' for name in ['report.md', 'errors.json', 'inventory.json',
                 'metrics.json', 'dependency-comparison.json', 'manifest.json', 'closure.json', 'image-areas.json']]
required += ['runs/first-001/first-001.json', 'runs/context-01/response.raw.txt']
parsed = {f: read(f) for f in required if f.endswith('.json')}
# Read complete text evidence as data; PDF identity verified independently below.
for f in required:
    if f.endswith(('.md', '.txt')):
        (P / f).read_text(encoding='utf-8-sig')

checks = []
def check_manifest(path, list_key, base):
    manifest = read(path)
    for r in manifest[list_key]:
        actual = ref(base / r['path'])
        assert actual['sha256'] == r['sha256'] and actual['bytes'] == r['bytes'], (path, r['path'])
    checks.append(dict(manifest=path, entries=len(manifest[list_key]), result='byte_hash_match'))

check_manifest('evaluation/eval-v1/manifest.json', 'artifacts', ROOT)
check_manifest('inputs/v1/manifest.json', 'artifacts', P)
check_manifest('transfer/context-v1/context/pass-01/manifest.json', 'artifacts', P / 'transfer/context-v1')
check_manifest('context/pass-01/manifest.json', 'files', ROOT)
check_manifest('context/pass-01/freeze-v1.json', 'frozen_files', ROOT)
check_manifest('context/pass-01/freeze-v1.json', 'approved_source_files', ROOT)
for run in ['first-001', 'context-01']:
    check_manifest(f'reports/{run}/manifest.json', 'artifacts', ROOT)
assert ref(P / 'source/original-pdf-20261008-01.pdf')['sha256'] == read('source/source-v1.json')['source']['sha256']
expected = dict(first_001=(617941, '3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307'),
    context_01=(712014, '95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'))
run_data = {}
for run, raw_path in [('first-001', 'runs/first-001/first-001.json'), ('context-01', 'runs/context-01/response.raw.txt')]:
    data = (P / raw_path).read_bytes()
    assert (len(data), sha(data)) == expected[run.replace('-', '_')]
    proposal = read(f'proposals/{run}/proposal.json')
    assert data == (P / f'proposals/{run}/proposal.json').read_bytes()
    prov = read(f'proposals/{run}/provenance.json')
    for pointer, s in prov['json_value_spans'].items():
        fragment = data[s['start_byte']:s['end_byte_exclusive']]
        assert sha(fragment) == s['sha256'], (run, pointer)
        assert json.loads(fragment) == resolve(proposal, pointer), (run, pointer)
    records = {}
    for group in ['rules', 'nodes', 'dependencies', 'gaps', 'evidence']:
        for i, record in enumerate(proposal[group]):
            pointer = f'/{group}/{i}'
            records[record['id']] = dict(pointer=pointer, raw_span=prov['json_value_spans'][pointer], original_record=record)
    run_data[run] = dict(raw_response=ref(P / raw_path), proposal=proposal, provenance=prov,
        records=records, inventory=read(f'reports/{run}/inventory.json'),
        dependencies=read(f'reports/{run}/dependency-comparison.json'),
        errors=read(f'reports/{run}/errors.json'), areas=read(f'reports/{run}/image-areas.json'))
    checks.append(dict(run=run, verified_value_spans=len(prov['json_value_spans']), result='byte_hash_and_decoded_value_match'))

eval_ref = ref(P / 'evaluation/eval-v1/manifest.json')
assert eval_ref['sha256'] == '7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce'
exp = read('evaluation/eval-v1/expectations.json')['expectations']
inv = read('evaluation/eval-v1/inventory.json')['items']
policy = read('evaluation/eval-v1/measurement-policy.json')
deps = read('evaluation/eval-v1/dependencies.json')
assert len(exp) == 74 and len(inv) == 207
assert sum(e['classification'] == 'confirmed_local_content_scope' for e in exp) == 66
assert sum(e['classification'] == 'requires_context' for e in exp) == 8
run_refs = {run: d['raw_response'] for run, d in run_data.items()}
dimensions = dict(conditions='conditions', effect='action_effect', exceptions='exceptions',
    numbers_units='parameters', negation='exceptions', time='time_limits',
    table='content', diagram='content', note='content')

def state(run, source_scope, ids, uncertainty):
    return dict(response=run_refs[run], status='pending', result='not_assessable',
        reviewer=None, preparer='Codex; evidence assembly only', source_scope=source_scope,
        output_record_ids=ids, uncertainty=uncertainty,
        reason='No owner decision for this response hash and exact scope. Mapping and source support do not accept meaning.')

expectation_rows = []
for i, e in enumerate(exp):
    num = int(e['id'].split('-')[1])
    part = 'M-POC5A.2' if num <= 25 else 'M-POC5A.3' if num <= 50 else 'M-POC5A.4'
    row = dict(id=e['id'], evaluation_pointer=f'/expectations/{i}', assigned_part=part,
        classification=e['classification'], criticality=e['criticality'],
        source_scope=e['reviewed_scope'], source_evidence=e['evidence'], inventory_refs=e['inventory_refs'],
        authorizing_decisions=e['authorizing_scoped_decisions'], exclusions=e['unreviewed_fields'],
        limits=e['limits'], whole_record_gold=False, runs={}, dimensions={})
    for run, d in run_data.items():
        mapping = next(r for r in d['inventory']['expectations'] if r['id'] == e['id'])
        ids = mapping['mapped_output_ids']
        row['runs'][run] = state(run, e['reviewed_scope'], ids, e['limits'] + e['unreviewed_fields'])
        row['runs'][run]['structural_mapping'] = mapping
        row['runs'][run]['local_scope_not_automatically_blocked'] = True
        row['runs'][run]['extractor_gap_claims'] = [r for r in d['proposal']['gaps'] if set(r['affected_ids']) & set(ids)]
        row['dimensions'][run] = {dim: dict(status='pending', applicability='pending_exact_scope_review',
            source_evidence_refs=[v.get('inventory_ref') for v in e['evidence']],
            output_field_pointers=[d['records'][rid]['pointer'] + '/' + field for rid in ids if field in d['records'][rid]['original_record']],
            fallback_record_ids=ids, reason='Field locators are candidates; exact meaning/absence/applicability requires owner review.')
            for dim, field in dimensions.items()}
    expectation_rows.append(row)

inventory_rows = []
for i, item in enumerate(inv):
    related = [e['id'] for e in exp if item['id'] in e['inventory_refs']]
    row = dict(id=item['id'], evaluation_pointer=f'/items/{i}', type=item['type'],
        frozen_item=item, expectation_ids=related, assigned_part='associated expectation part; otherwise M-POC5A.4', runs={})
    for run, d in run_data.items():
        mapping = next(r for r in d['inventory']['items'] if r['inventory_id'] == item['id'])
        row['runs'][run] = state(run, item.get('evidence', []), mapping['output_ids'],
            ['No whole-record gold; parent mapping does not verify this child span.'])
        row['runs'][run]['structural_mapping'] = mapping
    inventory_rows.append(row)

rubrics = []
for category in policy['categories']:
    assert len(category['units']) == category['denominator_proposed']
    for unit in category['units']:
        rubrics.append(dict(id=unit['id'], category=category['id'], frozen_unit=unit,
            runs={run: state(run, unit['scoped_content'],
                next(e for e in expectation_rows if e['id'] == unit['expectation_id'])['runs'][run]['output_record_ids'],
                unit['do_not_score']) for run in run_data}))

relations = []
for group in ['confirmed_execution_relations', 'mentions', 'continuations', 'unconfirmed_execution_candidates']:
    for i, r in enumerate(deps[group]):
        relations.append(dict(id=r['id'], category=group, evaluation_pointer=f'/{group}/{i}',
            frozen_record=r, gold=group == 'confirmed_execution_relations',
            status='pending', reviewer=None, assigned_part='M-POC5A.4',
            uncertainty='Exact reviewed tuple/scope only. Unconfirmed candidates, aliases and metadata are not gold.',
            run_comparison={run: next((x for key in ['execution_relations', 'mentions', 'continuations']
                for x in d['dependencies'][key] if x.get('evaluation_id') == r['id']), None)
                for run, d in run_data.items()}))

edge_rows = {run: [dict(id=r['id'], response=run_refs[run], pointer=d['records'][r['id']]['pointer'],
    raw_span=d['records'][r['id']]['raw_span'], status='pending', result='not_assessable', reviewer=None,
    original_record=r, previous_comparison=next(v for v in d['dependencies']['all_output_edges'] if v['id'] == r['id']),
    uncertainty='Pending edge is neither TP nor certain FP; external target aliases need separate review.')
    for r in d['proposal']['dependencies']] for run, d in run_data.items()}
glyphs = {run: [dict(evidence_id=a['evidence_id'], inherited_locator_observation=a,
    original_evidence=d['records'][a['evidence_id']], status='pending', reviewer=None,
    uncertainty='Quote support/valid geometry does not certify full meaning or exact glyph containment.')
    for a in d['areas']['images'] if a['quote_in_area_status'] in ['boundary_clipping_pending_review', 'failed']]
    for run, d in run_data.items()}

focus = [
 dict(id='SEM-001', expectations=['EXP-017'], output_ids=['R916', 'G916'],
      classes=['błędna interpretacja', 'niejednoznaczność'],
      proposal='Oba wyniki zachowują warunek DR>TQ i minimum 1, ale R916.interpretation=unknown/G916.blocking pozostawia DR<=TQ nierozstrzygnięte. Proponowane niepełne odtworzenie zatwierdzonej lokalnej gałęzi 0 CH i nieuzasadniona blokada tej gałęzi; nie jest to dowód błędnego odczytu ani twierdzenia o zawsze 1 CH.',
      limits='Nie obejmuje pełnego OW, rzeczywistego TQ ani całej EXP-016. E916 ma osobny błąd lokatora.'),
 dict(id='SEM-002', expectations=['EXP-040'], output_ids=['R953', 'G953'],
      classes=['błędna interpretacja', 'niejednoznaczność', 'brak kontekstu'],
      proposal='Oba wyniki podają both rout/separate hexes, lecz deklarują nierozstrzygnięty zakres eliminacji. Eval-v1 przyjmuje eliminację każdej PH osobno, z możliwością legalnego Rout drugiej. Proponowana niepełna lokalna interpretacja; sprawdzić osobno, czy podstawa wcześniejszej decyzji była dostępna ekstraktorowi.',
      limits='Nie oceniać rzeczywistej geometrii, kolejności, wspólnego jedynego celu, 6.69/10.22 ani D1. Nie przenosić braków setupu na syntetyczne dane.'),
 dict(id='SEM-003', expectations=['EXP-030', 'EXP-031'], output_ids=['R932', 'N932ex', 'G932', 'DCTX932-S4', 'GCTX-order'],
      classes=['brak kontekstu', 'niejednoznaczność', 'błędna interpretacja'],
      proposal='first-001 ma lokalne pół/floor i literalny przykład, bez rozstrzygnięcia AS. context-01 dodaje udokumentowane 2x wyniku obrońcy przy AS, warunkowe pół/floor dla LC, wyjątek Routed i kumulatywność. Proponowane poprawne częściowe podparcie operatorów; pełna kolejność, zaokrąglenie, applicability i wynik pozostają nierozstrzygnięte.',
      limits='Zakres LC użytego w determination (8.45), tylko wymienione klasy obrońcy; nie dopisywać automatycznego znoszenia 2x i pół ani nowego gold dla EXP-031.'),
 dict(id='SEM-004', expectations=['EXP-025'], output_ids=['R923', 'DCTX923-S4'],
      classes=['brak kontekstu', 'błędna interpretacja'],
      proposal='9.23 mówi o Hits zadanych przez SK; Step 4 #3 mówi o Hits atakującego, gdy obrońcą jest SK. Nowa niejawna relacja R923->NCTX846S4 jest kandydatem uzasadnienia strony/faktora/floor/cap, wymaga osobnej decyzji o konieczności i rodzaju. Nie jest pewnym TP ani FP.',
      limits='Nie domyka doboru mieszanego obrońcy/Size/CRT i nie zwiększa gold 3 relacji niejawnych.'),
 dict(id='SEM-005', expectations=['EXP-016', 'EXP-017'], output_ids=['E916'], classes=['format'],
      proposal='Dawny potwierdzony błąd: bbox E916 urywa wyjątek Leader Elephant. Pełny obraz obejmuje wyjątek, ale oryginalnego lokatora nie naprawiono.', limits='Błąd dowodu nie jest automatycznie błędną transkrypcją lub interpretacją.'),
 dict(id='SEM-006', expectations=[], output_ids=[], classes=['pominięcie'],
      proposal='Oba wyniki nadal nie mają 3 krytycznych osobnych par niejawnych DEP-NEW-001/002/003 i 4 osobnych wzmianek DEP-034/035/043/067-1. To obserwacje strukturalne; semantyczne FN i treść w prozie oceniane osobno.',
      limits='DEP-NEW-001: R972->R971 condition; 002: N914table->R914 exception; 003: R986->R914 condition, wszystkie implicit. D961stack/DEP-037 różnica rodzaju pending.'),
 dict(id='SEM-007', expectations=[], output_ids=[], classes=['niejednoznaczność'],
      proposal='58 dawnych i 6 nowych granic glifów wymagają dokładnego review. Oględziny trzech pełnych regionów w tej części nie potwierdzają wszystkich bbox.', limits='111 cytatów i valid geometry nie certyfikują pełnych transkrypcji ani małych wartości.'),
 dict(id='SEM-008', expectations=['EXP-031', 'EXP-042'], output_ids=['NCTX846S4', 'N1013'], classes=['brak kontekstu'],
      proposal='Nowa połączona ścieżka kończy się na brakującym 6.68 bullet #6 po 3 krawędziach. Nie pozyskano źródła trzeciego kroku; pełne zależne wyniki blocked_source.', limits='Stop rozszerzania na granicy 2; nie deklarować zgodności całego grafu ani aktywnego czasu.')
]
for f in focus:
    f['criticality'] = ('critical_in_reviewed_scope' if f['id'] in ['SEM-001', 'SEM-002', 'SEM-003', 'SEM-004']
        else 'critical_for_three_implicit_tuples; noncritical_for_four_mentions' if f['id'] == 'SEM-006'
        else 'unknown; evaluate exact affected scope')
    f['impact'] = f['proposal']
    f['uncertainty'] = f['limits']
    f.update(status='pending', human_reviewer=None, preparer='Codex',
        proposed_assessment_only=True, source_expectation_pointers=[f'/expectations/{i}' for i,e in enumerate(exp) if e['id'] in f['expectations']],
        response_refs=run_refs, evaluation_manifest=eval_ref,
        output_trace={run: {rid: d['records'][rid] for rid in f['output_ids'] if rid in d['records']} for run,d in run_data.items()})

checklist = dict(id='M-POC5A-semantic-01-checklist', card='M-POC5A', part='M-POC5A.1',
    status='partial_waiting_review', prepared_at_utc=datetime.now(timezone.utc).isoformat(),
    evaluation=eval_ref, responses=run_refs, source=ref(P / 'source/original-pdf-20261008-01.pdf'),
    reviewer=None, semantic_acceptance='not_performed', whole_record_gold=False,
    human_decisions=[], counts=dict(content_groups=66, context_groups=8, inventory=207,
        rubric_units=len(rubrics), categories={c['id']:c['denominator_proposed'] for c in policy['categories']},
        output_edges={r:len(d['proposal']['dependencies']) for r,d in run_data.items()},
        reviewed_content_groups={r:0 for r in run_data}, reviewed_inventory={r:0 for r in run_data}),
    limitations=dict(active_budget='unknown', exact_selectors='unknown', tokens='unknown', price='unknown',
        first_extraction_history='unknown', assessment_exposure='unknown', clean_context='unknown',
        context_path_discovery_outside_allowlist='independently_confirmed', assessment_content_read='not_observed',
        contamination='not_proven', full_isolation='not_proven', full_graph_depth_compliance='not_assessable'),
    limits=dict(extra_pages=1, extra_rules=1, extra_tables=0, context_rounds_total=1, corrections_total=0,
        new_extractions_this_part=0, new_context_rounds_this_part=0, new_corrections_this_part=0, source_expansion_stop_depth=2),
    scope_policy='Only exact owner-confirmed eval-v1 scopes. All 105 candidates and unreviewed aliases remain outside gold. Local synthetic facts are not automatically blocked by missing real setup. 20 situations excluded: M-POC5B.',
    expectations=expectation_rows, inventory=inventory_rows, category_units=rubrics,
    illustration_states=dict(frozen_policy=policy['illustration_states_separate'], status='pending', reviewer=None),
    frozen_relations=relations, output_edges=edge_rows, locator_review=glyphs, focus_issue_ids=[f['id'] for f in focus],
    output_records={run:d['records'] for run,d in run_data.items()},
    resume='SEM-001/002/003 owner decisions first; then every pending in assigned parts. Hash changes invalidate affected prior decisions.')
save(OUT / 'checklist.json', checklist)
save(OUT / 'issues.json', dict(id='M-POC5A-semantic-01-issues', evaluation=eval_ref, responses=run_refs,
    six_classes=['format','pominięcie','błędny odczyt','błędna interpretacja','brak kontekstu','niejednoznaczność'],
    semantic_errors_confirmed='not_assessable', issues=focus,
    inherited_observations={run:d['errors']['errors'] for run,d in run_data.items()},
    operational_issues=checklist['limitations'],
    count_policy='Inherited structural observations and extractor declarations are preserved separately; proposed semantic findings require owner decision. Absence of reviewed wrong reads is not zero errors.'))
save(M / 'input-audit.json', dict(required_inputs=[ref(P/f) for f in required], checks=checks,
    complete_json_read=True, complete_text_evidence_read=True,
    visual_scope=['inputs/v1/regions/pdf-33-core-left.png','inputs/v1/regions/pdf-34-core-right.png',
        'context/pass-01/evidence/8.46-step-4-pdf-27.png'],
    visual_reviewer='Codex, limited focus text review; no human acceptance or strict glyph-boundary certificate',
    output_counts=checklist['counts']))

lines = ['# M-POC5A.1 — porównanie znaczenia obu wyników', '',
    'Stan: partial / waiting_review. Oceniający przygotował rejestr; właściciel nie nadał jeszcze akceptacji żadnemu zakresowi obu odpowiedzi.', '',
    f"eval-v1: `{eval_ref['sha256']}`.", '',
    *[f"{r}: {v['bytes']} bajtów, SHA-256 `{v['sha256']}`." for r,v in run_refs.items()], '',
    'Podział przed oceną: .1 integralność/rejestr/pierwsze rozbieżności; .2 EXP-001–025; .3 EXP-026–050; .4 EXP-051–074, pozostały inwentarz, wszystkie relacje i lokatory. Wszystkie części do 90 minut; bez pominięć pending.', '',
    'Pełne zakresy źródłowe, pola obu wyników, JSON pointers i dokładne bajty znajdują się w [checklist.json](checklist.json). Rejestr zawiera 74 porównania, 207 pozycji, wszystkie rubryki i wszystkie krawędzie; to przygotowanie dowodów, nie 74/207 wykonanych ocen.', '',
    '## Pierwszy zakres pokazany do przeglądu', '']
for f in focus:
    lines += [f"### {f['id']}", '', f['proposal'], '', 'Granice: '+f['limits'], '', 'Propozycja oceniającego Codex; decyzja właściciela pending.', '']
lines += ['## Oczekiwania — pełny zakres do review', '']
for row in expectation_rows:
    lines += [f"### {row['id']} — {row['assigned_part']}", '',
        'Dokładny zatwierdzony zakres: '+row['source_scope'], '',
        'Wyłączenia/niepewności: '+'; '.join(row['limits']+row['exclusions']), '']
    for e in row['source_evidence']:
        lines += [f"Źródło PDF {e['pdf_page']}, {e.get('column','')}, {e.get('inventory_ref','')}, bbox {e.get('bbox_pdf_points')}; dokładny source_span: {json.dumps(e.get('source_span'),ensure_ascii=False)}.", '',
            '> '+e.get('transcription','').replace('\n','\n> '), '']
    for run, s in row['runs'].items():
        lines += [f"**{run} — pending / not_assessable**. Kandydaci: {', '.join(s['output_record_ids'])}; osobny hash powyżej.", '']
        for rid in s['output_record_ids']:
            rr=run_data[run]['records'][rid]
            lines += [f"{rid}, pointer `{rr['pointer']}`, bajty [{rr['raw_span']['start_byte']}, {rr['raw_span']['end_byte_exclusive']}); hash zakresu `{rr['raw_span']['sha256']}`.", '']
            obj=rr['original_record']
            for field in ['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','content']:
                if field in obj:
                    lines += [field+':', '```json', json.dumps(obj[field],ensure_ascii=False,indent=2), '```', '']
        lines += ['Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): '+', '.join(g['id'] for g in s['extractor_gap_claims']), '']
lines += ['## Inwentarz — wszystkie 207 pozycji', '',
    'Dokładny frozen_item z transkrypcją, source_span, obrazem/hashem/bbox oraz osobnymi mapami obu odpowiedzi jest w checklist.inventory. Poniższy indeks nie nadaje akceptacji znaczenia.', '',
    '| ID | Typ | first-001 kandydaci | context-01 kandydaci | Zakres review |', '|---|---|---|---|---|']
for row in inventory_rows:
    lines += ['| '+' | '.join([row['id'],row['type'],','.join(row['runs']['first-001']['output_record_ids']),
        ','.join(row['runs']['context-01']['output_record_ids']),','.join(row['expectation_ids']) or 'M-POC5A.4; pending'])+' |']
lines += ['', '## Relacje, lokatory i metryki', '',
    '5 jawnych i 3 niejawne pary wykonawcze, 7 wzmianek i 7 kontynuacji zachowują mianowniki. 105 kandydatur pozostaje poza gold. Wszystkie 126/131 proponowanych krawędzi mają osobne pending; TP_gold, TP_output, FP, FN i precision/recall pozostają not_assessable.', '',
    '64 granice glifów i dziedziczony E916 wymagają osobnego zakresu review; 111 krótkich cytatów i valid geometry nie certyfikują całej treści. Rubryki: 41/38/43/66/52/29/7/1 oraz dwa osobne stany ilustracji.', '',
    'Krytyczny brak źródła blokuje pełny zależny wynik; nie blokuje automatycznie lokalnego wyniku z zadanymi faktami. Bez nowych źródeł, pass-02, ekstrakcji, korekt i oceny 20 sytuacji.', '',
    'Ścieżka 3 krawędzi kończy się brakującym celem; stop pozyskiwania na 2 zachowany, bez certyfikatu całego grafu. 1 strona/1 reguła/0 tabel, 1 runda kontekstu, 0 korekt.', '',
    'Niezależnie potwierdzono listing/path discovery poza allowlistą w context-01. Odczyt treści oceny niezaobserwowany; ekspozycja i czysty kontekst unknown, bez dowodu skażenia lub pełnej izolacji. Historyczne first-001, selektory, aktywny czas/budżet, tokeny/cena unknown. Kalendarz nie mierzy aktywnego budżetu.', '',
    'Kontrole i końcowe zachowanie bajtów prowadzi nowy measurement/M-POC5A-semantic-01/completion.json; zamkniętych raportów nie aktualizowano.', '',
    'Wznowienie: decyzje właściciela SEM-001/002/003, następnie pierwsze pending części .2–.4. Nie przenosić akceptacji M-POC4B na znaczenie.', '']
(OUT / 'review.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(prepared=checklist['counts'], protected_files=len(protected), integrity_checks=checks,
    review_bytes=(OUT/'review.md').stat().st_size),ensure_ascii=False))
