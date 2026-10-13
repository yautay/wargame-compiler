"""One-session formatting of manually authored review data; no inference or legacy imports.
Not an importer, runtime schema, pipeline or rule engine. Source IDs/evidence are attached
to the explicit human-readable proposals below. Outputs must not exist before this run.
"""
from pathlib import Path
import json, hashlib, copy
from collections import Counter
from datetime import datetime, timezone

ROOT = Path('C:/dev/wargame-compiler')
P = ROOT / 'private/poc/spqr-chapter9'
SESSION = P / 'measurement/M-POC1B-001'
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value):
    assert not path.exists(), f'Refuse to overwrite {path}'
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

source = read(P / 'source/source-v1.json')
inventory = read(P / 'evaluation/draft/inventory.json')
candidates = read(P / 'evaluation/draft/dependency-candidates.json')
manifest = read(P / 'evaluation/owner-review-001/review-manifest.json')
assert sha(Path(source['source']['path'])) == source['source']['sha256']
for row in manifest['baseline_original_artifacts'] + manifest['files']:
    assert sha(P / row['path']) == row['sha256'], row['path']
items = {x['id']: copy.deepcopy(x) for x in inventory['items']}
for name in manifest['supplement_order']:
    supplement = read(P / 'evaluation/owner-review-001' / name)
    for item in supplement.get('items', []):
        assert item['id'] not in items
        items[item['id']] = copy.deepcopy(item)
    for change in supplement.get('field_overrides', []):
        if change['field'] == 'classification':
            items[change['id']]['classification'] = change['reviewed_value']
        elif change['field'] == 'evidence[0].bbox_pdf_points':
            items[change['id']]['evidence'][0]['bbox_pdf_points'] = change['reviewed_value']

def evidence(refs):
    result = []
    for ref in refs:
        item = items[ref]
        for raw in item['evidence']:
            e = copy.deepcopy(raw)
            # Original pending fields describe the historical read, never new approval.
            e.pop('human_review', None)
            e['inventory_ref'] = ref
            e['parent_inventory_ref'] = item.get('parent_id')
            e['locator_policy'] = 'Containing envelope; exact child span is source_span when present; not a new glyph-level box.'
            if 'source_transcription' in item:
                e['source_span'] = item['source_transcription']
            e['M_POC1B_read'] = 'Codex manual review of unchanged PDF31–37 renders and helper locators'
            result.append(e)
    return result

common = {
    'card': 'M-POC1B', 'date': '2026-10-07', 'version': 'M-POC1B-draft-001',
    'assessment_version': 'draft_unfrozen', 'source_id': source['id'],
    'source_sha256': source['source']['sha256'],
    'owner_review_basis': {'path': 'evaluation/owner-review-001/review-manifest.json',
                         'sha256': sha(P / 'evaluation/owner-review-001/review-manifest.json'),
                         'scope': 'M-POC1A inventory boundaries/structure/policy only; no semantic acceptance'},
    'author': 'Codex, manual session in this chat',
    'human_review': {'status': 'waiting_review', 'reviewer': None, 'date': None, 'approved_ids': []},
    'frozen': False, 'gold': False,
    'status_policy': {
        'source_supported_proposal': 'Codex finds sufficient chapter evidence for the stated local proposition, conditional on its scope. Not owner-confirmed or semantic gold.',
        'requires_context': 'Named missing target/data blocks the specified full resolution; local known facts remain available.',
        'unresolved_interpretation': 'Source wording or conflict does not justify a unique interpretation; owner review needed.',
        'owner_confirmed': 'Only an actual scoped owner decision may populate this category; currently zero.'},
    'scope_limits': ['Not a complete atomic inventory or graph of the rulebook',
                     'No source beyond PDF31–37 added; boundary context remains separate',
                     'Synthetic inputs do not establish eligibility or facts of a real scenario',
                     'No answer to M-POC2B exists; author has seen evaluation and cannot be a blind extractor'],
}

