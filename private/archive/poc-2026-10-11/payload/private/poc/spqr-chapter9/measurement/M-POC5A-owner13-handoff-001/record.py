"""Record the owner's .4d3 acceptance and prepare a fresh-session handoff."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
R = P / 'reviews/semantic-01'
M = Path(__file__).resolve().parent
PACK = R / 'part-04d3'
D = ROOT / 'docs'
def load(p): return json.loads(p.read_bytes())
def ref(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def save(p, value):
    assert not p.exists(), p
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def newtext(p, value):
    assert not p.exists(), p
    p.write_text(value, encoding='utf-8')

now = datetime.now(timezone.utc).isoformat()
prior = load(R/'current-state-26.json')
packet = load(PACK/'comparisons.json')
pres = load(PACK/'presentation.json')
mf = load(PACK/'manifest.json')
save(M/'start.json', dict(recorded_at_utc=now, card='M-POC5A.4d3-owner-review',
    scope='Record explicit acceptance and prepare prompt only; no .4d4 semantic review.',
    estimate_minutes_range=[10,20], active_time='unknown',
    protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f != P/'measurement/sessions.jsonl'],
    sessions_before=ref(P/'measurement/sessions.jsonl'), previous_state=ref(R/'current-state-26.json')))
for x in mf['artifacts'] + [mf['source'], mf['evaluation'], mf['scope_plan']] + list(mf['responses'].values()):
    assert ref(ROOT/x['path']) == x
reply = 'zatwierdzam i podaj prompt aby kontynuować w nowej sesji'
reviewer = 'owner in this chat; personal identity unknown'
disposition = ('Owner confirmed SEM-021 only as omission of one historical explanatory clause per answer '
    'from mapped textual content: operative conditions retained and attached source image retains the explanation. '
    'Two mixed parent and two child judgments describe the same underlying omission, not four independent errors. '
    'No demonstrated wrong game outcome, automatic semantic FN, new game rule or response repair; older pending unchanged.')
save(M/'approval-evidence.json', dict(owner_reply_verbatim=reply, recorded_at_utc=now,
    owner_message_sent_at_utc='unknown', actual_owner_file_open_or_read='unknown',
    interpretation='Accept immediately presented .4d3 recommendations:114 bounded supported judgments and4 related mixed-parent/omitted-child judgments. Prepare prompt for .4d4 in a new session, without executing it here.',
    presented_decisions=pres['decisions'], basis=[ref(PACK/'owner-focus.md'), ref(PACK/'presentation.json')]))
scopes=[]
for i, row in enumerate(packet['inventory']):
    j=copy.deepcopy(row)
    j.update(status='reviewed', human_reviewer=reviewer, reviewer=reviewer,
        recorded_at_utc=now, whole_record_accepted=False,
        comparison_artifact=ref(PACK/'comparisons.json'), comparison_pointer=f'/inventory/{i}')
    for run, v in j['runs'].items():
        v.update(status='reviewed', human_reviewer=reviewer, reviewer=reviewer,
            owner_decision='accepted_presented_bounded_judgment', whole_record_accepted=False)
    scopes.append(j)
unresolved = [i for i in prior['unresolved_issue_ids'] if i != 'SEM-021']
assert unresolved == pres['summary']['previous_unresolved_issue_ids']
decision=dict(id='M-POC5A-owner-decision-13', card='M-POC5A', part='M-POC5A.4d3',
    date='2026-10-11', timezone='Europe/Warsaw', recorded_at_utc=now, reviewer=reviewer,
    owner_reply_verbatim=reply, decision='accepted_presented118_bounded_inventory_judgments',
    approval_evidence=ref(M/'approval-evidence.json'), prior_decision=ref(R/'owner-decision-12.json'),
    prior_state=ref(R/'current-state-26.json'), comparison_manifest=ref(PACK/'manifest.json'),
    focused_packet=ref(PACK/'owner-focus.md'), evaluation=mf['evaluation'], responses=mf['responses'], source=mf['source'],
    recommendations=pres['decisions'], scopes=scopes, newly_reviewed_inventory_occurrences=118,
    per_answer={'first-001':59,'context-01':59}, bounded_supported_occurrences=114,
    mixed_parent_occurrences=2, explanatory_child_omission_occurrences=2,
    underlying_omitted_explanatory_clauses_per_answer=1, issue_disposition={'SEM-021':disposition},
    unresolved_prior_issue_ids=unresolved, pending_expectation_ids=prior['pending_expectation_ids'],
    count_policy=packet['scope_policy'], owner_file_open_or_read='unknown', metrics='not_assessable',
    excluded=pres['excludes'], no_response_changes=True, no_gold_change=True, no_new_sources=True,
    whole_card_closed=False)
save(R/'owner-decision-13.json', decision)
dr=ref(R/'owner-decision-13.json')
o=copy.deepcopy(load(R/'owner-review-overlay-12.json'))
o.update(id='M-POC5A-owner-review-overlay-13', decision=dr,
    prior_overlay=ref(R/'owner-review-overlay-12.json'), inventory_owner_decision=dr,
    owner_reviewed_inventory_scoped_occurrences=332, inventory_count_policy=packet['scope_policy'])
for run, v in o['runs'].items():
    v['inventory_scopes'] += [dict(id=j['id'], source_scopes=j['source_scopes'],
        manual_assessment=j['manual_assessment'], comparison=j['manual_comparison'],
        decision=dr, trace=j['runs'][run], status='reviewed', reviewer=reviewer,
        whole_record_accepted=False) for j in scopes]
    v['owner_reviewed_inventory_scoped_occurrences']=166
save(R/'owner-review-overlay-13.json', o)
newtext(R/'owner-review-summary-13.md', '# Zatwierdzenie .4d3\n\n'
    'Właściciel: „'+reply+'”. Przyjęto 118 przedstawionych ocen: 114 zakresów wsparcia '
    'oraz 2 mieszane oceny akapitu i 2 oceny pominiętego wyjaśnienia historycznego. '
    'SEM-021 potwierdzono w tym ograniczonym zakresie. To jedna pominięta klauzula na odpowiedź; '
    'warunki operatywne zachowano, dołączony obraz zawiera wyjaśnienie. Nie wykazano błędnego wyniku gry. '
    'Oryginały pozostają bez naprawy, bez automatycznego FN lub dodatkowej reguły.\n\n'
    'Łącznie 332 zakresy inwentarza mają decyzje właściciela (166 na odpowiedź). '
    'Starsze 8 oczekiwań i 13 kwestii pozostają otwarte. Następna nowa sesja: '
    'wyłącznie .4d4 — 41 pozycji / 82 porównania; potem osobno .4d5 i M-POC5B.\n')
s=copy.deepcopy(prior)
s.update(id='M-POC5A-current-state-27', part='M-POC5A.4d3-owner-review',
    previous_state=ref(R/'current-state-26.json'), decision=dr,
    overlay=ref(R/'owner-review-overlay-13.json'), inventory_owner_decision=dr,
    new_owner_decisions=[dr], part_4d3_owner_review_complete=True,
    inventory_owner_reviewed_new_occurrences=118, inventory_owner_reviewed_assigned_occurrences=332,
    inventory_owner_pending_compared_occurrences=0, unresolved_issue_ids=unresolved,
    next_part='M-POC5A.4d4', next_action='In a fresh local evaluator session, estimate and execute only .4d4:41 assigned IDs/82 occurrences. No repeated .4d3 approval; older pending remain open.',
    resume='Owner13 accepted118 bounded .4d3 judgments, including limited SEM-021 omission.332 inventory scopes have owner decisions. Next .4d4 in new session; .4d5 reconciliation and M-POC5B remain separate.')
s['issue_dispositions']['SEM-021']=disposition
s['summary'].update(new_owner_reviewed_occurrences=118, owner_pending_occurrences=0,
    owner_accepted_scoped_occurrences=118, owner_accepted_supported_occurrences=114,
    owner_decided_mixed_or_omission_occurrences=4)
save(R/'current-state-27.json',s)

prompt='''Kontynuuj M-POC5A, część M-POC5A.4d4.

Pracuj lokalnie w C:\\repo\\wargame-compiler na feature/tests.
To sesja oceniająca. Wykonaj rzeczywisty przegląd całej przypisanej partii;
nie kończ na planie, generowaniu rejestru pending lub samych kontrolach hashów.
Znaczenie akceptuje właściciel. Nie powtarzaj ekstrakcji i nie poprawiaj odpowiedzi.
P = private/poc/spqr-chapter9/; R = P/reviews/semantic-01/.

Przeczytaj CLAUDE.md, docs/SESSION-PLAYBOOK.md, STATUS, HANDOFF, ROADMAP,
POC-PLAN, ADR-0039 i karty M-POC5A/.4/.4d/.4d4.
Aktualny handoff: docs/handoff/2026-10-11-M-POC5A-owner13-handoff-01.md.
Aktualny stan: R/current-state-27.json. Decyzje: owner-decision-13.json,
owner-review-overlay-13.json i owner-review-summary-13.md; także poprzednie
decyzje prowadzące oczekiwania, relacje i lokatory (03/07/10).
Ten prompt prowadzi nowszy stan i zakres .4d4; historyczny prompt
P/prompts/semantic-review-part04b1-start-v1.txt zachowuje bazowe rygory oceny,
ale jego stary stan i przydział .4b1 nie są zakresem tej sesji.

Właściciel już zatwierdził .4d3. Nie pytaj ponownie o tę zgodę i nie zapisuj
duplikatu owner-decision-13. Przyjęto 114 ograniczonych ocen oraz 4 powiązane
oceny mieszane/pominięcia SEM-021. To jedna pominięta klauzula wyjaśnienia
historycznego na odpowiedź; część operatywna i źródłowy obraz zachowane.
Nie ustanawia to nowej reguły, automatycznego FN ani błędnego wyniku gry.
Łącznie inwentarz: 166/207 pozycji, 332/414 wystąpień porównano i przyjęto
ograniczone oceny. To nie 332 całe poprawne rekordy. Relacje: 257 zakresów;
lokatory: 124; rubryka/oczekiwanie: 264 pary; po 63 lokalne zakresy i 3
wymagania źródła na odpowiedź. Zachowaj bez ponownego punktowania.

Najpierw zweryfikuj oryginalne bajty/SHA-256 i manifesty:
- P/runs/first-001/first-001.json: 617941 bajtów,
  3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
- P/runs/context-01/response.raw.txt: 712014 bajtów,
  95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
- P/evaluation/eval-v1/manifest.json: 4116 bajtów,
  7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
- P/source/original-pdf-20261008-01.pdf: 3965827 bajtów,
  e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e.
- P/measurement/M-POC5A-semantic-04d1/scope-plan.json: 9721 bajtów,
  928dc497c018a6e9cdae75681a523f4d8d62e071ff657edfd876d20af7c16fe5.

Przeczytaj pełne wymagane wejścia: oba run.json/session-evidence.txt,
proposal.json/provenance.json, zamknięte report.md/errors.json/inventory.json/
metrics.json/dependency-comparison.json/manifest.json/closure.json obu wyników,
context-comparison.json, measurement/M-POC4B-context-01/report-reference-supplement.json,
reviews/context-source-01/decision-01.json i review-closure-01.json.
Źródła prowadzą source/source-v1.json, inputs/v1/manifest.json,
context/pass-01/manifest.json i freeze-v1.json oraz rzeczywisty manifest
transfer/context-v1/context/pass-01/manifest.json. Przeczytaj zamrożone eval-v1:
dependencies.json, expectations.json, inventory.json i measurement-policy.json;
R/checklist.json oraz wcześniejsze review/issues i pakiety z manifestami,
w szczególności part-04d1/02/03. Lista pełnych wejść jest też w
P/measurement/M-POC5A-semantic-04d3/read-inputs.json — użyj jej do sprawdzenia
kompletności, ale rejestr przeczytania nie zastępuje rzeczywistego porównania.

Dokładny przydział PRZED wykonaniem prowadzi scope-plan.json, /parts/3:
41 jawnych ID, osobno po 41 w first-001 i context-01 = 82 wystąpienia.
To pozostałe typy inwentarza z pierwszym dowodem na PDF 36–37. Nie pomijaj ID
i nie rozszerzaj zakresu przez szeroki parent lub pudełko dowodowe.
Źródłowy rozdział kończy się przed 10.0 na PDF 37. Pozostała treść strony
granicznej nie jest nową partią reguł. Dozwolone są dostarczone PDF 31–37;
strona 27 tylko w już dostarczonym wycinku Step4. Nie odczytuj całej PDF 27
lub innych stron jako nowego kontekstu. Nie pozyskuj nowych źródeł/pass-02.

Przed semantycznym review zapisz świeży szacunek pełnej .4d4 (plan 70–90min).
Limit jednej części 90 minut. Jeśli nie mieści się, podziel PRZED wykonaniem,
z jawnymi rozłącznymi listami ID, kartami, additive planem, STATUS/ROADMAP.
Wykonaj jedną największą spójną część mieszczącą się w limicie. Pozostałe ID
muszą mieć jawny przydział. .4d5 i M-POC5B nie są wykonywane w tej sesji.

Wykonaj rzeczywiste porównania każdego przypisanego ID w obu odpowiedziach:
- Odczytaj tekst/obraz źródła i właściwy child span przed szerszą kopertą.
  Jeśli zakres przecina kolumny, odtwórz ich prawidłową kolejność. Wybrany
  dosłowny fragment prowadzi przed podsumowaniem; mapped-parent nie certyfikuje child.
- Porównaj oznaczenia, warunki, działanie/skutek, wyjątki, liczby, jednostki,
  negacje i czas w odpowiednich polach. Rozdziel literalną transkrypcję,
  streszczenie i interpretację. Zapisz wybrane ocenione zakresy i wyłączenia;
  nie przenoś oceny wybranego pola na cały rekord.
- Grafiki i żetony porównaj wizualnie: napisy, glify, rozmieszczenie, podpisy,
  rzeczywisty zakres ilustracji. Odczyt glifu nie certyfikuje znaczenia ratingu,
  setupu, tożsamości jednostki lub wartości tabel bez dostarczonego źródła.
  Rozdziel fizyczną kontynuację od zależności wykonawczej.
- Dla każdego wariantu zapisz recenzenta, dokładne źródło/hash/pointer,
  pierwotne pole i ślad do surowych bajtów odpowiedzi, porównanie, wpływ,
  proponowaną decyzję, niepewności i wyłączenia. Hash/schema/mapowanie tylko
  dowodzi pochodzenia; nie stanowi dowodu poprawności znaczenia.
- Zapisuj błędny odczyt, pominięcie, interpretację, brak kontekstu,
  niejednoznaczność i obserwację strukturalną osobno. Krytyczne braki źródeł
  blokują zależny pełny wynik. Nie zgaduj tabel, setupu lub ratingów.

Starsze 8 pending: EXP-010/017/019/040/050/052/066/074.
Lokalne 017/040/052; kontekst 010/019/050/066/074.
SEM-001–013 pozostają otwarte w dotychczasowych zakresach, także przy
częściowych przyjętych aspektach SEM-004/005/007. Pozostałe ograniczone
dyspozycje SEM-014–021 zachowaj. Nie wybieraj za właściciela dawnych wariantów
AS/LC, liczby eliminowanych jednostek DD, połączenia bramek Triarii, kompasu,
minimum i ratingów. Lokalne przyjęte warunki nie zamykają tych kwestii.
Nie rozszerzaj 105 niepotwierdzonych kandydatów do gold. Nie powielaj błędów
ani punktów przez parent/child. Pełne TP/FP/FN/precision/recall i jakość
nadal not_assessable bez wymaganych ocen i sprawdzonych mianowników.

Zapisz nowy R/part-04d4/: comparisons.json/md, review.md, issues.json,
owner-focus.md, presentation.json, manifest.json; additive current-state
po 27 oraz osobny P/measurement/M-POC5A-semantic-04d4/. Przy dalszym podziale
użyj nowych odpowiednich ID. Wcześniejsze artefakty pozostają niezmienne;
sessions.jsonl tylko append, dokładnie jeden nowy wpis tej sesji. Nowe oceny
waiting_review do decyzji człowieka. Oryginałów nie naprawiaj.

Wyjaśnij wyniki PO LUDZKU w owner-focus i w czacie: co mówi instrukcja,
co zapisał model, jaka jest różnica, co zmienia, jaka decyzja jest proponowana
i czego nie obejmuje. Wydziel konkretny pozytywny zestaw i nierozstrzygnięcia.
Pokaż plik z porównaniami; nie poświadczaj faktycznego odczytu za właściciela.
Przy pełnym wykonaniu .4d4 pokrycie inwentarza wyniesie 207 pozycji/414
porównań, lecz .4d5 uzgodnienie i M-POC5B nadal pozostają do wykonania.
Nie ogłaszaj zakończenia etapu 5 przez samo pokrycie inwentarza.

Aktualizuj STATUS/ROADMAP/karty/handoff według rzeczywistego zakresu;
publicznie tylko agregaty, treść wydawcy/obrazy/reguły/odpowiedzi prywatnie.
Uruchom scripts/check.ps1 offline, lokalne TMP/TEMP i nowy basetemp;
git diff --check, rzeczywiste logi, audyt niezmienności i trzy osobne
liczniki porównane/udostępnione/przyjęte-pending. M-POC5 jedyny next;
nadrzędne M-POC5A/.4/.4d partial do rzeczywistego rozliczenia całości.

Zachowaj zastane zmiany: bez reset/clean/stash/przełączenia gałęzi,
globalnej konfiguracji Git, commit/push, nowych czatów/wiadomości,
API inferencji, automatyzacji GUI/procesów modelowych, nowych ekstrakcji,
korekt odpowiedzi, M-POC5B/6/7 i architektury. Nie deleguj agentom bez
osobnego polecenia właściciela. Lokalna ścieżka C:\\repo ma pierwszeństwo
przed historycznym C:\\dev w bootstrapie.
Limity nadal: 1 dodatkowa strona/1 reguła/0 tabel, 1 runda kontekstu/0 korekt,
0 pełnych domknięć, 4 częściowe uzupełnienia/4 nowe deklaracje, stop głębokość2.
Historyczne listing/path discovery poza allowlistą potwierdzone; odczyt
treści oceny niezaobserwowany, ekspozycja/czysty kontekst unknown — bez
twierdzenia o skażeniu lub pełnej izolacji. Konfiguracja, aktywne czasy,
tokeny/cena/budżet unknown; czas kalendarzowy nie jest czasem aktywnym.
'''
promptpath=P/'prompts/semantic-review-part04d4-start-v1.txt'
newtext(promptpath,prompt)
body=('Właściciel zatwierdził .4d3: 118 przedstawionych ocen (114 ograniczonych '
    'ocen wsparcia i 4 powiązane oceny mieszane/pominięcia). Jedną obserwację '
    'pominięcia na odpowiedź potwierdzono w ograniczonym zakresie; nie są to '
    'cztery niezależne błędy ani przyjęcie całych rekordów. Starsze 8 oczekiwań '
    'i 13 kwestii pozostają otwarte.\n\n'
    'Owner-decision-13 / overlay-13 i current-state-27 prowadzą stan. Łącznie '
    '332 zakresy inwentarza mają decyzje, po 166 na odpowiedź; 166/207 pozycji '
    'i 332/414 wystąpień porównano. Nadrzędne karty pozostają partial, M-POC5 '
    'jedyny next. Oryginały i wcześniejsze pakiety zachowano.\n\n'
    'Następna nowa sesja: wyłącznie .4d4 — 41 pozycji / 82 porównania. '
    'Prompt: `private/poc/spqr-chapter9/prompts/semantic-review-part04d4-start-v1.txt`. '
    'Przed oceną wymagany świeży szacunek; .4d4 nie wykonano tutaj. '
    'Potem osobno .4d5 końcowe uzgodnienie i M-POC5B: 20 sytuacji w obu '
    'odpowiedziach (40 ocen).\n\n'
    'Ta sesja zapisuje zatwierdzenie i przekazanie na prośbę właściciela. '
    'Bez nowych źródeł, ekstrakcji, korekt, czatów, commit/push. Pełne metryki '
    'nieocenialne, aktywny czas/tokeny/cena/budżet unknown. Kontrole i audyt '
    'prowadzi nowy pomiar `measurement/M-POC5A-owner13-handoff-001/`.\n')
handoff=D/'handoff/2026-10-11-M-POC5A-owner13-handoff-01.md'
newtext(handoff,'# M-POC5A — zatwierdzenie .4d3 i prompt nowej sesji\n\n'
    '- **Data:** 2026-10-11, Europe/Warsaw\n- **Milestone:** M-POC5\n'
    '- **Karta:** M-POC5A\n- **Wynik:** partial\n'
    '- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+body)
publicpaths=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',
    *[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4d','.4d3','.4d4']]]
save(M/'public-documents-before.json',[ref(p) for p in publicpaths])
status=(D/'STATUS.md').read_text(encoding='utf-8')
lines=status.splitlines()
lines=[('- **Wynik M-POC5A:** partial — .4d3 zatwierdzona 118 ocen; łącznie 332 '
    'zakresy inwentarza z decyzjami, 166/207 pozycji i 332/414 porównań; '
    'następna .4d4: 41 pozycji, potem .4d5 i M-POC5B; starsze pending otwarte')
    if l.startswith('- **Wynik M-POC5A:**') else l for l in lines]
status='\n'.join(lines)+'\n'
pos=status.index('\n## ')
status=status[:pos]+'\n## Zatwierdzenie .4d3 i przekazanie nowej sesji — 2026-10-11\n\n'+body+status[pos:]
(D/'STATUS.md').write_text(status,encoding='utf-8')
oldhandoff=(D/'HANDOFF.md').read_text(encoding='utf-8')
(D/'HANDOFF.md').write_text('# HANDOFF\n\n'
    '- **Ostatnia sesja:** [2026-10-11-M-POC5A-owner13-handoff-01](handoff/2026-10-11-M-POC5A-owner13-handoff-01.md)\n'
    '- **Wynik:** partial\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'
    +body+'\n## Historia przed zatwierdzeniem .4d3\n\n'+oldhandoff.removeprefix('# HANDOFF\n'),encoding='utf-8')
roadmap=(D/'ROADMAP.md').read_text(encoding='utf-8')
old='.4d3 porównana59 pozycji/118 ocen(114+2mieszaneparent+2child), nowe pending;166/207 pozycji332/414 wystąpień porównano;'
assert old in roadmap
roadmap=roadmap.replace(old,'.4d3 zatwierdzona118 ograniczonych ocen (114 wsparcia i4 powiązane mieszane/pominięcia); łącznie332 zakresy inwentarza z decyzjami,166/207 pozycji332/414 wystąpień porównano; następna osobna.4d4;')
(D/'ROADMAP.md').write_text(roadmap,encoding='utf-8')
for path in publicpaths[3:]:
    with path.open('a',encoding='utf-8') as f:
        f.write('\n## Zatwierdzenie .4d3 i nowa sesja — 2026-10-11\n\n'+body)
save(M/'artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-13.json',
    'owner-review-overlay-13.json','owner-review-summary-13.md','current-state-27.json']]
    +[ref(promptpath),ref(handoff)]+[ref(p) for p in publicpaths]))
print(json.dumps(dict(new_owner_judgments=118,bounded_supported=114,mixed_or_omission=4,
    total_owner_inventory=332,remaining_ids=41,prompt=ref(promptpath)),ensure_ascii=False))
