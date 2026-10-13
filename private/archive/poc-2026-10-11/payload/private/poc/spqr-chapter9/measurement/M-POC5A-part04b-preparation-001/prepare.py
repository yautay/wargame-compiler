"""Plan edge-ID partitions only; no semantic review or acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(),protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),request='ok daj prompt do nowej sesji na duży postęp prac',scope='Prepare prompt and split .4b before execution; no edge judgments or new chat.'))
C=load(P/'reviews/semantic-01/checklist.json');cur=load(P/'reviews/semantic-01/current-state-07.json')
answers={r:load(P/f'proposals/{r}/proposal.json') for r in ['first-001','context-01']}
edges={r:{d['id']:d for d in a['dependencies']} for r,a in answers.items()}
ids=set().union(*(set(a) for a in edges.values()));new=set(edges['context-01'])-set(edges['first-001'])
assert len(new)==5 and len(ids)==131
part1={d['id'] for a in edges.values() for d in a.values() if d['target_status'] in ['internal','external_with_source'] or d['kind'] in ['mention','continuation']}|new
part2={i for i in ids-part1 if edges['context-01'][i]['from'].startswith(('R91','R92','R93','R94','N91','N101'))}
part3=ids-part1-part2
parts={f'M-POC5A.4b{i}':sorted(s) for i,s in enumerate([part1,part2,part3],1)}
assert set().union(*(set(s) for s in parts.values()))==ids and sum(map(len,parts.values()))==131
counts={k:{r:sum(i in a for i in v) for r,a in edges.items()} for k,v in parts.items()}
assert sum(sum(v.values()) for v in counts.values())==257
scope=[]
for part,selected in parts.items():
    scope.append(dict(part=part,output_edge_ids=selected,occurrences=counts[part],occurrence_count=sum(counts[part].values()),selection_rule={'M-POC5A.4b1':'Any run has internal/source-present target, mention or continuation; plus all five context-added edges. Structural routing only, not proof of target/source correctness.','M-POC5A.4b2':'Remaining edges with from prefix R91/R92/R93/R94/N91/N101.','M-POC5A.4b3':'All remaining edges; disjoint exhaustive complement.'}[part],semantic_review='not_performed',status='planned'))
plan=dict(id='M-POC5A.4b-scope-plan-01',date='2026-10-11',timezone='Europe/Warsaw',split_before_execution=True,metadata_only=True,current_state=ref(P/'reviews/semantic-01/current-state-07.json'),evaluation=C['evaluation'],responses=C['responses'],counts=dict(distinct_output_ids=131,output_occurrences=257,first=126,context=131),parts=scope,first_part_extra_frozen_scope=['5 explicit execution tuples','3 implicit execution tuples including missing DEP-NEW-001/002/003','7 frozen mentions including missing DEP-034/035/043/067-1 and D961stack kind difference','7 frozen continuation tuples'],new_context_edge_ids=sorted(new),unconfirmed_candidates=105,all_gold_remains_frozen=True,owner_acceptance='not_requested_or_given_for_relations',further_split_policy='If estimated full evidence review of a named part exceeds 90 minutes, split that part with exact ID lists and update cards/STATUS/ROADMAP BEFORE semantic review. All assigned IDs must stay accounted for.',first_part_executed=False)
save(M/'scope-plan.json',plan)
for n in [1,2,3]:
    part=scope[n-1];path=ROOT/f'docs/work/tasks/semantic/M-POC5A.4b{n}.md'
    text=f'''# M-POC5A.4b{n}: Relacje — partia {n}

- **ID:** M-POC5A.4b{n}
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** [M-POC5A.4b](M-POC5A.4b.md), stan current-state-07.json lub nowszy.

## Cel i pytanie eksperymentalne

Rzeczywisty przegląd przypisanych relacji obu odpowiedzi. Podział z
2026-10-11 PRZED wykonaniem: {len(part['output_edge_ids'])} różnych ID,
{part['occurrences']['first-001']} wystąpień first-001 i {part['occurrences']['context-01']} context-01.
Typy/statusy ekstraktora służą wyłącznie przydzieleniu zakresu, nie ocenie.

## Dokładne pliki do przeczytania

Bootstrap, SESSION-PLAYBOOK, STATUS, HANDOFF i aktualny handoff, ROADMAP,
POC-PLAN, ADR-0039; karty M-POC5A/.4/.4b. Prywatnie stan, decyzje i overlay,
oba run/proposal/provenance/report, eval-v1 i źródła. Dokładny przydział:
private/poc/spqr-chapter9/measurement/M-POC5A-part04b-preparation-001/scope-plan.json.

## Wejścia i wersja oceny

Niezmienione first-001/context-01 i eval-v1; osobne hashe i bajty.
63 zakresy lokalne i 3 wymagania źródła przyjęte na wynik; żadna relacja
nie dziedziczy przez to akceptacji. 8 oczekiwań nadal pending.

## Wymagane działania

Sprawdzić dla każdego ID źródłowy zakres, tożsamość/zakres celu, kierunek,
rodzaj, jawność, konieczność i wpływ brakującego celu. Transkrypcję odróżnić
od interpretacji; brak źródła od pominięcia relacji. Dwa osobne wyniki na
eval-v1, z pointer/hash/bajtami, recenzentem, zakresem i niepewnościami.
''' + ('''W tej pierwszej partii dodatkowo porównać 5/3 zamrożonych par wykonawczych,
7 wzmianek i 7 kontynuacji oraz brakujące krytyczne pary, pięć nowych
krawędzi kontekstu i nierozstrzygniętą ścieżkę trzech kroków. Nie naprawiać
odpowiedzi i nie nadawać automatycznych TP/FP/FN.
''' if n==1 else '') + '''Jedna część do 90 minut. Jeśli oszacowany zakres jest większy, podzielić
go z pełnymi listami ID PRZED przeglądem znaczenia i zaktualizować karty,
ROADMAP i STATUS. Nie zastępować realnego review samym rejestrem pending.

## Artefakty wyjściowe i lokalizacje

Nowy reviews/semantic-01/part-04b'''+str(n)+'''/ (comparisons, review, issues,
owner-focus, presentation, manifest), additive current-state i nowy pomiar
M-POC5A-semantic-04b'''+str(n)+'''/. Wpis sessions.jsonl append-only.

## Kryteria zakończenia i kontrole

Wszystkie przypisane ID rozliczone źródłowo, ocenione lub jawnie blokowane;
brak automatycznej akceptacji. scripts/check.ps1, git diff --check,
rzeczywiste logi i audyt niezmienności. Tylko decyzja człowieka akceptuje znaczenie.

## Zakres wyłączony

Inne partie, .4c/.4d, nowe źródła/pass-02, ekstrakcja i korekty,
API inferencji/automatyczne procesy modelowe, M-POC5B/20 sytuacji, M-POC6/7
i architektura. Nie rozszerzać eval-v1/gold ani wyborów właściciela.

## Przegląd człowieka

Pokazać decyzje po ludzku: co mówi źródło, co zapisał model, gdzie jest
różnica i co zmienia; potem proponowana decyzja i wyłączenia. Pełne ID,
hash/pointer/bajty zostają w prywatnym pakiecie. Brak decyzji waiting_review.

## Wznowienie

Od scope-plan i aktualnego current-state; wszystkie wcześniejsze pending
zachować. Nie utożsamiać poprawnego source requirement z zamkniętym wynikiem.

## Przekazanie

Następna osobna część z zachowaniem wszystkich pending. Nadrzędne .4b,
.4 i M-POC5A partial do pełnego rozliczenia i decyzji. M-POC5 jedyny next.

## Dokładne ID relacji tej partii

'''+', '.join(part['output_edge_ids'])+'.\n'
    assert not path.exists();path.write_text(text,encoding='utf-8')
print(json.dumps(dict(parts={s['part']:dict(ids=len(s['output_edge_ids']),occurrences=s['occurrences']) for s in scope},protected_files=len(protected))))