# Each line is a manually selected assessment proposition, not an inferred rule.
# Local full-result context can still be required even when the proposition is supported.
expectation_text = r'''
C-9.11-01,C-9.11-02,C-9.11-03,C-9.11-04,C-9.11-05|condition,negation,time|source_supported_proposal|Pass-Thru jest opcją piechoty atakowanej od Front przez EL z SHOCK MUST CHECK TQ; decyzja przed Pre-Shock DR, co najmniej jeden wolny Rear. Flank/Rear, współatak innych jednostek lub enemy ZOC na początku Orders Phase wykluczają opcję. Przy dwóch obrońcach obaj muszą spełniać warunki.|Zmiana czasu lub pominięcie jednej negacji zmienia legalność.|Pełny Shock i definicje Front/Rear/ZOC są celami zewnętrznymi; nie wyliczać ich z tego akapitu.
C-9.11-07,C-9.11-08|number,effect|source_supported_proposal|Wybrany Pass-Thru daje piechocie +1 DRM do Pre-Shock TQ; Hits obrońcy z rozstrzygnięcia Shock dzielone przez 2 z zaokrągleniem w dół, Hits EL zmniejszone o 1.|Zły znak, adresat albo zaokrąglenie zmienia liczbę Hits.|Bazowy wynik Shock musi być dostarczony; kolejność innych modyfikatorów i dolna granica redukcji EL do przeglądu.
C-9.11-09|condition,effect,time|source_supported_proposal|Po Shock przesunięcie EL do wybranego przez gracza EL wolnego Rear obrońcy następuje tylko gdy piechota nie Rout i EL nie Rampage; facing zachowany.|Nie wolno przenieść EL mimo Rout/Rampage lub do zajętego Rear.|Stan Rout wymaga procedury ogólnej; Rampage ma wewnętrzny cel R-9.14.
C-9.11-10,C-9.24-03|exception,number|source_supported_proposal|Końcowy Pass-Thru TQ Check nie dotyczy SK; dla innych obrońców Hits stanowi dodatni nadmiar DR ponad TQ. To odrębny test od Pre-Shock.|Usunięcie wyjątku SK lub utożsamienie dwóch testów zmienia wynik.|Nie rozszerzać wyjątku na wszystkie testy TQ.
C-9.12-02,C-9.12-03|condition,exception|source_supported_proposal|Screen strzela wyłącznie Reaction Fire, wiersz Elephant Screen MRRC; własne znaczniki podaży. Leader Elephant nie ma Screen.|Zgubienie only lub wyjątku daje dodatkowy atak.|Pełny wynik ognia wymaga 8.2 i wiersza MRRC.
C-9.13-01,N-03-S2|definition,effect,exception|source_supported_proposal|Riders są Mounted Javelinists dla Missile Fire; javelins i screen przy Reaction Fire mają osobne rzuty. Nota nie wyłącza reguły przy braku historycznej wieży.|Jeden wspólny rzut lub historyczna rekonstrukcja wyłączająca regułę zmienia ogień.|Tożsamość wiersza MRRC z samego Mounted Javelinists pozostaje hipotezą DC-031.
C-9.14-01,T-01,TR-01,TR-02,TR-03|table,number,exception|source_supported_proposal|Rout EL uruchamia Rampage. T-01 jest jedną tabelą z 0, 1–6, 7–9; dla zwykłego EL 0 kieruje ku najbliższemu friendly (remis wybiera przeciwnik), 1–6 korzysta z kompasu mapy, pierwszy 7–9 od źródła Rampage, kolejny 7–9 eliminuje.|Rozdzielenie tabeli lub zgubienie first/subsequent zmienia wynik.|Kierunku na rzeczywistej mapie nie ustala sam przykład D-01.
TR-01,TR-03,C-9.14-11|exception,number|source_supported_proposal|Leader Elephant przy 0 jest eliminowany; przy późniejszym 7–9 zamiast eliminacji jest natychmiast rallied z Hits=TQ−2. Jest to lokalny szczególny przypadek wobec ogólnego zakazu rally Rampage.|Pominięcie szczególnego wyjątku zmienia stan jednostki.|Zakres Leader Elephant przy pierwszym 7–9 jest odrębnym nierozstrzygniętym oczekiwaniem.
TR-03,C-9.14-11|exception,time|unresolved_interpretation|Nie ustalono, czy końcowe If it is a Leader Elephant obejmuje również pierwszy 7–9 czy tylko kolejne rzuty; nie przypisać temu pełnego zakresu bez decyzji.|Szeroki albo wąski zakres zmienia Rampage/rally na pierwszym rzucie.|Przegląd składni tabeli i uzasadniona decyzja właściciela.
TR-02,D-01,X-01|graphic,definition|requires_context|Wynik 1–6 wymaga kompasu konkretnej mapy; kierunek geograficzny przy vertex odróżniony od ruchu przez hexside. D-01/X-01 jest przykładem, nie globalnym kompasem.|Zmyślona orientacja zmienia heksy ruchu.|Wskazana mapa bitwy z dowodem i kompasem, bez domknięcia całej instrukcji.
C-9.14-02,C-9.14-11|time,exception,negation|source_supported_proposal|Każdy Rampage kończy się natychmiast przed inną mechaniką, z wyjątkiem OW wobec EL; nie ma równocześnie dwóch Rampage. EL w Rampage nie ma ZOC, nie wyzwala Reaction Fire żadnego rodzaju i nie jest zwykle rally.|Równoległe procedury, ZOC albo dodatkowy ogień zmieniają rozstrzygnięcie.|OW 6.51 wymaga zewnętrznej procedury; szczególny Leader Elephant zachować oddzielnie.
C-9.14-03,C-9.14-04|number,effect,condition|source_supported_proposal|Na directional DR EL próbuje przejść 3 heksy; przed zajętym hekssem zatrzymuje się sąsiednio. Trafiona piechota dostaje 1 Hit od Front lub 2 od Flank/Rear; kawaleria zawsze 2; w stosie oba oddziały dostają Hits. Leader bez możliwości withdrawal ginie bez rzutu.|Typ, kierunek, 3 heksy i przypisanie Hits zmieniają skutki.|Możliwość withdrawal leadera wymaga 4.72; geometrię i typy przyjąć tylko jako jawne dane przypadku.
C-9.14-06,C-9.14-07,C-9.14-08,C-9.14-09|number,condition,time|source_supported_proposal|Rampage kończy zejście z mapy, eliminacja po mahout DR, odległość co najmniej 8 od najbliższej jednostki lub po czwartym kolejnym Rampage DR jeśli brak wcześniejszych warunków.|>8 zamiast ≥8 lub zła liczba rzutów zmienia czas eliminacji.|Nie dorabiać pomiaru odległości na nieznanej mapie.
C-9.14-10|effect,exception|source_supported_proposal|Stacked leader jedzie z EL; na końcu Rampage sprawdza casualty 4.73, ocalały pozostaje w końcowym miejscu; zejście EL z mapy eliminuje obu.|Brak casualty albo wyjątku off-map zmienia stan leadera.|Wynik casualty wymaga 4.73; nie wyliczać prawdopodobieństwa bez celu.
C-9.15-01|negation,number,exception|source_supported_proposal|Kawaleria nie wchodzi dobrowolnie w enemy EL ZOC, wejście Flank/Rear kosztuje po 2 Hits na heks; wymuszone wejście w ZOC ma tę samą karę. Nie atakuje Front EL; Flank/Rear nie daje zwykłej Attack Superiority.|Wymuszone ≠ dobrowolne i brak AS są krytyczne.|Wyliczenie geometrii ZOC i bazowego Shock wymaga reguł ogólnych.
C-9.16-01|condition,time,exception|source_supported_proposal|Zbliżenie zwykłego EL z nieprzyległego heksu do enemy cavalry nakazuje próbę OW; gdy można się wycofać, brak dowolnego Reaction Fire. Jeśli nie można: natychmiastowy TQ check; routed cavalry eliminowana bez DR. Reguła wyłącza Leader Elephants.|Zmiana triggera, czasu lub wyjątku zmienia reakcję.|OW i ustalenie możliwości withdrawal wymagają kontekstu; zakres minimum dla DR≤TQ osobno.
C-9.16-01|number,condition|unresolved_interpretation|Dla kawalerii bez OW zdanie If DR is higher ... with a minimum result of 1 nie daje w tej ocenie zatwierdzonego wyniku przy DR≤TQ. Zablokować tę granicę zamiast zgadywać 0 albo 1.|Różnica 0/1 Hit jest krytyczna.|Właściciel rozstrzyga zakres minimum z tekstem lub wskazuje potrzebny dowód.
C-9.17-01|negation,exception|source_supported_proposal|EL przeciw EL: żadna strona nie uzyskuje Position Superiority, także atak Flank/Rear nie daje AS.|Błędny bonus pozycyjny zmienia Shock.|Nie rozszerzać zakazu na wszystkie rodzaje superiority.
C-9.18-01|condition,exception|requires_context|EL może być dowodzony przez dowolnego leadera unless specifically otherwise; sprawdzenie konkretnego uprawnienia wymaga wyjątków właściwego scenariusza/reguł.|Domniemanie braku wyjątku daje nieuprawniony rozkaz.|Wskazany leader, scenariusz i źródło jego ograniczeń; lokalna reguła ogólna pozostaje znana.
C-9.19-01|number,condition,table|source_supported_proposal|Indian vs African: African EL +1 DRM Pre-Shock, dodatkowo do not na dwóch nazwanych charts; nie dla wszystkich EL i nie zamiast tabel.|Zły adresat lub zastąpienie tabel zmienia wynik.|Clash of Spears and Swords, Shock Superiority oraz 8.43 wymagają źródeł do pełnego Shock.
N-07-S2,C-9.21-01|definition,exception|source_supported_proposal|Velites są LI, nie SK; wyjątki SK nie przechodzą na Velites przez podobieństwo funkcji. OW: SK Hits tylko przy Rear, Velites przy Flank lub Rear.|Błędna klasyfikacja zmienia wyjątki legalności i Hits.|Added maneuver nie definiuje wszystkich uprawnień; procedura OW pozostaje zewnętrzna.
C-9.21-01|number,condition|source_supported_proposal|SK mogą OW do 2 heksów przed jednostką o MA takim samym lub mniejszym, niezależnie od różnicy MA.|Zła nierówność albo 2 heksy zmienia legalność.|Pełna trasa OW wymaga procedury, mapy i danych.
C-9.22-01|number,negation|source_supported_proposal|Target SK daje +2 DRM Missile Fire; SK oraz LI Archers Class A nie mogą H&D. LC dowolnej missile class nie może H&D przeciw SK.|Zmiana target/source lub zgubienie negacji zmienia legalność.|Wynik ognia wymaga MRRC i H&D; brak zakazu nie dowodzi pełnej legalności.
C-9.23-02,C-9.23-03,C-9.23-04|negation,exception,condition|source_supported_proposal|SK nie może Shock attack; atakujący wyłącznie SK nie robi Pre-Shock TQ mimo markera. Przy obronie SK z innym typem wybierany jest inny typ, Size SK ignorowany.|Alone i wybór obrońcy są krytyczne.|Nie przypisywać SK immunitetu od innych testów ani obrońcy mieszanego.
C-9.23-05|number,effect|source_supported_proposal|Hits zadawane przez SK w Shock: połowa w dół, najwyżej 1 Hit.|Zły limit lub zaokrąglenie zmienia wynik.|Bazowe Hits muszą być podane; kolejność innych modyfikatorów wymaga kontekstu.
C-9.23-06|condition,exception|source_supported_proposal|PH/HI/LG zaatakowani od Front przez LI nie robią Pre-Shock TQ mimo markera atakujących; LI nadal robią. Odwrotność nie obowiązuje: PH/HI/LG atakując LI robią test.|Odwrócenie kierunku wyjątku zmienia testy.|Nie rozszerzać na Flank/Rear ani inne typy.
C-9.24-02,C-9.24-04|exception,number|source_supported_proposal|Rout SK oznacza eliminację; SK zmienia facing za 0 MP i powtarza ruch w Game Turn bez cohesion cost; special stacking wskazuje 6.69.|Błędna jednostka lub koszt zmienia stan/ruch.|Koszty terenu i pełny stacking nie są wyłączone.
C-9.24-05,X-03|condition,number|source_supported_proposal|Przy ustalaniu line pojedynczy SK lub Velites w przerwie nie przerywa line. Przykład pozwala kilka oddzielnych przerw po jednej jednostce; nie pozwala przerwy dwóch kolejnych.|Globalne najwyżej jeden zamiast po jednym w przerwie zmienia LC.|To lokalny wyjątek; pozostałe warunki 4.32 wymagają kontekstu.
C-9.31-01|condition,exception|source_supported_proposal|Missile LC H&D tylko przeciw niższemu MA, z wyjątkiem SK; LC Archers mogą fire podczas OW przez 6.55.|≤ zamiast < albo pominięcie SK zmienia legalność.|Sama przewaga MA nie domyka H&D; konieczna procedura 8.3.
C-9.32-01|number,condition|source_supported_proposal|Hits zadane przez atakującą LC przeciw PH/HI/MI/LG/BI są dzielone przez 2 w dół.|Zastosowanie do obrońcy LC albo innych typów zmienia Hits.|Zależność od AS w przykładzie X-04 wymaga osobnej interpretacji/kontekstu.
C-9.32-01,X-04|number,table,exception|requires_context|X-04 mówi o printed result przy LC z AS przeciw HI, podczas gdy reguła mówi halve. Bez reguły superiority i tabel nie ustalać kolejności ani nowego wyjątku od połowy.|Możliwe anulowanie/mnożenie przed redukcją zmienia liczbę.|Ograniczony dowód bazowego AS/CRT; decyzja właściciela o kolejności.
C-9.41-01|condition,number,exception|source_supported_proposal|Moving Front attack na PH: za każdy flank occupied friendly PH lub friendly PH ZOC 2L, przy HI 1L. Brak dla started adjacent/stayed, Flank/Rear i jeśli dowolny attacker PH.|Zgubienie moving, per flank lub any zmienia kolumnę.|Lokalny shift, nie pełny wynik CRT bez tabeli.
N-09-S2,C-9.51-01,X-06|condition|requires_context|Wstęp DD odsyła po listę eligible units do scenario-specific rules. Nie każda PH z definicji jest uprawniona; przykład Cynoscephalae nie dostarcza tej listy.|Zgadywana eligibility legalizuje formację.|Wybrany scenariusz z listą uprawnionych jednostek.
C-9.51-01|condition,number,time|source_supported_proposal|DD dwóch PH wymaga IO lub LC bezpośrednio OC; back zaczyna bezpośrednio za front, wchodzi za normalny terrain cost +1 MP, idzie pod front; kończy ruch obu na tę Orders Phase.|Zły leader, MP lub kontynuacja ruchu zmienia legalność.|Eligibility, OC i koszt terenu jako osobne potrzebne fakty.
C-9.52-02,C-9.52-03,C-9.52-04|condition,negation,number|source_supported_proposal|DD orders tylko OC; wspólny ruch za 2 IO albo LC, wolno PAW; nie Wheel/Reverse/Column. Przy unstack top wychodzi normalnie, bottom pozostaje.|Błędne uprawnienia albo zamiana top/bottom zmienia ruch.|Procedury zewnętrzne 6.8/6.44/6.45/6.7 i orders pozostają potrzebne dla pełnego wykonania.
C-9.52-05,C-9.52-06|number,negation|source_supported_proposal|DD zawsze MA4, nigdy MA5; movement Hit przypada obu. Nikt nie przechodzi przez DD ani do DD, traktowane impassable.|Zignorowanie zakazu lub MA zmienia legalność.|Przypadek formowania DD z 9.51 wymaga rozróżnienia etapu od gotowej formacji.
C-9.53-02,C-9.53-03|number,condition,exception|source_supported_proposal|DD sumuje Size; TQ check top, przy ataku Rear bottom; jeśli testowana jednostka dostała Hits, druga także sprawdza.|Wybranie TQ obu naraz albo pominięcie następnego testu zmienia Hits.|Ogólny test TQ i inne modyfikatory poza lokalną selekcją wymagają celu.
C-9.53-04,C-9.53-05,C-9.41-01|number,condition|source_supported_proposal|Przeciw atakowi DD obrońca +1 DRM Pre-Shock; DD broniąc się −1 DRM i może korzystać z Phalanx Defense tylko przy warunkach 9.41.|Zły znak lub bezwarunkowy shift zmienia wynik.|R-9.53→R-9.41 to użycie warunkowej modyfikacji, nie odwrotny kierunek.
C-9.53-06,C-9.53-07|number,effect,exception|source_supported_proposal|DD Shock od Flank/Rear: defender Hits razy3 zamiast razy2; Shock Hits rozdzielane równo, nieparzysty top. Missile Hits top, ale Rear bottom.|Zły mnożnik, odd Hit albo źródło Hits zmienia stan.|Bazowy wynik i kolejność wobec innych mnożników muszą być dostarczone/zweryfikowane.
C-9.53-08|exception,effect|source_supported_proposal|Rout jednej PH w DD powoduje Rout obu; retreat do osobnych heksów, brak możliwości powoduje eliminację zamiast retreat.|Pominięcie sprzężenia albo osobnych heksów zmienia wynik.|Legalne heksy retreat i zakres końcowego the unit wymagają kontekstu przy konfliktach.
C-9.61-01|condition,number,exception|source_supported_proposal|Roman stack: zasadniczo dwa infantry same border bez penalty, ale istnieją wyjątki jak Velites. Wspólny ruch: 2 IO, 1 IO gdy stacked OC sam rozkazuje, albo 1 LC gdy obie eligible.|Pominięcie wyjątku lub jeden IO zawsze zmienia legalność.|Pełny stacking chart i eligibility nie są dowiedzione regułą thumb.
C-9.62-01|number,effect,condition|source_supported_proposal|Roman stack sumuje Size, inne ratings top; każdy własny TQ check ale TQ top; tylko top fire, oba Shock ten sam hex. Automatic Hits każdej jednostce; Shock Hits odsyłają do 8.46 Step4 i10.13.|Zgubienie each albo użycie bottom TQ zmienia liczbę testów/stan.|Rozdział 9 nie domyka alokacji Shock Hits; 10.13 jest kontekstem, 6.68 nieprzejrzane.
C-9.63-01|number,condition|source_supported_proposal|Różne border colors lub same color różne classes w Roman stack: +1 DRM do wszystkich TQ checks.|Błędne and zamiast or albo tylko jeden test zmienia Hits.|Typy i kolory muszą być znane z danych jednostek.
C-9.64-01|negation,condition|source_supported_proposal|Zmiana stacking order tylko IO, nie movement ani LC; LC może zmienić facing. Gdy z Roman stack rusza jedna jednostka, tylko top.|Utożsamienie facing z kolejnością stosu zmienia legalność.|Nie zastosować zwykłego unstack do MLE bez sprawdzenia szczególnej reguły.
C-9.65-01|number,effect|source_supported_proposal|Roman infantry zmienia facing za1 MP, dowolna liczba vertices.|Per vertex zamiast per zmiana zmienia koszt.|Nie rozszerzać tej wartości na MLE, które zachowuje facing.
C-9.66-01-S1,C-9.66-01-S2,C-9.66-01-S3,C-9.66-01-S4,C-9.66-01-S5,C-9.66-01-S6,D-02,CAP-01,CAP-02|condition,negation,graphic|source_supported_proposal|MLE unstack Roman line: top sideways do vacant flank, Clear i poza enemy ZOC; facing zachowany. Nie można wejść zajęty flank ani użyć MLE do stacking together. D-02: górny Original, dolny After; strzałki ilustrują boczne rozłożenie.|Zgubienie negacji/warunku albo odwrócenie paneli zmienia manewr.|Same Line przez4.32, Clear i ZOC wymagają danych/procedur; grafika nie daje ogólnego prawa do dowolnej strony.
C-9.67-01,X-07|time,number,exception|source_supported_proposal|Reakcyjne MLE gdy enemy combat unit wchodzi w odległość2; opcja nie musi być użyta przy pierwszej okazji. OW i MLE mogą współwystąpić, ale nie przez te same units.|Ta sama jednostka używająca obu narusza wyjątek.|OW i legalność line muszą być ustalone oddzielnie.
C-9.68-01|condition,number,negation|source_supported_proposal|Aktywne MLE tylko LC; po nim obie units mogą move z MA−2; brak Hits za MLE. Column units nie mogą MLE.|IO zamiast LC lub brak MA−2 zmienia legalność/budżet.|Nie przenosić automatycznie post-MLE ruchu na tryb reakcyjny.
C-9.7-01-S1|condition,time,exception|source_supported_proposal|Doctrine obowiązuje Romans przed200 BCE bez Scipio Africanus jako OC; źródło jawnie nakazuje Cannae mimo historycznej obecności Scipio. C-9.7-01-S2 jest opisem, nie dodatkowym warunkiem.|Zła granica czasu albo historia zamiast przypisania gry zmienia stosowalność.|W realnym scenariuszu data i tożsamość OC wymagają dowodów.
C-9.7-01-S1,C-9.71-01,C-9.72-01|condition|requires_context|Dla nieokreślonej bitwy nie ustalać stosowalności doctrine ani progu RP bez daty, OC i Army Withdrawal Level.|Brak danych nie dowodzi ani legalności ani zakazu.|Konkretny scenariusz, OC, AWL/RP i stan mapy.
C-9.71-01,C-9.71-02,C-9.71-03|negation,condition,number|source_supported_proposal|Triarii cannot move ale may face do jednego z dwóch triggerów: enemy combat nie EL w3 iLOS dowolnej Triarii line unit; albo co najmniej6 od wszystkich Roman/Ala infantry lines, z wyłączeniem allied. To alternatywa OR.|Nagłówek mieszany, wyjątek EL i kwantyfikatory są krytyczne.|Line, LOS, odległości i identyfikacja wojsk wymagają jawnych danych.
C-9.72-01|number,condition,exception|source_supported_proposal|Move+Shock Triarii wymaga RP≥floor(AWL/2); zawsze mogą Shock bez ruchu enemy w swojej ZOC. Próg nie usuwa odrębnej bramki ruchu9.71.|Błędne zaokrąglenie albo ruch z wyjątku stojącego Shock zmienia legalność.|9.71 i9.72 czytane razem; full legal attack nadal wymaga innych warunków.
C-9.81-01|definition,negation|source_supported_proposal|Scorpio bolt-firing B, built-in crew, TQ; traktowany LI dla movement i obrony Shock/Missile. Nie Shock-capable; ofensywnie tylko Missile Fire.|Traktowanie jako LI także w ataku daje nieuprawniony Shock.|Pełne LI defense/movement i bolt MRRC wymagają kontekstu.
C-9.82-01,N-11|condition,negation,time,graphic|source_supported_proposal|Scorpio mode zmienia IO friendly leadera. Fire nie move, Move nie fire; w phase przełączenia do Move nie rusza, do Fire nie strzela. Ruch wymaga IO, ogień nie. N-11 wiąże front=Fire, reverse=Move.|Usunięcie blokady phase przełączenia zmienia tempo; no orders nie znosi mode.|9.85 uzupełnia harmonogram ognia; źródło nie ustanawia dodatkowej akcji po switch.
C-9.83-01|number,condition|source_supported_proposal|Na heks najwyżej jeden Scorpio; wszystkie inne stacking rules nadal obowiązują.|Wyłącznie one Scorpio nie legalizuje dowolnego stosu.|Pełna legalność współzajęcia wymaga general stacking.
C-9.84-01|definition,exception|source_supported_proposal|Scorpio bez facing; każdy heks Front, move/fire dowolny kierunek niezależnie od orientacji żetonu.|Użycie graficznego obrotu do nadania Rear zmienia obronę.|Nie znosi range/LOS/terrain.
C-9.85-01,G-04|number,time,negation,graphic|source_supported_proposal|Active Scorpio fire max2 na Game Turn, max1 na friendly Orders Phase w Movement/Missile segment bez order; Once→Finished, po fire nic więcej w phase w tym recovery.|Game Turn vs Orders Phase i wykluczenie recovery są krytyczne.|Warunki range/LOS/MRRC i mode9.82 nadal obowiązują.
C-9.86-01,G-05|number,time,exception|source_supported_proposal|Reaction Scorpio fire max2 na enemy Orders Phase w enemy Movement/Missile segment, nawet podczas ruchu; Once→Finished. Ordinary Reaction Fire8.2 jest zabronione.|Przeniesienie active turn cap albo dopisanie ordinary RF zmienia ataki.|No Reaction Fire any kind w Rampage9.14 nadal wyłącza trigger; zewnętrzny ogień i segment wymagają kontekstu.
C-9.87-01|effect,exception|source_supported_proposal|Scorpio ponosi/recover Hits jak inne units; gdy Rout jest natychmiast eliminowany.|Próba rally routed Scorpio zmienia stan.|Trigger Rout i recovery amounts wymagają general rules.
C-9.91-02|negation,effect|source_supported_proposal|BI nie ponosi terrain cohesion przy passable terrain ani facing Rough; nie używa Column/PAW/OW.|Brak cohesion cost nie oznacza braku MP cost lub wejścia w impassable.|Passability/koszt MP wymagają Movement Cost Chart, zakazy nie wymagają wykonania zabronionych procedur.
C-9.93-02,C-9.93-03|number,exception|source_supported_proposal|BI Recovery order usuwa tylko1 Hit; depleted BI eliminowany zamiast Rout.|Większa recovery albo Rout zamiast eliminacji zmienia stan.|Depleted stan i inne warunki recovery wymagają kontekstu; konflikt z Ferocity po depleted elimination nie rozstrzygnięty.
C-9.94-02|number,time|source_supported_proposal|Wszystkie BI startują z Ferocity; −1 DRM BI Pre-Shock i +2 DRM defenders Pre-Shock.|Zły znak lub adresat zmienia wynik.|Inne DRM i Pre-Shock procedure nie są domknięte.
C-9.94-03|condition,number,effect|source_supported_proposal|Każdy Rout BI wyzwala test leader Initiative; DR≤Initiative utrzymuje Ferocity, > traci trwale pod tym leaderem, inne commands bez wpływu.|Błędne ≥ albo globalna utrata zmienia stan grup.|Scenario commander mapping i Initiative muszą być dostępne; depleted elimination ≠ jawny Rout trigger.
C-9.94-03,C-9.95-02|condition|requires_context|Bez scenario setup nie wybrać leadera, Initiative ani członków command do Ferocity/Impetuosity.|Nieznana tożsamość/kontrola blokuje skutek dla konkretnych units.|Jedno wskazane przypisanie scenario wraz z ratings, nie domyślny najbliższy leader.
C-9.95-02|number,time,condition|source_supported_proposal|Start BI MA+1; dowodzący BI −1 do wszystkich first-try Momentum rolls. Po ≥2 BI tej samej command w enemy ZOC Impetuosity trwa do końca Game Turn, potem wygasa tylko tej command.|Nie natychmiast po drugim wejściu i nie całej armii.|Mapping command, ZOC i Momentum wymagają danych; lokalny czas wygaśnięcia jest jawny.
N-14-S2,N-14-S3|negation,table|requires_context|Zachować ignore reference to Chariots on Combat Tables jako instrukcyjny kandydat przy Gallic transport CH; historyczny/scenario opis osobno. Zakres konkretnych charts/wierszy nieustalony.|Usunięcie instrukcji lub objęcie dowolnych chariots zmienia combat.|Dokładne Combat Tables i ich chariot entries, decision owner o zakresie; nie traktować Sentinum/Telamon jako listy eligibility wszystkich LI.
C-9.96-02|definition,negation,effect|source_supported_proposal|CH ma MA bez Size/TQ; bez eligible LI nie rusza, nawet OW. Enemy combat unit moving adjacent do samotnego CH natychmiast go eliminuje.|Nieznana eligibility nie uprawnia do ruchu; static adjacency ≠ podany trigger ruchu.|Eligibility LI scenariuszowa nieuzupełniona; samotny CH da się ocenić lokalnie.
C-9.96-03|number,condition,graphic|source_supported_proposal|CH przewozi jedną LI; CH na top oznacza mounted; kombinacja liczy się jako jedna dla stacking, ale other restrictions nadal obu konfiguracjom.|Dwa LI lub usunięcie innych restrykcji zmienia legalność.|Nie używać roman top/TQ jako zasad CH; brak TQ/Size CH zachować.
C-9.96-03|number,condition,time|source_supported_proposal|LI mount/dismount bez MP/Hit. Dismount continued move tylko jeśli przebyty ruch kombinacji <printed LI MA, pozostałe MP=różnica. Mount: CH MA minus MP LI już użyte.|≤ zamiast <, reset MP albo błędne MA zmienia budżet.|Ocenia się lokalny budżet przy supplied eligibility, MA i MP; trasa wymaga tabeli.
C-9.96-03|number,table,exception|source_supported_proposal|Mounted CH płaci/zakazuje teren przez Movement Cost Chart; movement cohesion tylko LI, nie CH.|Brak Hits CH nie znosi terrain MP/prohibitions.|Konkretna trasa bez Movement Cost Chart pozostaje zablokowana.
C-9.96-05|time,exception|source_supported_proposal|Repeat movement LI bez Hits tylko gdy całą Orders Phase mounted CH; dotyczy second i third movement w Game Turn.|Mount pod koniec phase nie spełnia entire phase.|General repeat movement i pozostałe terrain Hits oddzielnie.
C-9.96-06|negation,definition|source_supported_proposal|Mounted LI nie Shock attack, musi dismount; broni się jako LI.|Defend as LI nie daje ataku mounted.|Dismount nie dowodzi legalności późniejszego attack bez pozostałych warunków.
C-9.96-07|table,exception,number|source_supported_proposal|Mounted LI fire używa Mounted Javelin MRRC; Missile Supply8.17 nie dotyczy while mounted, marker LOW/NO usuwany przy mount; H&D jak cavalry.|Zgubienie while albo pozostawienie markerów zmienia ogień.|Nie zgadywać podaży po późniejszym dismount ani pełnego MRRC/H&D; display annotation06c zachowuje original helper.
G-01,G-02,G-03,D-02,G-04,G-05|graphic|requires_context|Pełna transkrypcja wszystkich małych ratings/napisów żetonów nie jest potwierdzona. Nie używać ilustracji jako listy parametrów scenariusza ani gold wartości jednostek.|Nieodczytane TQ/MA może zmienić wynik; konkretne użycie parametru byłoby krytyczne.|Wybrany żeton/parametr z dokładnym źródłem i przeglądem, tylko jeśli sytuacja go potrzebuje.
'''

