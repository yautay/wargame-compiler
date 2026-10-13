from review_tools import ROOT,P,M,R,read,ref
import json, datetime, copy, sys, hashlib

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(path,text):path.write_text(text.rstrip()+'\n',encoding='utf-8')

OUT=R/'part-04d4'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
phase=sys.argv[1]
if phase=='documents':
    draft=read(M/'assembly-summary.json')['manifest_draft']
    draft['artifacts'].append(ref(OUT/'owner-focus.md'))
    save(OUT/'manifest.json',draft)
    old=read(R/'current-state-27.json');s=copy.deepcopy(old)
    s.update(id='M-POC5A-current-state-28',part='M-POC5A.4d4',next_part='M-POC5A.4d5',status='partial_waiting_review',
        previous_state=ref(R/'current-state-27.json'),proposal_overlay=ref(OUT/'manifest.json'),
        summary=read(M/'assembly-summary.json')['summary'],prior_part_summary=old['summary'],new_owner_decisions=[],
        new_issue_ids=['SEM-022'],inventory_evaluator_compared_assigned_occurrences=414,inventory_remaining_assigned_occurrences=0,
        inventory_remaining_assigned_ids=0,inventory_owner_reviewed_new_occurrences=0,inventory_owner_reviewed_assigned_occurrences=332,
        inventory_owner_pending_compared_occurrences=82,inventory_remaining_parts=['M-POC5A.4d5'],
        part_4d4_evaluator_review_complete=True,part_4d4_owner_review_complete=False,all_assigned_inventory_evaluator_review_complete=True,
        all_assigned_inventory_owner_scoped_review_complete=False,part_4d5_reconciliation_pending=True,
        M_POC5A_closed=False,M_POC5A_4_closed=False,M_POC5A_4d_closed=False,
        next_action='Owner decision on 80 bounded supported scopes and 2 mixed SEM-022 scopes from part-04d4; then separate .4d5 reconciliation, then M-POC5B 40 situation judgments.',
        resume='Whole .4d4 manually compared: 41 IDs / 82 occurrences. Total207 IDs /414 comparisons;332 prior owner scopes retained,82 new pending. .4d5 and M-POC5B not executed.',
        actual_owner_file_open_or_read='unknown',TP_FP_FN_precision_recall='not_assessable')
    s['inventory_comparison_counters']=dict(compared=414,available=414,owner_decided=332,owner_pending=82,policy='Exact scopes; not full correct records.')
    s['issue_dispositions']['SEM-022']='Proposed limited omission of one explanatory clause per answer from R995 content; operative portion and image retained; waiting_review. No automatic FN/game-outcome claim.'
    assert not (R/'current-state-28.json').exists()
    save(R/'current-state-28.json',s)
    section='''## Wykonanie .4d4 — 2026-10-11

Wykonano cały rzeczywisty przegląd 41 przypisanych pozycji inwentarza, osobno w obu oryginalnych odpowiedziach: 82 porównania. Prywatny part-04d4 zawiera dokładne źródła, oryginalne pola i ślady do bajtów, oceny, wyłączenia oraz opis proponowanych decyzji po ludzku. Szacunek 75–90 minut zapisano przed oceną.

Proponowane 80 ograniczonych ocen wsparcia i 2 mieszane oceny jednej klauzuli, po jednej na odpowiedź. Operatywna treść zachowana; ograniczone pominięcie wyjaśnienia tekstowego przy zachowanym obrazie źródła zapisano osobno, bez automatycznego FN lub wykazanego błędnego wyniku gry. Role nagłówków nie certyfikują ich pełnej transkrypcji lub dawnych wad lokatorów.

Porównano 82 / udostępniono 82 / nowych decyzji właściciela 0 / pending 82; faktyczny odczyt plików unknown. Owner-decision-13 zachowuje zatwierdzenie .4d3 bez duplikatu. Łącznie 207/207 pozycji i 414/414 wystąpień porównano; 332 wcześniejsze zakresy przyjęte, 82 nowe oczekują decyzji. To nie 414 całych poprawnych rekordów.

Starsze 8 oczekiwań i 13 kwestii pozostają otwarte; ograniczone wcześniejsze dyspozycje zachowano. 257 zakresów relacji, 124 lokatorów, 264 pary rubryki i po 63 lokalne zakresy/3 wymagania źródła zachowano bez ponownego punktowania. Gold i limity bez zmiany; pełne metryki not_assessable.

current-state-28 prowadzi wynik. Najbliższa czynność: decyzje według prywatnego owner-focus .4d4; potem osobna .4d5 końcowe uzgodnienie i M-POC5B 20 sytuacji w obu wynikach (40 ocen). Tych kart tu nie wykonano. M-POC5A/.4/.4d pozostają partial; M-POC5 jedyny next. Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Konfiguracja, aktywne czasy, tokeny, cena i budżet unknown. Kontrole, logi i audyt niezmienności: measurement/M-POC5A-semantic-04d4/.
'''
    for name in ['docs/work/tasks/M-POC5A.md','docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4d.md','docs/work/tasks/semantic/M-POC5A.4d4.md']:
        f=ROOT/name;oldtext=f.read_text(encoding='utf-8-sig');md(f,oldtext.rstrip()+'\n\n'+section)
    f=ROOT/'docs/STATUS.md';txt=f.read_text(encoding='utf-8-sig')
    oldline=next(line for line in txt.splitlines() if line.startswith('- **Wynik M-POC5A:**'))
    txt=txt.replace(oldline,'- **Wynik M-POC5A:** partial — cała .4d4 porównana: 41 pozycji / 82 wystąpienia; 80 propozycji wsparcia i 2 mieszane, waiting_review; łącznie 207/207 pozycji i 414/414 porównań, 332 zakresy przyjęte / 82 pending; następnie .4d5 i M-POC5B, starsze nierozstrzygnięcia otwarte',1)
    at=txt.index('\n## ');txt=txt[:at]+'\n\n'+section+txt[at:];md(f,txt)
    handoff=ROOT/'docs/handoff/2026-10-11-M-POC5A-semantic-04d4.md'
    md(handoff,'# M-POC5A — przegląd inwentarza .4d4\n\n- **Data:** 2026-10-11, Europe/Warsaw\n- **Milestone:** M-POC5\n- **Karta:** M-POC5A.4d4\n- **Wynik:** partial / waiting_review\n- **Wykonawca:** Codex\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+section+
       '\nWejścia: prompt semantic-review-part04d4-start-v1, scope-plan /parts/3, current-state-27, owner-decision/overlay-13, niezmienione oba run/proposal/provenance/report, eval-v1 i dostarczone źródła. Dokładne prywatne hashe: pomiar preflight/read-inputs/manifest-verification. Po decyzjach obecnego pakietu oszacować .4d5 przed osobną sesją. Kontrole offline z lokalnymi TMP/TEMP i nowym basetemp, rzeczywiste wyniki w completion.json. Zastane zmiany zachowane.\n')
    f=ROOT/'docs/HANDOFF.md';oldtext=f.read_text(encoding='utf-8-sig')
    header='# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d4](handoff/2026-10-11-M-POC5A-semantic-04d4.md)\n- **Wynik:** partial / waiting_review\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'
    md(f,header+section+'\n## Historia — poprzednie przekazanie po owner13\n\n'+oldtext.split('\n',1)[1])
    f=ROOT/'docs/ROADMAP.md';txt=f.read_text(encoding='utf-8-sig');line=next(line for line in txt.splitlines() if line.startswith('| M-POC5 |'))
    cells=line.split('|');cells[3]=' M-POC5A partial: całe .4d4 porównane 41 pozycji/82 wystąpienia; 80 ograniczonych propozycji wsparcia i 2 mieszane waiting_review; łącznie 207/207 pozycji i 414/414 porównań, 332 wcześniejsze zakresy przyjęte i 82 nowe pending; 257 zakresów relacji/124 lokatorów/264 pary rubryki i po63 lokalne zakresy/3 wymagania źródła zachowane; starsze8 oczekiwań/13 kwestii otwarte; najpierw decyzje .4d4, potem osobna .4d5 uzgodnienie i M-POC5B20 sytuacji/40 ocen; pełne metryki nieocenialne '
    txt=txt.replace(line,'|'.join(cells),1);md(f,txt+'\n\n'+section)
    f=ROOT/'docs/work/tasks/README.md';md(f,f.read_text(encoding='utf-8-sig')+'\n\nStan po .4d4 (2026-10-11): rzeczywiście porównano cały przydział 41 pozycji/82 wystąpienia. Łącznie 207/207 pozycji i 414/414 porównań; 332 wcześniejsze zakresy z decyzjami, 82 nowe waiting_review. Po decyzjach obecnego pakietu osobna [M-POC5A.4d5](semantic/M-POC5A.4d5.md) i M-POC5B40 ocen sytuacji; nadrzędne karty partial, starsze nierozstrzygnięcia otwarte.\n')
    save(M/'documentation-updates.json',dict(recorded_at_utc=now,files=[ref(ROOT/name) for name in [
        'docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/tasks/README.md','docs/work/tasks/M-POC5A.md',
        'docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4d.md','docs/work/tasks/semantic/M-POC5A.4d4.md',
        'docs/handoff/2026-10-11-M-POC5A-semantic-04d4.md']],public_content='aggregates only'))
    print('Manifest/current-state-28 and public aggregates saved; earlier decisions/packages unchanged.')
