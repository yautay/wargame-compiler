from session import ROOT,P,R,S,M,read,ref,save,md,now
import json,copy,hashlib,sys,re

phase=sys.argv[1]
if phase=='documents':
    paths={x['path'] for x in read(P/'measurement/M-POC5A-semantic-04d5/read-inputs.json')['files']}
    paths.update((R/n).relative_to(ROOT).as_posix() for n in ['current-state-30.json','current-state-31.json','owner-decision-15.json','owner-review-overlay-15.json','owner-review-summary-15.md'])
    paths.update(f.relative_to(ROOT).as_posix() for f in (R/'part-04d5').iterdir() if f.is_file())
    paths.update(['docs/work/tasks/M-POC5B.md','docs/handoff/2026-10-11-M-POC5A-semantic-04d5.md',
      'private/poc/spqr-chapter9/evaluation/eval-v1/situations.json',
      'private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt',
      'private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-scope.json'])
    for sit in read(P/'evaluation/eval-v1/situations.json')['situations']:
        paths.add(sit['authorizing_decision']['path'])
        if sit.get('overlay_provenance'):paths.add(sit['overlay_provenance']['path'])
    entries=[]
    for path in sorted(paths):
        f=ROOT/path
        if f.suffix=='.json':read(f)
        else:f.read_text(encoding='utf-8-sig')
        entries.append(ref(f))
    save(M/'read-inputs.json',dict(files=entries,method='Full requiredJSON/text read; source/field/case comparisons and manualderivations separately recorded. Read/hash/schema is not semanticcorrectness.'))
    prior_verification=P/'measurement/M-POC5A-semantic-04d4/manifest-verification.json'
    checked={}
    for item in read(prior_verification)['verified_references']:
        expected=item['actual'];name=expected['path']
        if name not in checked:checked[name]=ref(ROOT/name)
        assert checked[name]==expected
    save(M/'manifest-verification.json',dict(prior=ref(prior_verification),all301_prior_bindings_unchanged=True,
      unique_artifacts_rechecked=len(checked),verified=list(checked.values()),frozen7artifacts_verified_in_preflight=True))
    report=read(S/'results.json');semantic=read(R/'current-state-31.json');summary=report['summary']
    manifest=dict(id='M-POC5B-situations-01-manifest-01',card='M-POC5B',status='partial_waiting_review',evaluation=semantic['evaluation'],
      source=ref(P/'source/original-pdf-20261008-01.pdf'),responses=semantic['responses'],frozen_situations=ref(P/'evaluation/eval-v1/situations.json'),
      artifacts=[ref(S/name)for name in ['results.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],
      estimate=ref(M/'estimate.json'),manual_assessments=ref(M/'manual-assessments.json'),validation=ref(M/'validation.json'),read_inputs=ref(M/'read-inputs.json'),
      semantic_parent=ref(R/'current-state-31.json'),reconciliation_owner_decision=ref(R/'owner-decision-15.json'),new_owner_situation_decisions=[])
    save(S/'manifest.json',manifest)
    state=copy.deepcopy(semantic);state.update(id='M-POC5-current-state-32',card='M-POC5B',part='M-POC5B-situations-01',status='partial_waiting_review',
      previous_state=ref(R/'current-state-31.json'),semantic_state_inherited=ref(R/'current-state-31.json'),proposal_overlay=ref(S/'manifest.json'),
      prior_semantic_summary=semantic['summary'],summary=summary,next_part='M-POC5B-owner-review',
      new_issue_ids=['SITREV-001','SITREV-002','SITREV-003'],new_owner_decisions=[ref(R/'owner-decision-15.json')],
      M_POC5B_executed=True,M_POC5B_evaluator_review_complete=True,M_POC5B_owner_review_complete=False,
      M_POC5B_remaining_situations=0,M_POC5B_remaining_answer_judgments=0,M_POC5B_remaining_unreviewed_answer_judgments=0,
      situation_evaluator_compared_occurrences=40,situation_owner_available_occurrences=40,situation_owner_decided_occurrences=0,situation_owner_pending_occurrences=40,
      situation_full_results_suspended_occurrences=3,M_POC5_closed=False,M_POC5B_closed=False,M_POC5A_closed=False,
      next_action='Owner review of35positive judgments and2candidateunjustifiedblocks/2Triariiheld/1contextLCheld in situations-01 owner-focus. Preserve old8pending/13issues and frozeneval. FormalM-POC5closure requires actual decisions; M-POC6/7 not started.',
      resume='All20frozen cases evaluated separately in both original rule representations:40compared/40available/0ownerdecisions/40pending. Evaluator-derived results are not new model scenario answers. Full3results held; prior414inventory/257relations/124locators/264rubricpairs retained.',
      actual_owner_file_open_or_read='unknown',full_semantic_metrics='not_assessable')
    assert not (R/'current-state-32.json').exists();save(R/'current-state-32.json',state)
    approval_section='''## Zatwierdzenie uzgodnienia .4d5 — 2026-10-11

Właściciel „zatwierdzam i kontynuuj” przyjął dokładne uzgodnienie .4d5 i przekazanie do M-POC5B z ograniczeniami. Nowe owner-decision15/overlay15 i current-state31 zachowują414 wcześniejszych decyzji inwentarza,257 zakresów relacji,124 lokatory,264 pary rubryki oraz starsze8 oczekiwań/13 kwestii. Nowych punktów0, bez wyboru dawnych wariantów lub pełnej akceptacji rekordów/metryk. .4d5 ma przyjęty raport uzgodnienia; M-POC5A/.4/.4d nadal partial w szerszym zakresie. W tej sesji wykonano osobne M-POC5B po szacunku75–90min dla wszystkich20 sytuacji/40 ocen.
'''
    section='''## M-POC5B — wszystkie sytuacje porównane, 2026-10-11

Po zatwierdzeniu dokładnego uzgodnienia .4d5 wykonano całe M-POC5B:20 zamrożonych sytuacji w obu oryginalnych odpowiedziach,40 ocen. Każdy wariant i wymagany wniosek porównano ze źródłem, oryginalnymi polami i frozenexpected; prywatny situations-01 zawiera ślady do bajtów, użyte zależności, ręczne wyprowadzenia i opis decyzji po ludzku. To ocena wyprowadzalności z zapisu reguł przy zadanych faktach, bez nowych odpowiedzi modelu na sytuacje, nowej ekstrakcji, korekty lub silnika. Szacunek75–90min zapisano przed oceną; cały zakres mieści się w jednej zaplanowanej części.

Propozycjefirst:15 zgodnych lokalnych wyników,3 właściwe oczekiwane blokady,1kandydat nieuzasadnionej lokalnej blokady i1pełny wynik zawieszony po porównaniu. Context:14/3/1/2. Razem35 pozytywnych ocen oraz5 do osobnego rozstrzygnięcia. Pełny mianownik20 w każdej odpowiedzi zachowany; warianty nie dają dodatkowych punktów. Oczekiwane blokady nie są meaningful localresults dla progu80%.

Porównano40 / udostępniono40 / nowych decyzji właściciela0 / pending40. Wszystkie40 ocen wykonane przez oceniającego;3 pełne wnioski zawieszone mimo porównanych komponentów. Wydzielono konsekwencje dwóch starych nierozstrzygnięć i jedno pytanie o zakres zamrożonych faktów wobec dostarczonego warunku po kontekście. Nie rozstrzygnięto starych wariantów ani nie zmieniono eval-v1; nie wykazano przez samo to regresji modelu lub konkretnej złej liczby.

current-state32 prowadzi nowy wynik. Starsze8 oczekiwań/13 kwestii oraz wcześniejsze ograniczone decyzje zachowane.414 zakresów inwentarza,257 relacji,124 lokatory i264 pary rubryki bez ponownego punktowania. M-POC5B i milestone5 partial/waiting_review, M-POC5 jedyny next. M-POC5A w szerszym zakresie nadal partial; pełne jakość/TP/FP/FN/precision/recall not_assessable.

Najbliższa czynność: decyzje według prywatnego situations-01/owner-focus —35 pozytywnych ocen oraz2+2+1 osobne. Następnie świadomie rozliczyć starsze nierozstrzygnięcia i warunki formalnego zamknięcia etapu5. Nie rozpoczęto M-POC6/7 ani naprawy odpowiedzi. Faktyczny odczyt plików przez właściciela unknown; konfiguracja, aktywne czasy, tokeny, cena i łączny budżet unknown. Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Kontrole i audyt: measurement/M-POC5B-situations-01/.
'''
    for name in ['docs/work/tasks/M-POC5A.md','docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4d.md','docs/work/tasks/semantic/M-POC5A.4d5.md']:
        f=ROOT/name;md(f,f.read_text(encoding='utf-8-sig')+'\n\n'+approval_section)
    f=ROOT/'docs/work/tasks/M-POC5B.md';md(f,f.read_text(encoding='utf-8-sig')+'\n\n'+section)
    f=ROOT/'docs/STATUS.md';txt=f.read_text(encoding='utf-8-sig');txt=txt.replace('- **Bieżąca karta:** M-POC5A','- **Bieżąca karta:** M-POC5B',1)
    oldline=next(x for x in txt.splitlines()if x.startswith('- **Wynik M-POC5A:**'))
    txt=txt.replace(oldline,'- **Wynik M-POC5A:** partial — .4d5 uzgodnienie zatwierdzone owner-decision15;414 zakresów inwentarza z decyzjami, starsze8 oczekiwań/13 kwestii i pełne wyniki pozostają otwarte',1)
    at=txt.index('\n## ');txt=txt[:at]+'\n- **Wynik M-POC5B:** partial — wszystkie20 sytuacji/40 ocen porównano; propozycjefirst15/3/1/1,context14/3/1/2;35 pozytywnych i5 osobnych, nowych decyzji0/pending40; pełne3 wnioski zawieszone mimo wykonanego porównania\n\n'+section+'\n'+txt[at:];md(f,txt)
    handoff=ROOT/'docs/handoff/2026-10-11-M-POC5B-situations-01.md'
    md(handoff,'# M-POC5B — wszystkie20 sytuacji w obu odpowiedziach\n\n- **Data:** 2026-10-11, Europe/Warsaw\n- **Milestone:** M-POC5\n- **Karta:** M-POC5B\n- **Wynik:** partial / waiting_review\n- **Wykonawca:** Codex\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5B\n\n'+approval_section+'\n'+section+
      '\nWejścia: kartaM-POC5B, niezmienny eval-v1/situations i jego20ID, oba oryginalne run/proposal/provenance/reports, dostarczonePDF31–37 i wyłącznie dostarczonyStep4cropPDF27, current-state30 i nowa owner-decision15/current-state31. Hashe, rozłączny pełny przydział i szacunek: preflight/estimate/read-inputs; rzeczywiste kontrole: completion.json. Materiał szczegółowy wyłącznie prywatny.\n')
    f=ROOT/'docs/HANDOFF.md';old=f.read_text(encoding='utf-8-sig');old=old.replace('- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d5](handoff/2026-10-11-M-POC5A-semantic-04d5.md)',
      '- **Ostatnia sesja (historyczna):** 2026-10-11-M-POC5A-semantic-04d5 (`handoff/2026-10-11-M-POC5A-semantic-04d5.md`)',1)
    md(f,'# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5B-situations-01](handoff/2026-10-11-M-POC5B-situations-01.md)\n- **Wynik:** partial / waiting_review\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5B\n\n'+section+'\n## Historia — poprzednie przekazanie\n\n'+old.split('\n',1)[1])
    f=ROOT/'docs/ROADMAP.md';txt=f.read_text(encoding='utf-8-sig');line=next(x for x in txt.splitlines()if x.startswith('| M-POC5 |'));cells=line.split('|')
    cells[3]=' M-POC5A szerszy zakres partial, .4d5 dokładne uzgodnienie zatwierdzone;414 wcześniejszych decyzji inwentarza/257relacji/124lokatorów/264parrubryki zachowane, starsze8 oczekiwań/13 kwestii otwarte. M-POC5B całe20 sytuacji/40 ocen porównane, waiting_review:35 pozytywnych propozycji i5 osobnych (first15/3/1/1,context14/3/1/2), pełne3 wyniki zawieszone po porównaniu; mianownik20 na odpowiedź, bez nowych odpowiedzi modelu na sytuacje lub silnika; najpierw decyzje i rozliczenie ograniczeń, pełne metryki nieocenialne '
    md(f,txt.replace(line,'|'.join(cells),1)+'\n\n'+section)
    f=ROOT/'docs/work/tasks/README.md';md(f,f.read_text(encoding='utf-8-sig')+'\n\nStan po M-POC5B (2026-10-11): zatwierdzono dokładne .4d5 uzgodnienie; wszystkie20 sytuacji w obu odpowiedziach porównano (40 ocen).35 pozytywnych propozycji i5 osobnych oczekuje właściciela, pełne3 wnioski zawieszone po porównaniu. Bieżąca kartaM-POC5B, M-POC5 jedyny next; szerszeM-POC5A i starsze8 oczekiwań/13 kwestii nadal partial/otwarte.\n')
    names=['docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/tasks/README.md','docs/work/tasks/M-POC5A.md','docs/work/tasks/M-POC5B.md',
      'docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4d.md','docs/work/tasks/semantic/M-POC5A.4d5.md','docs/handoff/2026-10-11-M-POC5B-situations-01.md']
    save(M/'documentation-updates.json',dict(files=[ref(ROOT/name)for name in names],public_content='aggregates only'))
    print('Read',len(entries),'inputs;301priorbindings still match. Resultsmanifest/current-state32 and M-POC5B handoff saved.')

elif phase=='close':
    checkroot=ROOT/sys.argv[2];result=read(checkroot/'result.json');assert result['tests_exit']==0 and result['diff_exit']==0
    before=read(M/'immutability-before.json');sessions=P/'measurement/sessions.jsonl';old_session=next(x for x in before['files']if x['path']==sessions.relative_to(ROOT).as_posix())
    assert ref(sessions)==old_session;saved=sessions.read_bytes();assert saved.endswith(b'\n')and b'M-POC5B-situations-01'not in saved
    report=read(S/'results.json');state=read(R/'current-state-32.json')
    completion=dict(id='M-POC5B-situations-01-completion-01',card='M-POC5B',recorded_at_utc=now(),status='partial_waiting_review',
      manifest=ref(S/'manifest.json'),state=ref(R/'current-state-32.json'),summary=report['summary'],
      preflight=ref(M/'preflight.json'),estimate=ref(M/'estimate.json'),validation=ref(M/'validation.json'),read_inputs=ref(M/'read-inputs.json'),
      approval=ref(R/'owner-decision-15.json'),checks=dict(result=result,result_file=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),diff_log=ref(checkroot/'diff-check.log')),
      operational_notes=['A draft assembly used path subscripting instead of a path join; corrected before anyresults were written. Originalinputs untouched.'],
      first_recorded_calendar_time=read(M/'preflight.json')['recorded_at_utc'],calendar_time_is_active=False,
      model_reasoning_selectors='unknown',active_user_time='unknown',active_model_time='unknown',tokens='unknown',price='unknown',overall_budget_compliance='unknown',
      new_sources=0,new_extractions=0,new_corrections=0,new_gold=0,new_model_situation_responses=0,engine_used=False,
      compared40=True,owner_pending40=True,M_POC5_closed=False,next_action=state['next_action'])
    save(M/'completion.json',completion)
    entry=dict(id='M-POC5B-situations-01',card='M-POC5B',milestone='M-POC5',workspace='C:/repo/wargame-compiler',branch='feature/tests',
      recorded_at_utc=now(),date='2026-10-11',timezone='Europe/Warsaw',status='partial_waiting_review',
      preceding_reconciliation_owner_approval=ref(R/'owner-decision-15.json'),completion=ref(M/'completion.json'),state=ref(R/'current-state-32.json'),
      evaluator_compared=40,owner_available=40,owner_newly_decided=0,owner_pending=40,per_answer_denominator=20,
      first_proposals=report['summary']['per_answer']['first-001'],context_proposals=report['summary']['per_answer']['context-01'],
      new_model_situation_responses=0,new_extractions=0,new_corrections=0,new_sources=0,active_time='unknown',tokens='unknown',price='unknown',budget='unknown',
      tests_exit=result['tests_exit'],diff_exit=result['diff_exit'],next_action=state['next_action'])
    with sessions.open('ab')as stream:stream.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
    unchanged=0;changes=[]
    for old in before['files']:
        f=ROOT/old['path']
        if f==sessions:
            current=f.read_bytes();assert hashlib.sha256(current[:old['bytes']]).hexdigest()==old['sha256']
            appended=current[old['bytes']:].decode().splitlines();assert len(appended)==1 and json.loads(appended[0])['id']==entry['id'];continue
        actual=ref(f)
        if actual==old:unchanged+=1
        else:changes.append(dict(before=old,after=actual))
    assert not changes,changes
    save(M/'immutability-after.json',dict(recorded_at_utc=now(),baseline=ref(M/'immutability-before.json'),prior_immutable_files_unchanged=unchanged,
      changed_prior_files=changes,sessions_original_prefix_preserved=True,exactly_one_session_append=True,
      all_originals_source_eval_reports_prior_decisions_and_packages_unchanged=True))
    print('Closed measurement; priorimmutable files',unchanged,'unchanged; one session append; originalanswers and frozenfacts preserved.')