expectations = []
for line in expectation_text.strip().splitlines():
    refs, dimensions, status, assertion, risk, limitation = line.split('|')
    refs = refs.split(',')
    i = f'EXP-{len(expectations)+1:03d}'
    expectations.append({'id': i, 'inventory_refs': refs, 'dimensions': dimensions.split(','),
        'status': status, 'proposition': assertion, 'criticality': 'critical',
        'criticality_reason': risk, 'criticality_author': 'Codex proposal, owner justification pending',
        'local_scope_and_needed_context': limitation, 'evidence': evidence(refs),
        'human_review_status': 'waiting_review', 'owner_confirmed': False,
        'dependency_ids': [], 'situation_ids': []})

# Manually assigned dispositions for ALL historical candidate occurrences.
# Compound candidates are retained as audit rows, then split below into review edges.
relation_text = r'''
001|procedure_use|Decyzja Pass-Thru jest przed Pre-Shock DR; źródło używa punktu czasowego8.43.
002|condition|Przeniesienie EL wymaga sprawdzenia braku Rampage według9.14.
003|procedure_use|Screen jest ograniczony do Reaction Fire8.2.
004|exception|OW6.51 jest wyjątkiem od natychmiastowej wyłączności Rampage.
005|condition|Eliminacja leadera zależy od niemożności withdrawal4.72.
006|procedure_use|Na koniec Rampage wymagany leader casualty4.73.
007|modification|+1 African EL modyfikuje Pre-Shock8.43, nie przepisuje tabel.
008|exception|SK wyłączony z końcowego Pass-Thru Check9.11.
009|condition|Odsyłacz wskazuje stacking exceptions6.69 do pełnej legalności stosu.
010|exception|Jedna SK/Velites w przerwie modyfikuje definicję line4.32.
011|procedure_use|LC wykonuje H&D8.3 z lokalnym ograniczeniem MA/target.
012|procedure_use|LC Archer fire podczas OW używa6.55.
013|procedure_use|DD ma prawo PAW6.8; pozytywne wykonanie potrzebuje procedury.
014|exception|DD nie Wheel6.44; do samego zakazu nie trzeba wykonać celu.
015|exception|DD nie Reverse6.45; do samego zakazu nie trzeba wykonać celu.
016|exception|DD nie Column6.7; zakaz nie jest użyciem procedury.
017|procedure_use|DD defense korzysta z warunkowej Phalanx Defense9.41; nie daje jej automatycznie.
018|definition|Roman lines ze spacing wymagają definicji4.32.
019|condition|Oba Roman stack units mają Shock ten sam hex zgodnie8.42.
020|modification|Automatic Hits6.68 mają być zastosowane do każdej jednostki.
021|procedure_use|Hits do alokacji powstają w8.46Step4; bazowa procedura wymagana dla pełnego wyniku.
022|procedure_use|Alokacja Roman Shock Hits wprost delegowana do10.13; cel poza core, zależy dalej od6.68.
023|definition|MLE all top w same Line wymaga definicji4.32.
024|procedure_use|9.82 wskazuje9.85 dla firing without orders; harmonogram nie usuwa mode lock.
025|exception|Scorpio zakaz ordinary RF8.2, nie zgoda na dodatkowe ataki.
026|exception|BI zakaz Column6.7; wynik zakazu lokalny.
027|exception|BI zakaz PAW6.8; wynik zakazu lokalny.
028|exception|BI zakaz OW6.5; wynik zakazu lokalny.
029|exception|Missile Supply8.17 wyłączona while mounted; nie definiuje powrotu supply po dismount.
030|table_use|Screen fire wybiera jawny Elephant Screen row MRRC; pełny wynik potrzebuje wiersza.
031|table_use|Mounted Javelinists9.13 nie nazywa MRRC; konieczność/tabela-row wymaga zewnętrznego dowodu, hipoteza pozostaje.
032|table_use|9.19 mówi in addition to notes on Clash; pełny Shock nie zastępuje tych not lokalnym DRM.
033|table_use|9.19 zachowuje Shock Superiority notes, nie zastępuje ich +1.
034|mention|X-02 podaje bazowy wynik dla ilustracji połowy; sam przykład nie poleca wykonania tabeli.
035|mention|X-04 mówi printed CRT result; wzmianka w przykładzie nie rozstrzyga kolejności AS/halving.
036|table_use|9.41 przesuwa kolumnę Shock Combat CRT; lokalny shift można policzyć bez lookup Hits.
037|mention|Stacking Charts nazwane for a summary. To informacyjny odsyłacz; brak charts nie blokuje jawnej liczby IO, ale pełny stacking wymaga niejawnych exceptionsDC-064.
038|modification|N-14-S2 nakazuje ignore Chariots references; zbiorczy cel nie wskazuje dokładnych charts/entries ani zakresu.
039|table_use|Terrain MP/prohibitions CH wprost przez Movement Cost Chart.
040|table_use|Mounted LI wprost używa Mounted Javelin row MRRC.
041|table_use|9.14 rout EL nakazuje rzut i wynik z lokalnej T-01.
042|definition|TR-02 używa kompasu mapy do odwzorowania1–6 na hexside; to wykonawcza geometria.
043|mention|X-01 poucza o map compass i charakterze przykładu; nie wykonywać oddzielnego drugiego lookup ani podwajaćDC-042.
044|mention|See diagram jest ilustracyjnym odsyłaczem; D-02 wspiera ruch boczny, nie niezależną procedurę ani nowe bonusy.
045|definition|Bez definicji facing/ZOC/markera nie można ustalić rzeczywistej legalności Pass-Thru. Warunki potrzebne wprost, brak exact targets.
046|procedure_use|Pass-Thru jawnie proceed with Shock resolution; podane bazowe Hits pozwalają tylko lokalną transformację.
047|procedure_use|Screens have their own missile supply markers wymaga sposobu supply dla realnego stanu, nie dowodzi osobnego wiersza tabeli.
048|procedure_use|9.13 jawnie Reaction Fire; zasady8.2 nie są automatycznie odczytane.
049|exception|ZOC/facing i AS są różnymi celami: zakazy Front/ZOC i brak AS Flank/Rear zmieniają reguły ogólne.
050|procedure_use|9.16 wymaga OW albo testu TQ i stanu Rout, nie wybiera aliasu8.43 dla tego natychmiastowego testu.
051|exception|ELvsEL wyłącza Position/Attack Superiority; tylko te kategorie.
052|condition|Unless specifically otherwise wymaga identyfikacji ograniczeń dowodzenia realnego leadera, nie dowodzi żadnego konkretnego wyjątku.
053|modification|SK/Velites zmieniają limity/koszt OW; pełna procedura nadal potrzebna.
054|exception|Missile +2 targetSK i H&D zakazy to odrębne cele, nie jeden uniwersalny wyjątek ognia.
055|exception|Attack SK alone wyłącza Pre-Shock także z markerem; other targets nie objęte.
056|exception|PH/HI/LG defensive frontvsLI modyfikują tylko kierunkowe Pre-Shock; reverse nieobjęty.
057|exception|SK eliminated instead of Rout modyfikuje ogólny skutek Rout.
058|condition|N-09-S2 wprost odsyła do listy DD eligible scenario; wykonawcza potrzeba, nie historyczna wzmianka.
059|procedure_use|DD wymaga rozkazu bezpośrednio OC i normal terrain cost+1; IO,LC,OC,terrain to różne cele.
060|modification|DD wybiera top/bottom i drugi TQ check po Hits; generic test i facing rozdzielić.
061|modification|Instead of doubled jawnie modyfikuje general flank/rear multiplier; potrzeba bazowego sposobu łączenia jest niejawna.
062|modification|DD sprzęga Rout obu i retreat separate hexes; legalne retreat require general procedure.
063|mention|Example See scenario Cynoscephalae informacyjny; nie utożsamiać z wykonawczą listą eligibilityDC-058.
064|condition|Rule of thumb plus exceptions i both eligible wymagają niepodanych stacking/LC warunków; brak chart nie nadaje legalności.
065|exception|Roman stacking-order zmiana tylko IO, nie movement/LC; facing LC jest inną akcją.
066|modification|Unlike most other units wskazuje zmianę normalnego facing cost, dokładny cel nie ustalony.
067|condition|MLE wymaga vacant Clear outside ZOC; OW to alternatywa, Clear/ZOC to warunki, rozdzielić.
068|condition|Gdy enemy movement triggers both, OW i MLE nie przez same units; OW trigger pozostaje zewnętrzny.
069|condition|LC only dla active MLE i Column exclusion to oddzielne cele, nie kompletna procedura LC.
070|condition|Stosowalność doctrine wymaga daty i OC scenariusza, nie historycznej wiedzy modelu.
071|definition|LOS oraz Triarii line potrzebne do odległości/trigera9.71.
072|definition|All other Roman/Ala but not allied wymaga identyfikacji line; to potrzebny zakres, nie podobieństwo nazw.
073|condition|Próg9.72 zależy od rzeczywistych RP/AWL; brak parametrów blokuje move+Shock.
074|definition|Scorpio LI for movement/defense i bolt fire wymagają odpowiednich zasad, nie LI shock-attack.
075|procedure_use|Mode/ruch Scorpio requires IO i ramy Orders Phase; oddzielne cele.
076|condition|All other stacking rules apply jednoznacznie zachowuje constraints; exact targets nierozstrzygnięte.
077|definition|Active cap rozróżnia Game Turn, Orders Phase i segment, realne liczniki potrzebują ram czasu.
078|definition|Reaction cap per enemy Orders Phase i segment, nie Game Turn; generic ordinary RF jest osobno wyłączonyDC-025.
079|procedure_use|Scorpio as any other unit potrzebuje recovery/rout trigger; lokalna eliminacja jawna.
080|modification|BI Recovery order limit1 modyfikuje recovery ogólną.
081|exception|Depleted BI elimination zamiast Rout; potrzebna definicja depleted, nie trigger Ferocity z samego słowa elimination.
082|modification|Ferocity zmienia Pre-Shock DRM dla atakującego/defenders; dokładna general procedure nie odczytana.
083|condition|Ferocity result zależy od scenario commander mapping i Initiative Rating, dwóch danych.
084|modification|Impetuosity zmienia first-try Momentum DRM oraz depends command membership; podzielić mechanic modification i scenario condition.
085|condition|Ruch CH wymaga eligible LI; OW wprost w zakresie zakazu ruchu, nie zgoda na ruch samotnego CH.
086|modification|CH+LI single for stacking ale other constraints i MP history wymagają general rules; osobne cele.
087|exception|Entire phase mounted wyłącza repeat-movement cohesion, nie terrain Hits.
088|condition|Defend as LI potrzebuje LI defense; must dismount jest warunkiem attack, nie pełnym uprawnieniem Shock.
089|procedure_use|Mounted LI H&D as cavalry wymaga procedury; nie nadawać innych cavalry attributes.
'''
curation = {}
for line in relation_text.strip().splitlines():
    n, kind, reason = line.split('|')
    curation[f'DC-{n}'] = (kind, reason)