elif phase=='close':
    manifest=read(OUT/'manifest.json')
    manifest['artifacts']=[ref(ROOT/a['path']) for a in manifest['artifacts']]
    save(OUT/'manifest.json',manifest)
    s=read(R/'current-state-28.json');s['proposal_overlay']=ref(OUT/'manifest.json')
    s['unresolved_issue_ids']=read(R/'current-state-27.json')['unresolved_issue_ids']+['SEM-022']
    s['inherited_issue_ids']=read(R/'current-state-27.json')['unresolved_issue_ids']
    s['current_part_owner_pending_issue_ids']=['SEM-022']
    save(R/'current-state-28.json',s)
    docs=read(M/'documentation-updates.json');docs['files']=[ref(ROOT/e['path']) for e in docs['files']];save(M/'documentation-updates.json',docs)
    checkroots=[ROOT/'private/poc/_checks'/n for n in ['active-89f54d12c061492785fdbdca1022e554','active-f172ac93a4594483ad15c6558bf2891c','active-3149bc3887aa41878f770de95761bfb2']]
    checks=[]
    for i,folder in enumerate(checkroots):
        result=read(folder/'result.json')
        checks.append(dict(attempt=i+1,result=result,result_file=ref(folder/'result.json'),pytest_log=ref(folder/'pytest.log'),diff_log=ref(folder/'diff-check.log'),
          outcome=['failed_missing_pytest_in_bundled_runtime','failed_duplicate_latest_handoff_pointer_fixed','passed_156_tests'][i]))
    assert checks[-1]['result']['tests_exit']==0 and checks[-1]['result']['diff_exit']==0
    before=read(M/'immutability-before.json');sessionspath=P/'measurement/sessions.jsonl'
    sessionbefore=next(f for f in before['files'] if f['path']==sessionspath.relative_to(ROOT).as_posix())
    b=sessionspath.read_bytes();assert len(b)==sessionbefore['bytes'] and hashlib.sha256(b).hexdigest()==sessionbefore['sha256']
    assert b.endswith(b'\n')
    assert b'M-POC5A-semantic-04d4' not in b
    completion=dict(id='M-POC5A-semantic-04d4-completion-01',card='M-POC5A.4d4',status='partial_waiting_review',
      completed_at_utc=now,preflight=ref(M/'preflight.json'),estimate=ref(M/'estimate.json'),read_inputs=ref(M/'read-inputs.json'),
      manifest_verification=ref(M/'manifest-verification.json'),review_manifest=ref(OUT/'manifest.json'),state=ref(R/'current-state-28.json'),
      summary=read(M/'assembly-summary.json')['summary'],checks=checks,
      actual_checks='First attempt lacked pytest; second156-test run had one continuity failure, fixed latest handoff pointer; final156 passed. Logs retained for all attempts.',
      operational_notes=['Read-only display helper initially assumed graphic transcription and raised KeyError; corrected fallback to original evidence object.',
                         'Console cp1252 could not encode a continuation arrow; switched output encoding to UTF-8; original files unchanged.',
                         'Large historical JSON/text output was truncated in tool display; relevant exact source/field content was re-exposed in bounded batches. Full inputs parsed; mechanical read log is not semantic proof.'],
      model_configuration='unknown',active_user_time='unknown',active_model_time='unknown',tokens='unknown',price='unknown',overall_budget_compliance='unknown',
      calendar_start_evidence=read(M/'preflight.json')['recorded_at_utc'],calendar_duration_is_active_time=False,
      new_sources=0,new_extractions=0,new_corrections=0,new_owner_decisions=0,other_parts_executed=[],
      sessions_append_policy='Exactly one new record for this session; original prefix preserved.',
      next_action=s['next_action'])
    save(M/'completion.json',completion)
    entry=dict(id='M-POC5A-semantic-04d4',card='M-POC5A.4d4',milestone='M-POC5',session_kind='local_evaluating_manual_review',
      recorded_at_utc=now,user_facing_date='2026-10-11',timezone='Europe/Warsaw',executor='Codex',branch='feature/tests',workspace='C:/repo/wargame-compiler',
      result='partial_waiting_review',completion=ref(M/'completion.json'),manifest=ref(OUT/'manifest.json'),state=ref(R/'current-state-28.json'),
      compared=82,owner_available=82,owner_newly_decided=0,owner_pending=82,
      prior_owner_inventory_scopes=332,total_inventory_compared=414,total_distinct_inventory_ids_compared=207,
      new_issue_ids=['SEM-022'],new_sources=0,new_extractions=0,new_corrections=0,
      active_user_time='unknown',active_model_time='unknown',tokens='unknown',price='unknown',overall_budget='unknown',
      tests_passed=156,test_attempts=3,diff_check_exit=0,next_action=s['next_action'])
    with sessionspath.open('ab') as stream:stream.write((json.dumps(entry,ensure_ascii=False)+'\n').encode('utf-8'))
    changed=[];verified=0
    for item in before['files']:
        path=ROOT/item['path'];current=path.read_bytes()
        if path==sessionspath:
            prefix=current[:item['bytes']];suffix=current[item['bytes']:]
            assert hashlib.sha256(prefix).hexdigest()==item['sha256']
            added=suffix.decode('utf-8').splitlines();assert len(added)==1 and json.loads(added[0])['id']==entry['id']
            continue
        actual=ref(path)
        if (actual['bytes'],actual['sha256'])!=(item['bytes'],item['sha256']):changed.append(dict(before=item,after=actual))
        else:verified+=1
    assert not changed,changed
    save(M/'immutability-after.json',dict(recorded_at_utc=now,baseline=ref(M/'immutability-before.json'),
      prior_files_unchanged=verified,changed_prior_immutable_files=changed,
      sessions_original_prefix_preserved=True,sessions_exactly_one_new_record=True,sessions_new_id=entry['id'],
      original_answers_source_eval_reports_decisions_and_prior_packages_unchanged=True,
      intentional_public_document_updates=docs['files'],public_content='aggregates only'))
    validation=dict(card='M-POC5A.4d4',all82_manual_judgments=True,exact_assigned_ids=True,raw_spans_verified=420,
       source_helper_exact_fragments_verified=True,source_images_hashes_verified=True,graphic_exact_crops_inspected=8,
       evidence_sources='Supplied PDF36–37; no PDF27 whole-page access or extra source acquisition.',
       iverified_prior_files=verified,sessions_one_new_entry=True,comparison_count=82,available_count=82,owner_decided_count=0,owner_pending_count=82,
       total_compared=414,total_prior_owner_decided=332,total_owner_pending=82,full_metrics='not_assessable')
    save(M/'validation.json',validation)
    print('Closed measurement:156 tests passed; immutable prior files',verified,'unchanged; exactly one session append.')
