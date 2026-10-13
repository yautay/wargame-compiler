from session import ROOT,P,R,M,read,ref,save,md,now
import json,copy,hashlib,sys

OUT=R/'part-04d5'
phase=sys.argv[1]
if phase=='documents':
    paths={x['path'] for x in read(P/'measurement/M-POC5A-semantic-04d4/read-inputs.json')['files']}
    paths.update((R/n).relative_to(ROOT).as_posix() for n in ['current-state-28.json','current-state-29.json','owner-decision-14.json','owner-review-overlay-14.json','owner-review-summary-14.md'])
    paths.update(f.relative_to(ROOT).as_posix() for f in (R/'part-04d4').iterdir() if f.is_file())
    paths.update(['docs/work/tasks/semantic/M-POC5A.4d5.md','docs/handoff/2026-10-11-M-POC5A-semantic-04d4.md',
       'private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04d1/scope-plan.json'])
    entries=[]
    for path in sorted(paths):
        f=ROOT/path
        if f.suffix=='.json':read(f)
        else:f.read_text(encoding='utf-8-sig')
        entries.append(ref(f))
    save(M/'read-inputs.json',dict(files=entries,method='Full JSON/text reads; exact reconciliation and manual pending source/output inspection separately documented. Read/hash/schema checks are not semantic correctness.'))
    previous_manifest_check=P/'measurement/M-POC5A-semantic-04d4/manifest-verification.json'
    verified=read(previous_manifest_check)['verified_references']
    checked={}
    for x in verified:
        expected=x['actual'];f=ROOT/expected['path']
        if expected['path'] not in checked:checked[expected['path']]=ref(f)
        assert checked[expected['path']]==expected
    save(M/'manifest-verification.json',dict(prior_check=ref(previous_manifest_check),prior301reference_bindings_still_match=True,
        unique_prior_artifacts_rechecked=len(checked),verified=list(checked.values()),semantic_proof=False))
    summary=read(OUT/'comparisons.json')['summary']
    manifest=dict(id='M-POC5A.4d5-manifest-01',card='M-POC5A.4d5',status='partial_waiting_review',evaluation=ref(P/'evaluation/eval-v1/manifest.json'),
      source=ref(P/'source/original-pdf-20261008-01.pdf'),responses=read(R/'current-state-29.json')['responses'],
      artifacts=[ref(OUT/name) for name in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],
      estimate=ref(M/'estimate.json'),scope_plan=ref(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json'),scope_pointer='/parts/4',
      prior_decision=ref(R/'owner-decision-14.json'),prior_overlay=ref(R/'owner-review-overlay-14.json'),read_inputs=ref(M/'read-inputs.json'),validation=ref(M/'validation.json'),new_owner_reconciliation_decisions=[])
    save(OUT/'manifest.json',manifest)
    state=read(R/'current-state-29.json');s=copy.deepcopy(state)
    s.update(id='M-POC5A-current-state-30',part='M-POC5A.4d5',next_part='M-POC5B',status='partial_waiting_review',
      previous_state=ref(R/'current-state-29.json'),proposal_overlay=ref(OUT/'manifest.json'),summary=summary,prior_part_summary=state['summary'],
      part_4d5_evaluator_review_complete=True,part_4d5_owner_reconciliation_complete=False,part_4d5_reconciliation_pending=True,
      inventory_remaining_parts=[],new_issue_ids=[],new_owner_decisions=[ref(R/'owner-decision-14.json')],
      reconciliation_counts={'compared_packages':1,'available_packages':1,'owner_decided_packages':0,'pending_packages':1,'new_inventory_occurrences':0,'new_rule_points':0},
      next_action='Owner decision on exact .4d5 reconciliation only; old8expectations/13issues retained. Then separately estimate/execute M-POC5B20 situations in both answers (40 judgments), split beforehand if>90minutes.',
      resume='Full .4d5 reconciliation executed:207inventory/74expectations/277rubricpairs/13issues;414priorinventory decisions retained. No new scores, old pending preserved; M-POC5B not executed.',
      M_POC5A_closed=False,M_POC5A_4_closed=False,M_POC5A_4d_closed=False,
      M_POC5B_executed=False,M_POC5B_remaining_situations=20,M_POC5B_remaining_answer_judgments=40)
    assert not (R/'current-state-30.json').exists();save(R/'current-state-30.json',s)
    section='''## Zatwierdzenie .4d4 i uzgodnienie .4d5 — 2026-10-11

Właściciel „zatwierdzam i kontynuuj” przyjął82 oceny .4d4:80 ograniczonych ocen wsparcia i2mieszane oceny klauzuli z ograniczonym pominięciem wyjaśnienia. Owner-decision14/overlay14 i current-state29 zapisują zgodę;414 wcześniejszych zakresów inwentarza ma decyzje,207 na odpowiedź. To nie414 całych poprawnych rekordów. Starsze8 oczekiwań/13 kwestii pozostają otwarte.

Wykonano całe .4d5: uzgodniono207 pozycji/414 wcześniejszych ocen,74 oczekiwania w obu oryginalnych hashach,277 par rubryki i13 starszych kwestii; rozliczono257 zakresów relacji,124 lokatory i granice218 oryginalnych rekordów reguł/węzłów. Odczytano właściwe źródła/pola ośmiu pending; nowsze ograniczone decyzje odróżniono od otwartych reszt. Prywatny part-04d5 zawiera konkretny wynik każdego uzgodnienia, podstawy, wyłączenia i opis po ludzku. Szacunek65–85min zapisano przed pracą.

Po63/66 lokalne zakresy i3/8 wymagania źródła na wynik przyjęte;3 lokalne i5 kontekstowych oczekiwań nadal pending.264/277 par rubryki przyjęte,13 pozostaje przy3lokalnych nierozstrzygnięciach. Nie dopisano wariantów, reguł lub gold i nie nadano nowych punktów. Pełne wyniki i metryki nadal not_assessable; wymaganie źródła nie dostarcza realnej mapy, setupu lub tabeli.

Wcześniejszy inwentarz: porównano414 / udostępniono414 / przyjęto414 / pending0. Nowy pakiet uzgodnienia: porównano1 / udostępniono1 / nowych decyzji0 / pending1. Wcześniejszych decyzji nie cofnięto; faktyczny odczyt plików przez właściciela unknown. current-state30 prowadzi wynik, M-POC5A/.4/.4d partial, M-POC5 jedyny next.

Najbliższa czynność: decyzja według owner-focus .4d5 o dokładnym uzgodnieniu i przekazaniu z ograniczeniami. Potem pozostaje wykonawczo osobne M-POC5B:20 zamrożonych sytuacji w obu odpowiedziach,40 ocen. Przed rozpoczęciem oszacować cały zakres i podzielić wcześniej, jeśli przekracza90min. Sytuacji nie wykonano tutaj. Do pełnego zamknięcia pozostaje także przegląd właściciela i rozliczenie otwartych kwestii, bez zgadywania braków.

Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Konfiguracja, aktywne czasy, tokeny, cena i łączny budżet unknown. Oryginały i wcześniejsze pakiety zachowane; logi, kontrole i audyt prowadzi measurement/M-POC5A-semantic-04d5/.
'''
    for name in ['docs/work/tasks/M-POC5A.md','docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4d.md','docs/work/tasks/semantic/M-POC5A.4d5.md']:
        f=ROOT/name;md(f,f.read_text(encoding='utf-8-sig')+'\n\n'+section)
    f=ROOT/'docs/STATUS.md';txt=f.read_text(encoding='utf-8-sig');oldline=next(x for x in txt.splitlines() if x.startswith('- **Wynik M-POC5A:**'))
    txt=txt.replace(oldline,'- **Wynik M-POC5A:** partial — .4d4 zatwierdzona,414 zakresów inwentarza z decyzjami; całe .4d5 uzgodnione207 pozycji/74 oczekiwania/277 par rubryki, nowy raport waiting_review; starsze8 oczekiwań/13 kwestii otwarte; po decyzji pozostaje wykonawczo M-POC5B20 sytuacji/40 ocen',1)
    at=txt.index('\n## ');md(f,txt[:at]+'\n\n'+section+txt[at:])
    handoff=ROOT/'docs/handoff/2026-10-11-M-POC5A-semantic-04d5.md'
    md(handoff,'# M-POC5A — zatwierdzenie .4d4 i uzgodnienie .4d5\n\n- **Data:** 2026-10-11, Europe/Warsaw\n- **Milestone:** M-POC5\n- **Karta:** M-POC5A.4d5\n- **Wynik:** partial / waiting_review\n- **Wykonawca:** Codex\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+section+
      '\nWejścia: scope-plan /parts/4, current-state28 oraz nowa zgoda właściciela, owner-decision/overlay14, oba oryginalne run/proposal/provenance/report, eval-v1 i niezmienne źródła/pakiety. Hashe prywatnie w preflight/read-inputs/manifest-verification; rzeczywiste kontrole w completion.json. Niewykonane sytuacje nie są ocenionym wynikiem; łącznego czasu końca M-POC5 nie oszacowano przed M-POC5B.\n')
    f=ROOT/'docs/HANDOFF.md';previous=f.read_text(encoding='utf-8-sig')
    previous=previous.replace('- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d4](handoff/2026-10-11-M-POC5A-semantic-04d4.md)',
      '- **Ostatnia sesja (historyczna):** 2026-10-11-M-POC5A-semantic-04d4 (`handoff/2026-10-11-M-POC5A-semantic-04d4.md`)',1)
    md(f,'# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d5](handoff/2026-10-11-M-POC5A-semantic-04d5.md)\n- **Wynik:** partial / waiting_review\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+section+'\n## Historia — poprzednie przekazanie\n\n'+previous.split('\n',1)[1])
    f=ROOT/'docs/ROADMAP.md';txt=f.read_text(encoding='utf-8-sig');line=next(x for x in txt.splitlines() if x.startswith('| M-POC5 |'));cells=line.split('|')
    cells[3]=' M-POC5A partial: .4d4 zatwierdzona,414 zakresów inwentarza z decyzjami; cała .4d5 uzgodniona207 pozycji/74 oczekiwania/277 par rubryki, nowy pakiet waiting_review bez nowych punktów; 257 relacji/124 lokatory/264 pary rubryki i po63 zakresy lokalne/3 wymagania źródła zachowane; starsze8 oczekiwań/13 kwestii otwarte; po decyzji uzgodnienia pozostaje M-POC5B20 sytuacji/40 ocen, oszacować przed wykonaniem; pełne metryki nieocenialne '
    md(f,txt.replace(line,'|'.join(cells),1)+'\n\n'+section)
    f=ROOT/'docs/work/tasks/README.md';md(f,f.read_text(encoding='utf-8-sig')+'\n\nStan po .4d5 (2026-10-11): .4d4 zatwierdzona82 ocen; całe uzgodnienie .4d5 wykonane i waiting_review.414 wcześniejszych zakresów inwentarza przyjęte, po63/66 lokalne zakresy i3/8 wymagania źródła zachowane. Po decyzji raportu pozostaje osobne M-POC5B20 sytuacji/40 ocen, z szacunkiem przed rozpoczęciem. Starsze8 oczekiwań/13 kwestii otwarte; nadrzędne karty partial.\n')
    docpaths=['docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/tasks/README.md','docs/work/tasks/M-POC5A.md',
      'docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4d.md','docs/work/tasks/semantic/M-POC5A.4d5.md','docs/handoff/2026-10-11-M-POC5A-semantic-04d5.md']
    save(M/'documentation-updates.json',dict(files=[ref(ROOT/name) for name in docpaths],public_content='aggregates only'))
    print('Read',len(entries),'inputs;301 prior manifest bindings unchanged. New manifest/state30/public handoff saved.')

elif phase=='close':
    checkroot=ROOT/sys.argv[2];result=read(checkroot/'result.json');assert result['tests_exit']==0 and result['diff_exit']==0
    before=read(M/'immutability-before.json');sessionpath=P/'measurement/sessions.jsonl';original=next(x for x in before['files'] if x['path']==sessionpath.relative_to(ROOT).as_posix())
    b=sessionpath.read_bytes();assert ref(sessionpath)==original and b.endswith(b'\n');assert b'M-POC5A-semantic-04d5' not in b
    report=read(OUT/'comparisons.json');state=read(R/'current-state-30.json')
    completion=dict(id='M-POC5A-semantic-04d5-completion-01',card='M-POC5A.4d5',status='partial_waiting_review',recorded_at_utc=now(),
      approval=ref(R/'owner-decision-14.json'),manifest=ref(OUT/'manifest.json'),state=ref(R/'current-state-30.json'),summary=report['summary'],
      preflight=ref(M/'preflight.json'),read_inputs=ref(M/'read-inputs.json'),validation=ref(M/'validation.json'),
      checks=dict(result=result,result_file=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),diff_log=ref(checkroot/'diff-check.log')),
      operational_notes=['Historical part02 run entries lacked proposed_assessment key; used the unchanged expectation-level classification after checking actual schemas.',
        'Historical relation scopes use distinct schemas; preserved exact accepted/rejected components and their prior judgment instead of assuming evaluator_comparison key.',
        'Read-only hash references cached within reconciliation for unchanged inputs; cache is provenance only, not semantic evaluation.'],
      active_user_time='unknown',active_model_time='unknown',model_reasoning_selectors='unknown',tokens='unknown',price='unknown',overall_budget='unknown',
      first_recorded_calendar_time=read(M/'preflight.json')['recorded_at_utc'],calendar_time_is_active=False,
      new_sources=0,new_extractions=0,new_corrections=0,new_gold=0,new_inventory_scores=0,M_POC5B_executed=False,next_action=state['next_action'])
    save(M/'completion.json',completion)
    entry=dict(id='M-POC5A-semantic-04d5',card='M-POC5A.4d5',milestone='M-POC5',workspace='C:/repo/wargame-compiler',branch='feature/tests',
      recorded_at_utc=now(),date='2026-10-11',timezone='Europe/Warsaw',status='partial_waiting_review',
      owner_approval_this_session=ref(R/'owner-decision-14.json'),completion=ref(M/'completion.json'),state=ref(R/'current-state-30.json'),
      reconciliation_compared_packages=1,reconciliation_available_packages=1,reconciliation_owner_decided_packages=0,reconciliation_pending_packages=1,
      prior_inventory_compared=414,prior_inventory_available=414,prior_inventory_owner_decided=414,prior_inventory_owner_pending=0,
      new_inventory_occurrences=0,new_rule_points=0,old_pending_expectations=8,old_open_issue_ids=13,
      active_time='unknown',tokens='unknown',price='unknown',budget='unknown',tests_result=result['tests_exit'],diff_result=result['diff_exit'],next_action=state['next_action'])
    with sessionpath.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
    changed=[];count=0
    for old in before['files']:
        path=ROOT/old['path']
        if path==sessionpath:
            after=path.read_bytes();assert hashlib.sha256(after[:old['bytes']]).hexdigest()==old['sha256']
            lines=after[old['bytes']:].decode().splitlines();assert len(lines)==1 and json.loads(lines[0])['id']==entry['id'];continue
        actual=ref(path)
        if actual!=old:changed.append(dict(before=old,after=actual))
        else:count+=1
    assert not changed,changed
    save(M/'immutability-after.json',dict(recorded_at_utc=now(),baseline=ref(M/'immutability-before.json'),prior_immutable_files_unchanged=count,
      changed_prior_files=changed,sessions_prefix_preserved=True,exactly_one_new_session_record=True,session_id=entry['id'],
      originals_sources_eval_reports_prior_decisions_and_packages_unchanged=True))
    print('Completion saved; immutable previous files',count,'unchanged; exactly one session appended.')