assert len(curation) == 89

# Splits of original compound targets. Exact external identities remain unresolved.
split_targets = {
 '045': [('definition','Front/Rear hex definitions'),('definition','enemy ZOC definition'),('definition','SHOCK MUST CHECK TQ marker')],
 '049': [('definition','ZOC/facing definitions'),('exception','Attack Superiority flank/rear')],
 '050': [('procedure_use','Orderly Withdrawal'),('procedure_use','immediate TQ check in9.16'),('condition','routed cavalry state')],
 '054': [('modification','Missile Fire DR'),('exception','H&D fire eligibility')],
 '059': [('procedure_use','Individual Order or Line Command directly from OC'),('definition','OC identity/authority'),('table_use','normal terrain movement cost')],
 '060': [('modification','general TQ check'),('definition','rear-facing attack geometry')],
 '064': [('condition','Roman/Velites stacking exceptions'),('condition','both units LC eligible')],
 '067': [('mention','Orderly Withdrawal alternative'),('condition','Clear terrain'),('condition','enemy ZOC')],
 '069': [('condition','Line Command eligibility/procedure'),('exception','Column formation MLE prohibition')],
 '070': [('condition','scenario battle date'),('condition','scenario Overall Commander identity')],
 '071': [('definition','LOS'),('definition','Triarii line')],
 '073': [('condition','current Roman Rout Points'),('condition','Army Withdrawal Level')],
 '074': [('definition','LI movement/defense'),('table_use','bolt missile fire')],
 '075': [('procedure_use','Individual Order from friendly leader'),('definition','Orders Phase')],
 '077': [('definition','Game Turn'),('definition','friendly Orders Phase'),('definition','Movement and Missile Fire Segment')],
 '078': [('definition','enemy Orders Phase'),('definition','enemy Movement and Missile Fire Segment')],
 '079': [('procedure_use','Cohesion Hit Recovery'),('condition','Rout trigger')],
 '081': [('definition','Depleted state'),('exception','ordinary Rout consequence')],
 '083': [('condition','scenario BI commander mapping'),('condition','assigned leader Initiative Rating')],
 '084': [('modification','first-try Momentum die roll'),('condition','scenario BI command membership')],
 '085': [('condition','scenario eligible LI'),('exception','Orderly Withdrawal of CH without eligible LI')],
 '086': [('condition','general stacking restrictions'),('modification','movement MP accounting')],
 '088': [('procedure_use','LI Shock defense'),('condition','dismount before Shock attack')],
}

