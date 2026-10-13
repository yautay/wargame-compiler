"""Record the real owner review and publish only aggregate session status."""
from prepare import ROOT, P, M, I, now, load, record, write, verify
import shutil

verify(load(M / 'baseline.json')['files'])
write(M / 'owner-visual-review.json', {
    'recorded_at_utc':now(), 'card':'M-POC2A', 'reviewer':'owner in this chat',
    'raw_response':'jest ok', 'in_reply_to':'Review of readability of new PDF 31-37 renders and core boundaries, with review.html opened for inspection',
    'readability_and_boundaries_confirmed':True, 'semantic_extraction_approval':False,
    'evaluation_scope_or_limits_changed':False, 'review_html':record(M / 'review.html'),
    'reviewed_package_manifest':record(I / 'manifest.json'),
})
for name in ('STATUS.md','HANDOFF.md','ROADMAP.md'):
    destination = M / 'bootstrap-before' / name
    destination.parent.mkdir(exist_ok=True)
    assert not destination.exists()
    shutil.copyfile(ROOT / 'docs' / name, destination)

manifest_hash = record(I / 'manifest.json')['sha256']
seal = load(M / 'package-seal.json')
status_path = ROOT / 'docs/STATUS.md'
old_status = status_path.read_text(encoding='utf-8')
history = old_status[old_status.index('## Historia wcześniejszego przygotowania i przekazania'):]
history = history.replace('## Niewykonane i otwarte', '## Historyczny stan otwartych kwestii przed freeze (zastąpiony powyżej)')
status_path.write_text(f'''# STATUS

- **Data aktualizacji:** 2026-10-09
- **Bieżący milestone:** M-POC2
- **Bieżąca karta:** M-POC2B
- **Wynik M-POC0:** done
- **Blokady:** brak technicznych; M-POC2B czeka na ręczne otwarcie czystej sesji i przekazanie pakietu przez właściciela
- **Wynik M-POC1A:** done — przegląd struktury źródła zakończony w zapisanym zakresie
- **Wynik M-POC1B:** done — przegląd oczekiwań i sytuacji zakończony
- **Wynik M-POC1C:** done — decyzje 06/07 zapisane, eval-v1 zamrożone
- **Wynik M-POC2A:** done — pakiet przygotowany, oględziny właściciela potwierdzone
- **Wynik M-POC2B:** planned — pierwsza ekstrakcja niewykonana

M-POC2A zakończono na feature/tests w C:/repo/wargame-compiler. Pakiet zawiera
7 pełnych renderów 200 dpi, 12 wycinków core, 4 wycinki kontekstu granicznego,
tekst pomocniczy, mapę zakresu, minimalny format, syntetyczny przykład, prompt,
metadane freeze, manifest i transfer-list — łącznie {seal['file_count']} pliki.
Główny zakres i kontekst są oddzielone; nie dodano stron poza PDF 31–37.

Kanoniczne artefakty pod private/poc/spqr-chapter9/: inputs/v1/, formats/
i prompts/first-v1.txt. Odseparowany katalog dla czystej sesji:
transfer/first-v1/ — wyłącznie pliki z transfer-list; bez klucza oceny,
raportów, handoffów, historii decyzji i pełnego 44-stronicowego PDF.
Manifest wejść SHA-256: {manifest_hash}.
Przekazanie jeszcze nie nastąpiło; plików pakietu nie zmieniać po wysłaniu.

Codex obejrzał wszystkie pełne strony, granice, tabelę i diagramy. Właściciel
potwierdził oględziny odpowiedzią „jest ok”. Techniczne kontrole hashy,
odseparowania, 16 wycinków i tekstów oraz przykładu syntetycznego passed.
722 zastane chronione pliki, w tym zamrożona ocena i indeks Git, bez zmian.
Wstępne scripts/check.ps1: 101 passed. Końcowy wynik i logi prowadzi
measurement/M-POC2A-001/completion.json; nie jest to pomiar jakości ekstrakcji.

Zamrożony eval-v1 i zgody 06/07 zachowane. Zakres: 66 lokalnych grup treści,
8 wymagań kontekstu, 20 sytuacji (17/3), 5 relacji jawnych i 3 niejawne.
105 pozostałych propozycji poza gold; 7 wzmianek i 7 kontynuacji osobno.
Progi/limity bez zmian. Aktywny czas człowieka, tokeny i cena nadal unknown.
Lokalna .venv zawiera pytest; Poppler/pdfplumber/Pillow z runtime Codex.

Dokładny następny krok: właściciel otwiera czystą sesję w odseparowanym
transfer/first-v1/ i przekazuje tylko transfer-list, manifest, prompt, format
i wymienione pliki. Ekstraktor nie otwiera głównego repo ani dokumentów oceny.
Model/rozumowanie zapisuje się z faktycznie widocznej konfiguracji albo unknown.
Ten czat jest sesją przygotowania, nie ślepą pierwszą ekstrakcją.
M-POC2B i dalsze karty niewykonane; jakość n/a. M-POC2 jedyny next.

''' + history, encoding='utf-8', newline='\n')