edges, audit = [], []
local = {'002':'R-9.14','008':'C-9.11-10','017':'R-9.41','024':'R-9.85','041':'T-01','044':'D-02'}
negative = {'014','015','016','025','026','027','028','029','051','055','056','057','065','080','081','087'}
for c in candidates['candidates']:
    n = c['id'][3:]
    if c['category'] == 'continuation':
        k = items[c['from']]
        # Fragment addresses prevent apparent semantic self loops.
        from_id, to_id = k['id']+'#start', k['id']+'#continuation'
        e = {'id': f'DEP-{n}', 'candidate_ids': [c['id']], 'from': from_id, 'to': to_id,
             'from_inventory_ref': k['from_item'], 'to_inventory_ref': k['to_item'],
             'kind': 'continuation', 'explicitness': 'explicit', 'executable': False,
             'direction_reason': k['direction_reason'], 'evidence': evidence([k['id']]),
             'target_status': 'internal', 'status': 'source_supported_proposal',
             'criticality': 'critical', 'criticality_reason': 'Ominięcie dalszego fragmentu pomija warunki/skutki; to porządek odczytu, nie zależność wykonawcza.',
             'missing_target_effect': 'Incomplete source read blocks affected expectation; both fragments present.',
             'human_review_status': 'waiting_review', 'owner_confirmed': False}
        edges.append(e)
        audit.append({'candidate_id': c['id'], 'disposition': 'physical_continuation', 'dependency_ids':[e['id']],
                      'reason': 'Fragment start→continuation, never same-parent semantic loop.'})
        continue
    kind, reason = curation[c['id']]
    facets = split_targets.get(n, [(kind, c['target_candidate'].get('name', c['target_candidate'].get('identifier')))])
    dep_ids = []
    for j, (facet_kind, name) in enumerate(facets, 1):
        eid = f'DEP-{n}' + (f'-{j}' if len(facets)>1 else '')
        dep_ids.append(eid)
        target = copy.deepcopy(c['target_candidate'])
        target.pop('fragment', None)
        target['facet'] = name
        explicitness = 'implicit' if c['explicitness'] == 'implicit_candidate' else 'explicit'
        # Explicit named constraints in compound historical hypotheses are classified
        # from source wording, not mechanically inherited from the historical flag.
        if n in {'049','051','055','056','074','076','079','086','088'}:
            explicitness = 'explicit'
        executable = facet_kind != 'mention'
        status = 'source_supported_proposal' if (n in local or facet_kind == 'mention') else 'requires_context'
        if n == '031':
            status = 'unresolved_interpretation'
        if n == '038':
            status = 'requires_context'
        to = local.get(n)
        target_status = 'internal' if to else 'unresolved'
        missing = ('No execution dependency; missing illustration/summary does not alone block local stated result.'
                   if not executable else
                   'Blocks full positive execution on a real state; local prohibitions/arithmetic with supplied facts remain assessable.')
        if n in negative or (facet_kind == 'exception' and n in {'054','069','085'}):
            missing = 'Local prohibition/exception is source-supported without executing the excluded procedure; exact base target needed for graph matching or combined/full outcome.'
        if n in {'042','058','070','073','083','084','085'} and facet_kind in {'definition','condition'}:
            missing = 'Missing map/scenario/parameter blocks applicability or affected concrete resolution. No guessed commander, eligibility, orientation or army parameter.'
        if to:
            missing = 'Internal source present; apply target conditions within local scope. General external procedures remain unresolved where needed.'
        if n == '031':
            missing = 'MRRC row identity unproven. Do not promote hypothesis to table-use gold or compute a shot.'
        if n == '022':
            target_status = 'external_with_boundary_evidence_incomplete'
            missing = '10.13 visible PDF37 right in boundary context, but6.68 allocation and full8.46Step4 not reviewed: full Roman multi-stack hit assignment blocked.'
        edges.append({'id':eid, 'candidate_ids':[c['id']], 'from':c['from'], 'to':to,
            'target_candidate':target, 'kind':facet_kind, 'explicitness':explicitness,
            'explicitness_reason': ('Named in the source without requiring a numeric token; original flags are retained in candidate_audit.' if explicitness=='explicit' else 'Need for exact base procedure/definition/table inferred from stated operation; target identity is not proven.'),
            'executable':executable, 'direction_reason':f"{c['from']} korzysta z/modyfikuje/wskazuje cel; nie odwrotnie. {reason}",
            'evidence':evidence([c['from']]), 'target_status':target_status, 'status':status,
            'criticality':'critical' if executable else 'noncritical',
            'criticality_reason':'Brak zmienia legalność, liczbę, czas, skutek lub uniemożliwia pełny wynik.' if executable else 'Informacyjna wzmianka; liczyć osobno od execution graph.',
            'missing_target_effect':missing, 'human_review_status':'waiting_review', 'owner_confirmed':False})
    audit.append({'candidate_id':c['id'], 'original_from':c['from'], 'original_explicitness':c['explicitness'],
        'disposition':'split_compound_candidate' if len(facets)>1 else ('mention_only' if kind=='mention' else 'manually_classified_proposal'),
        'dependency_ids':dep_ids, 'reason':reason, 'original_bytes_preserved':True})

# A new implicit internal need, absent from the historical candidates: do not hide it.
edges.append({'id':'DEP-NEW-001', 'candidate_ids':[], 'from':'C-9.72-01','to':'R-9.71',
    'kind':'condition','explicitness':'implicit','executable':True,'target_status':'internal',
    'status':'source_supported_proposal', 'direction_reason':'Ocena move+Shock musi nadal spełniać bramkę ruchu9.71; próg9.72 nie uchyla wcześniejszego cannot move. Kierunek9.72→9.71 to potrzeba warunku, nie reguła pierwszeństwa z samej kolejności.',
    'evidence':evidence(['C-9.71-01','C-9.71-02','C-9.71-03','C-9.72-01']),
    'criticality':'critical','criticality_reason':'Sam próg RP mógłby nieuprawnienie odblokować ruch.',
    'missing_target_effect':'Internal source available; inferred conjunction requires owner semantic review; does not establish full Shock legality.',
    'human_review_status':'waiting_review','owner_confirmed':False})

# Explicit record of boundary context. Not new chapter9 expectations or recursive closure.
for e in edges:
    if 'DC-022' in e['candidate_ids']:
        e['boundary_target_evidence'] = {
            'scope':'context_not_chapter9_core', 'pdf_page':37,'printed_page':'37','column':'right',
            'source_sha256':common['source_sha256'], 'render':'source/review-evidence/pdf-37.png',
            'render_sha256':sha(P/'source/review-evidence/pdf-37.png'),
            'bbox_pdf_points':[315,75,567,368], 'bbox_precision':'Approximate containing envelope for10.13, exception bullets and example; top-left PDF points.',
            'observation':'10.13 rozdziela między units/stacks i odsyła przy alokacji wewnątrz stosu do6.68 bullet6; sam widoczny cel nie domyka całej alokacji.',
            'owner_semantic_review':False}

ex_by_id = {e['id']:e for e in expectations}
for exp in expectations:
    refs = set(exp['inventory_refs'])
    for d in edges:
        origin = d.get('from_inventory_ref', d['from'])
        if origin in refs or any(items[r].get('parent_id') == origin for r in refs):
            exp['dependency_ids'].append(d['id'])

def ex_ids(refs):
    return [e['id'] for e in expectations if set(e['inventory_refs']).intersection(refs)]
def dep_ids(refs):
    return [d['id'] for d in edges if d.get('from_inventory_ref', d['from']) in refs]

def situation(n, title, categories, refs, facts, task, expected, rationale, missing=None, blocker=None):
    sid=f'SIT-{n:02d}'
    ids=ex_ids(refs)
    for i in ids:
        ex_by_id[i]['situation_ids'].append(sid)
    return {'id':sid,'title':title,'categories':categories,'inventory_refs':refs,
      'facts':facts,'facts_policy':'Synthetic supplied conditions for a local test; no real scenario/unit parameters accepted. Unstated broader legality is not inferred.',
      'question':task,'expected':{'kind':'justified_block' if blocker else 'local_result',
        'result':expected,'scope':'Only requested local gate/transformation; never a complete combat/movement resolution.',
        'rationale':rationale,'missing_context':missing or [],'blocker':blocker},
      'status':'unresolved_interpretation' if blocker=='source_ambiguity' else ('requires_context' if blocker else 'source_supported_proposal'),
      'criticality':'critical','criticality_reason':'Wrong result/block changes legality, effect, number, exception, timing or ability to resolve.',
      'criticality_author':'Codex proposal; owner justification pending',
      'expectation_ids':ids,'dependency_ids':dep_ids(refs),'evidence':evidence(refs),
      'human_review_status':'waiting_review','owner_confirmed':False}