handoff = f'''# M-POC2A — pakiet wejściowy do pierwszej ekstrakcji

- **Milestone:** M-POC2
- **Karta:** M-POC2A
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2B

Data: 2026-10-09, Europe/Warsaw. Wykonawca: Codex, ręczna sesja przygotowania.
Pracowano bezpośrednio na feature/tests w C:/repo/wargame-compiler.

## Wejścia, wynik i hashe

Zweryfikowano stabilny prywatny PDF, source-v1 i supplement lokalizacji oraz
zamrożony eval-v1/freeze-public-v1. Źródło SHA-256:
e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e.
Manifest eval-v1: 7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
Nie zmieniono zakresu, oczekiwań, progów ani limitów.

Pod private/poc/spqr-chapter9/ utworzono inputs/v1/ z pełnymi obrazami PDF
31–37 (200 dpi), 12 wycinkami core, 4 wycinkami kontekstu, automatycznym
tekstem i mapą współrzędnych. Format i fikcyjny przykład są w formats/;
dokładny prompt w prompts/first-v1.txt. Manifest i transfer-list w inputs/v1/.
Manifest wejść SHA-256: {manifest_hash}.
Pełne hashe wszystkich plików: manifest i measurement/M-POC2A-001/package-seal.json.

Odseparowany katalog transfer/first-v1/ zawiera dokładnie {seal['file_count']} pliki
({seal['total_bytes']} bajtów), identyczne z allowlistą. Nie zawiera ocen,
raportów, historii decyzji, handoffów, skryptów przygotowania ani pełnego PDF.
Kopia freeze-public-v1 zawiera tylko metadane i zachowała oryginalne bajty.
To katalog do ręcznego otwarcia jako osobny workspace, bez głównego repo.
Nie przekazano jeszcze plików do ekstraktora; pliki zachować po wysłaniu.

## Kontrole, przegląd i ograniczenia

Codex obejrzał wszystkie 7 pełnych stron oraz kluczowe wycinki granic, tabeli
i diagramów. Właściciel odpowiedział „jest ok” na prośbę o oględziny
czytelności i granic. Dowód i hash oglądanego pakietu:
measurement/M-POC2A-001/owner-visual-review.json.
Nie jest to akceptacja przyszłego znaczenia reguł ani grafu.

Hashe pakietu i kopii przekazania zgodne. Niezależnie sprawdzono 16 wycinków
pikselowo i 16 pomocniczych tekstów wobec PDF, kolejność oraz granice.
Fikcyjny przykład parsuje się, ma poprawne ID/referencje i stany wartości.
722 zastane chronione pliki (w tym wcześniejsze handoffy, źródła, oceny,
decyzje i indeks Git) bez zmian. Kontrola ciągłości obsługuje teraz poprawne
przejście M-POC2A → M-POC2B i odrzuca przejście bez ukończenia A.
Wstępne kontrole scripts/check.ps1: 101 passed; końcowe logi, wynik i hashe
w measurement/M-POC2A-001/completion.json. Lokalny TMP/TEMP i nowy basetemp.

Tekst jest automatyczny, nie korektą glifów; pełne rendery mają pierwszeństwo.
Nie dodano kontekstu poza siedmioma stronami. Środowisko .venv lokalne;
pytest do kontroli, Poppler/pdfplumber/Pillow z runtime Codex. Początkowe
ensurepip i połączenie PyPI w sandboxie nie powiodły się; lokalny pytest
zainstalowano po dopuszczonym ponowieniu sieciowym. Brak zmian legacy.

Czas kalendarzowy od pierwszego zarejestrowanego zegara i końcowe metadane
są w completion; zegar pomija bootstrap. Czas aktywny człowieka/modelu,
tokeny i cena unknown. Przygotowanie nie zużyło rund ekstrakcji/kontekstu/korekt.

## Dokładne wznowienie

Właściciel ręcznie otwiera czystą sesję w
C:/repo/wargame-compiler/private/poc/spqr-chapter9/transfer/first-v1/.
W sesji przekazuje wyłącznie pliki z inputs/v1/transfer-list.txt i uruchamia
prompts/first-v1.txt. Proponowana konfiguracja eksperymentu: GPT 6.1 Sol / wysoki;
zapisać faktycznie widoczne selektory lub unknown, bez deklaracji na podstawie planu.
Ekstraktor weryfikuje hashe, ogląda obrazy i zwraca jedną oryginalną odpowiedź.
Właściciel zachowuje surowe bajty, fakty przekazania i dowody sesji M-POC2B.
Nie otwierać tam STATUS/HANDOFF/evaluation/ ani klucza oceny. Przy ekspozycji
oczekiwań oznaczyć contaminated. Błędny hash/brak wejścia zatrzymuje próbę.

M-POC2B jeszcze nie wykonano, odpowiedzi nie ma, jakość n/a. M-POC2 jedyny next.
M-POC3 zacznie się dopiero od oryginalnej odpowiedzi. Nie wykonywano API,
automatyzacji GUI, innych czatów, inferencji, commita/pusha ani zmian innych repo.
'''
write(ROOT / 'docs/handoff/2026-10-09-M-POC2A.md', handoff)
(ROOT / 'docs/HANDOFF.md').write_text(f'''# HANDOFF

- **Ostatnia sesja:** [2026-10-09-M-POC2A](handoff/2026-10-09-M-POC2A.md)
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2B

M-POC2A zakończone: wejścia PDF 31–37, minimalny format, fikcyjny przykład,
prompt, manifest i transfer-list. Oględziny właściciela potwierdzone.
Pakiet ma {seal['file_count']} pliki; hashe i kontrola odseparowania poprawne.
Manifest wejść SHA-256: {manifest_hash}.
Końcowe kontrole: private/poc/spqr-chapter9/measurement/M-POC2A-001/completion.json.

Właściciel otwiera ręcznie czystą sesję w odseparowanym katalogu
C:/repo/wargame-compiler/private/poc/spqr-chapter9/transfer/first-v1/,
z wyłącznie plikami z inputs/v1/transfer-list.txt i prompts/first-v1.txt.
Nie przekazywać głównego repo, evaluation/, raportów ani handoffów oceny.
M-POC2B i pierwsza ekstrakcja niewykonane; jakości nie zmierzono.
eval-v1 i wcześniejsze zgody zachowane. M-POC2 jedyny next.

[STATUS](STATUS.md), [ROADMAP](ROADMAP.md), [plan](POC-PLAN.md).
''', encoding='utf-8', newline='\n')
roadmap_path = ROOT / 'docs/ROADMAP.md'
roadmap = roadmap_path.read_text(encoding='utf-8')
roadmap_path.write_text(roadmap.replace('| M-POC2 | next | Niezmienne wejścia, format i pierwsza ręczna ekstrakcja |', '| M-POC2 | next | M-POC2A done: odseparowany pakiet 33 plików, hashe i oględziny właściciela; M-POC2B niewykonane, ręczna czysta sesja jako następny krok |'), encoding='utf-8', newline='\n')
print('Owner review recorded; STATUS, ROADMAP and HANDOFF advance to M-POC2B')