situations = [
 situation(1,'Pass-Thru: legalna opcja i lokalne liczby',['ordinary','boundary'],
 ['C-9.11-01','C-9.11-07','C-9.11-08','C-9.11-09'],
 {'defender':'jedna LI, Front attack','attacker':'jedna EL SHOCK MUST CHECK TQ bez współatakujących',
 'initial_enemy_ZOC':False,'free_rear':1,'decision_before_PreShock_DR':True,
 'base_Shock_Hits':{'defender':5,'elephant':3},'infantry_routed':False,'elephant_rampaged':False},
 'Czy można wybrać opcję? Podaj lokalny DRM, Hits i końcowe placement, bez obliczania całego Shock.',
 'Opcja spełnia lokalne warunki; Pre-Shock piechoty +1 DRM, Hits5→2 i EL3→2. Po podanych stanach EL do wolnego Rear wybranego przez gracza EL, facing bez zmiany; końcowy test LI jest osobnym krokiem.',
 '5/2 zaokrąglone w dół; krok3 wymaga obu negatywnych stanów. Bazowe Hits są wejściem, nie wynikiem z nieznanej CRT.'),
 situation(2,'Pass-Thru: ZOC na początku phase',['boundary','exception'],
 ['C-9.11-01','C-9.11-04'],
 {'other_PassThru_conditions':True,'in_enemy_ZOC_at_phase_start':True,'in_enemy_ZOC_now':False},
 'Czy wyjście z ZOC w trakcie phase pozwala teraz wybrać Pass-Thru?',
 'Nie. Pass-Thru wykluczony przez ZOC na początku Orders Phase; późniejszy stan nie usuwa zakazu.',
 'Warunek odnosi się do start of Orders Phase, nie chwili decyzji. Nie wyliczać zwykłego Shock bez procedury.'),
 situation(3,'SK po Pass-Thru a Pre-Shock',['exception','conflict'],
 ['C-9.11-07','C-9.11-10','C-9.24-03','C-9.23-03'],
 {'defender':'wyłącznie SK','all_PassThru_conditions':True,'PassThru_elected':True},
 'Czy końcowy Pass-Thru test jest wymagany i czy ten wyjątek usuwa każdy Pre-Shock test?',
 'SK nie robi końcowego Pass-Thru TQ Check. Nie wolno z tego wywieść zwolnienia każdego testu:9.23 zwalnia attackerów atakujących SK alone,9.11 mówi o +1 do Pre-Shock obrońcy.',
 'To dwa testy i różni adresaci. Wyniku Pre-Shock obrońcy bez ogólnej procedury nie obliczono.'),
 situation(4,'Zwykły EL: pierwszy i kolejny7–9',['ordinary','boundary','table'],
 ['TR-03','C-9.14-03'],
 {'unit':'ordinary EL','DR':8,'first_roll_geometry':'kierunek bezpośrednio od przyczyny jest jednoznaczny i wolny','early_termination':False},
 'Porównaj pierwszy8 z kolejnym8 przy podanych warunkach.',
 'Pierwszy8: kierunek od jednostki wywołującej Rampage, próba3 heksów ruchu; sam DR8 nie eliminuje zwykłego EL na pierwszym rzucie. Kolejny8: EL eliminowany.',
 'Wiersz7–9 oddziela first od subsequent. Nie zastosowano orientacji przykładowego kompasu.'),
 situation(5,'Leader Elephant: późniejsze7–9 wobec no rally',['exception','conflict','table'],
 ['TR-03','C-9.14-11'],
 {'unit':'Leader Elephant bez stacked leadera','TQ':6,'roll_number':2,'DR':8},
 'Czy ogólny zakaz rally w Rampage wymusza eliminację?',
 'Nie. Propozycja: szczególny wiersz tabeli natychmiast rally Leader Elephant z4 Hits (6−2), zamiast eliminacji; zakres pierwszego7–9 pozostaje poza tym przypadkiem.',
 'Wyraźne instead i immediately w lokalnej tabeli zawężają ogólny zakaz; owner review zakresu wyjątku nadal konieczny.'),
 situation(6,'Rampage: brak kompasu mapy',['boundary','graphic'],
 ['TR-02','D-01','X-01'],
 {'unit':'EL','DR':1,'battle_map':'unknown','available_diagram':'D-01 example'},
 'Podaj konkretny hexside/kierunek na mapie.',
 'Blokada konkretnego kierunku. Wiadomo, że należy użyć kompasu mapy; D-01 nie zastępuje go.',
 'Caption mówi just an example/use compass for each battle; TR-02 odróżnia vertex/hexside.',
 ['wybrana mapa i jej kompas z dowodem'],'missing_critical_target'),
 situation(7,'Kawaleria bez OW: DR=TQ',['boundary','conflict'],
 ['C-9.16-01'],
 {'elephant':'ordinary, z nieprzyległego do sąsiedniego','cavalry_can_withdraw':False,'cavalry_routed':False,'DR':5,'TQ':5},
 'Czy natychmiastowy test daje0 czy1 Hit?',
 'Blokada liczby Hits przy równości; test jest wymagany. Nie przypisano0 ani1.',
 'If DR is higher i minimum1 wymagają rozstrzygnięcia zakresu. Sam rachunek różnicy nie rozstrzyga normy.',
 ['decyzja właściciela o minimum lub wskazany dodatkowy dowód'],'source_ambiguity'),
 situation(8,'SK: halving i cap1',['ordinary','boundary'],
 ['C-9.23-05'],
 {'context':'SK broni się w legalnie ustalonym Shock','unadjusted_Hits_inflicted_by_SK':[1,3,6],'other_modifiers':False},
 'Podaj tylko transformację Hits zadanych przez SK.',
 'Odpowiednio0,1,1 Hits: floor(1/2)=0, floor(3/2)=1, floor(6/2)=3 ograniczone do1.',
 'Zastosowane round down oraz maximum1; nie obliczono pełnego wyniku CRT.'),
 situation(9,'LC przeciw SK: wyjątek H&D i lokalna połowa',['exception','ordinary'],
 ['C-9.31-01','C-9.22-01','C-9.32-01'],
 {'missile_LC_MA':8,'SK_MA':6,'separate_Shock_test_target':'HI','unadjusted_LC_Hits':5,'superiority_and_other_modifiers':False},
 'Czy niższe MA SK pozwala H&D? W osobnym ataku LC na HI przekształć podane5 Hits.',
 'H&D przeciw SK zabronione mimo niższego MA. W odrębnym podanym Shock LC na HI lokalnie5→2 Hits.',
 'Wyjątek targetSK jest wspólny9.22/9.31;9.32 działa na Hits zadane przez atakującą LC, nie na Hits otrzymane.'),
 situation(10,'Phalanx Defense: moving HI i stationary',['ordinary','boundary'],
 ['C-9.41-01'],
 {'defender':'PH','both_flanks_qualify':True,'attacker':'HI, żaden PH','angle':'Front','variants':['moves adjacent then Shock','starts adjacent and stays']},
 'Podaj tylko shift wynikający z9.41, nie wynik CRT.',
 'Moving HI:1L za każdy flank, razem2L. Started adjacent/stayed:0L z9.41. Dla moving non-HI/non-PH byłoby4L przy tych flankach.',
 'HI replaces2L by1L per flank; moving warunek i wyłączenia zachowane.'),
 situation(11,'DD: niewiadoma eligibility scenariusza',['ordinary','boundary'],
 ['N-09-S2','C-9.51-01','X-06'],
 {'units':'dwie PH','OC_order':True,'rear_start_and_MPs':True,'scenario_eligible_list':'missing'},
 'Czy można ogłosić formowanie DD dla tych rzeczywistych PH?',
 'Blokada eligibility. Podane lokalne warunki9.51 nie zastępują listy scenario-specific.',
 'N-09-S2 wymaga listy; X-06 jest odesłaniem do przykładu, nie dowodem że wszystkie PH eligible.',
 ['konkretny scenario i lista eligible units'],'missing_critical_target'),
 situation(12,'DD: Flank3x i nieparzysty podział',['exception','boundary'],
 ['C-9.53-06','C-9.53-07'],
 {'formation':'DD już legalnie ustalone','attack':'Shock Flank','base_defender_Hits_before_directional_multiplier':3,'other_modifiers':False},
 'Podaj lokalny mnożnik i podział Hits, bez testów Rout.',
 '3×3=9 Hits, top5 i bottom4. Użycie zwykłego2× lub odd Hit bottom byłoby błędne.',
 '3x instead of doubled oraz equally/odd top. Pozostała procedura i Rout są poza lokalnym wynikiem.'),
 situation(13,'Roman stack: order vs facing',['boundary','conflict'],
 ['C-9.64-01','C-9.62-01','C-9.63-01'],
 {'stack':'Roman units różne border colors','top_TQ':7,'bottom_TQ':5,'order':'LC','requested_actions':['switch top/bottom','change facing']},
 'Która akcja spełnia lokalny wymóg order? Jakiego TQ/DRM używa każdy test stosu przed zmianą?',
 'LC nie pozwala switch stacking order; facing może być przez LC. Każda unit własny test zTQ7 top i+1DRM za różne colors. Nie ustalono alokacji Shock Hits.',
 'IO only dla switch; all checks +1, każdy uses top TQ. Pełne warunki LC nadal muszą być znane.'),
 situation(14,'MLE: wymagania heksu i orientacja',['ordinary','boundary','graphic'],
 ['C-9.66-01-S1','C-9.66-01-S2','C-9.66-01-S3','C-9.66-01-S4','C-9.66-01-S5','C-9.66-01-S6','D-02','C-9.68-01'],
 {'line':'Roman stacks same Line established','order':'eligible LC','column':False,'destination_variants':['vacant Clear outside enemy ZOC','occupied Clear','vacant non-Clear','vacant Clear in enemy ZOC']},
 'Porównaj lokalne warunki MLE i facing; czy można złożyć stos odwracając diagram?',
 'Tylko pierwszy destination spełnia lokalne warunki; top sideways, facing zachowany, po LC obie units mogą move zMA−2, brak Hits za MLE. Pozostałe trzy destinations zabronione. Odwrócenie diagramu nie daje prawa stacking together.',
 'Wszystkie warunki heksu są koniunkcją; Only unstacking. Tekst9.68 określa LC post-move.'),
 situation(15,'MLE i OW na jednym triggerze',['exception','conflict','time'],
 ['C-9.67-01','X-07'],
 {'enemy_move':'combat unit wchodzi w2 heksy','both_triggers_established':True,'MLE_and_OW_same_units':True},
 'Czy te same units mogą wykonać obie reakcje? Czy zaniechanie pierwszej okazji kasuje następne?',
 'Te same units nie mogą wykonać obu. Różne units mogą przy spełnionych warunkach; odmowa wcześniejszej okazji nie kasuje późniejszych MLE triggers.',
 'Both together but not same units; source says may choose whenever enemy places itself. X-07 obrazuje różne units.'),
 situation(16,'Triarii: próg zaokrąglony i wyjątek bez ruchu',['boundary','exception','conflict'],
 ['C-9.7-01-S1','C-9.71-01','C-9.71-02','C-9.71-03','C-9.72-01'],
 {'doctrine_applicable':'synthetic:Romans218BCE, Scipio nie OC','AWL':11,'RP_variants':[4,5],'movement_gate_9_71':True,'enemy_in_ZOC':True},
 'Oceń tylko RP gate move+Shock oraz standing Shock; czy RP sam uchyla9.71?',
 'Próg floor(11/2)=5:RP4 nie spełnia move+Shock gate,RP5 spełnia przy podanej bramce9.71. Standing Shock na enemy wZOC możliwy w zakresie9.72 przy obu RP. SamRP5 nie uchyla9.71.',
 'At least half round down, without moving exception. Propozycja łącznego czytania bramek ma osobną niejawna relację do review.'),
 situation(17,'Scorpio: mode lock i dwa różne limity ognia',['ordinary','boundary','conflict','time'],
 ['C-9.82-01','C-9.85-01','C-9.86-01','G-04','G-05'],
 {'variants':[{'mode_switch':'Move→Fire wtej phase','active_shots_this_turn':0},
 {'mode':'Fire bez switch','active_shots_this_turn':1,'active_shots_this_phase':0},
 {'mode':'Fire bez switch','active_shots_this_turn':2},
 {'mode':'Fire','enemy_phase':'nowa','reaction_shots_this_phase':1}],
 'other_shot_conditions':'supplied legal range/LOS/target; target nie Rampaging EL'},
 'Oceń lokalne prawo do następnego strzału i recovery po nim.',
 'Po switch doFire brak strzału wtej phase mimo no orders. W drugiej wersji jeden active shot dostępny, marker Finished i brak recovery wphase. Przy2 active wturn brak następnego active. Nowa enemy phase ma odrębny cap2reaction, po1 dostępny jeszcze1, bez ordinary RF8.2.',
 '9.82 mode lock zachowany; active per Game Turn/per friendly phase≠reaction per enemy phase. Realny hit lookup nie wykonany.'),
 situation(18,'Ferocity: brak przypisania leadera',['ordinary','conflict'],
 ['C-9.94-03','C-9.95-02'],
 {'event':'jedna BI Routs','nearby_leaders':['A','B'],'Initiative':[5,7],'DR':6,'scenario_command_mapping':'missing'},
 'Czy Ferocity utracona i które BI nią objąć?',
 'Blokada wyboru leader Initiative i zakresu utraty. Wiadomo, że należy wykonać Ferocity check poRout, ale nie wybierać najbliższego ani korzystniejszego leadera.',
 '9.94 identyfikuje leadera przez scenario setup. ZDR6 przy5 byłaby utrata, przy7 zachowanie, więc brak jest krytyczny.',
 ['setup commander mapping i członkostwo BI command'],'missing_critical_target'),
 situation(19,'Impetuosity: koniec turn, nie natychmiast',['boundary','time'],
 ['C-9.95-02'],
 {'command_mapping':'synthetic A=[BI1,BI2,BI3], B=[BI4]','event':'druga BI zA wchodzi enemy ZOC wGame Turn2','base_MA':5,'Momentum_roll_kind':'first-try'},
 'Kiedy wygasa bonus i jaki zakres obejmuje?',
 'DlaA przez resztęGame Turn2 nadal MA6 i−1DRM first-try Momentum leadera; po końcu turn Impetuosity A wygasa. Nie traci jej automatycznie B, jeśli własny trigger nie zaszedł.',
 'At least two of a leader command i rest of Game Turn/after which; command mapping wyłącznie zadane syntetycznie, nie dowód realnego setup.'),
 situation(20,'CH+LI: dismount na granicy MA i mounted zakazy',['boundary','exception'],
 ['C-9.96-03','C-9.96-05','C-9.96-06','C-9.96-07'],
 {'eligibility':'supplied eligible LI','LI_printed_MA':5,'CH_MA':8,'distance_in_MPs_before_dismount_variants':[4,5],
 'LI_MPs_before_mount':3,'Missile_LOW_NO_marker_before_mount':True,'other_costs':False},
 'Podaj lokalny budżet po dismount/mount; czy wolno mounted Shock i czy partial-phase mount daje repeat-movement wyjątek?',
 'Dismount po4MP daje1MP, po5 brak dalszego ruchu; mount po3MP LI daje do5MP mounted CH (8−3). Mount/dismount koszt0MP/0Hits, marker LOW/NO usuwa się przy mount. Mounted LI nie Shock attack; partial-phase mount nie spełnia entire-phase zwolnienia repeat-movement Hits.',
 'Strict less-than i difference zachowane; nie wyliczono terrain/trasy ani supply po późniejszym dismount.'),
]
assert len(situations)==20

# Stable sets and separate denominators: source support is not human confirmation.
def counts(rows):
    return {'total':len(rows),'by_status':dict(Counter(r['status'] for r in rows)),
            'owner_confirmed':sum(r['owner_confirmed'] for r in rows),
            'owner_unconfirmed':sum(not r['owner_confirmed'] for r in rows),
            'by_criticality':dict(Counter(r['criticality'] for r in rows))}
def sets(rows):
    return {s:[r['id'] for r in rows if r['status']==s] for s in common['status_policy'] if s!='owner_confirmed'} | {'owner_confirmed':[]}

expectation_doc = common | {'artifact':'M-POC1B-expectations','unit_policy':'Manually defined local assessment propositions; not98 norms or a verified atomic denominator. Numbers in statement and dimension tags belong to this review only.',
 'counts':counts(expectations),'sets':sets(expectations),'expectations':expectations,
 'coverage':{'numbered_rule_labels_total':41,'numbered_rule_labels_with_evidence':None,
             'unreviewed_atomic_coverage':'unknown','graphic_glyph_coverage':'not exhaustive'},
 'non_normative_policy':'N-01/N-02/N-04/N-05/N-06/N-08/N-10/N-12/N-13 and explanatory spans not promoted to independent obligations. Historical head-to-head observations do not create modifiers.',
}
covered=set()
for e in expectations:
    for ref in e['inventory_refs']:
        item=items[ref]
        associated=item.get('associated_rule_or_section',item.get('associated_rule'))
        parent=item.get('parent_id')
        if associated and associated.startswith('R-'): covered.add(associated)
        if parent and parent.startswith('R-'): covered.add(parent)
        if ref.startswith('R-'): covered.add(ref)
expectation_doc['coverage']['numbered_rule_labels_with_evidence']=len(covered)
assert len(covered)==41, covered

dependency_doc = common | {'artifact':'M-POC1B-dependencies',
 'direction_convention':'from = user/modifier/mention source; to = used/mutated target. Physical continuations start fragment→later fragment. Never reverse because target supplies the fact.',
 'counts':counts(edges), 'sets':sets(edges),
 'denominators':{'historical_candidate_occurrences':96,'candidate_occurrences_dispositioned':len(audit),
 'historical_distinct_external_numeric_tokens':19,'verified_gold_edges':0,
 'execution_proposals_by_explicitness':dict(Counter(e['explicitness'] for e in edges if e['executable'])),
 'mentions_by_explicitness':dict(Counter(e['explicitness'] for e in edges if e['kind']=='mention')),
 'physical_continuations':sum(e['kind']=='continuation' for e in edges),
 'all_proposals_by_explicitness':dict(Counter(e['explicitness'] for e in edges)),
 'source_supported_execution_by_explicitness':dict(Counter(e['explicitness'] for e in edges if e['executable'] and e['status']=='source_supported_proposal')),
 'owner_confirmed_execution_by_explicitness':{'explicit':0,'implicit':0},
 'precision_recall':'n/a; no frozen owner-reviewed gold, no extraction response'},
 'candidate_audit':audit,'dependencies':edges,
 'duplicate_policy':'One historical occurrence is not automatically one unique edge. Compound targets split into facets; aliases/repeated references need owner identity review. No TP/FN denominator before freeze; same semantic tuple duplicates will not increase TP.',
 'alias_policy':'MRRC is named, full-title alias and row identity remain unverified without target;10.13 boundary evidence does not recursively prove6.68.',
 'new_relation_policy':'DEP-NEW-001 separately marked implicit internal proposal, no silent expansion of historical96.',
}
situation_doc = common | {'artifact':'M-POC1B-situations','counts':counts(situations),'sets':sets(situations),
 'expected_kind_counts':dict(Counter(s['expected']['kind'] for s in situations)),
 'categories':dict(Counter(c for s in situations for c in s['categories'])),
 'situation_denominator':20,'outcome_measurement':'n/a before owner review and extraction;16 proposed local results and4 justified blocks are not16 successful extraction outcomes.',
 'situations':situations,
 'context_policy':'No missing parameter inferred. Supplied numbers/types/gates are synthetic input facts and not scenario acceptance. A local_result proves only the requested calculation or gate, never full attack/route legality.',
 'threshold_warning':'The16/20 local-result proposal composition equals80%, but local tests are deliberately limited in scope. Owner must assess utility of this scope before freeze; not a predeclared pass of POC quality.',
}

for name, doc in [('expectations.json',expectation_doc),('dependencies.json',dependency_doc),('situations.json',situation_doc)]:
    write(P/'evaluation/draft'/name,doc)

write(SESSION/'assembly-summary.json', {'date':datetime.now(timezone.utc).isoformat(),
 'expectations':expectation_doc['counts'],'dependencies':dependency_doc['denominators'],
 'situations':situation_doc['expected_kind_counts'],
 'original_manifests_verified':True,'source_hash_verified':True,
 'formatter_policy':'Static manual proposals plus evidence attachment only; no inference calls, legacy code/schema, runtime or engine.'})
print(json.dumps(read(SESSION/'assembly-summary.json'),ensure_ascii=False))
