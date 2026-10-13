# ADR-0040 Archiwum POC i nowy kierunek IG

- **Data:** 2026-10-11.
- **Status:** przyjęta decyzja kierunkowa na podstawie polecenia właściciela.

Właściciel polecił zarchiwizować cały obecny POC i oprzeć aktywny projekt
na planie IG jako zalążku narzędzia do digitalizacji gier. Zlecił też
przegląd źródeł internetowych dla SPQR, OSG i GCACW.

## Decyzja

1. Zachować POC w oryginalnych bajtach, z mapą ścieżek, manifestem
   SHA-256 i weryfikacją. Dane publiczne i prywatne pozostają rozdzielone.
2. Przyjąć [plan IG](../IG-PLAN.md) jako aktywny kierunek. Pierwszym
   etapem jest recenzja draftu przed wyborem kontraktu i implementacją.
3. Zaproponować wspólny rdzeń z osobnymi profilami systemów,
   wersji, trybów, scenariuszy i materiałów. Zgodność wymaga prób.
4. Zachować dowody, luki i decyzje człowieka. Reguły instrukcji
   i stan sytuacji partii są odrębnymi warstwami.

## Zakres zastępowania

[ADR-0039](../../archive/poc-2026-10-11/project/docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md)
jest historią POC. Kolejka M-POC i czekanie na POC7 przed propozycją
architektury nie prowadzą już aktywnego projektu, zgodnie z nowym
poleceniem. Ich historyczne wyniki, limity i oczekiwania nie zmieniły się.

Decyzja nie nadaje sukcesu POC ani semantycznej akceptacji ig-draft-0.2.
Nie wybiera bazy danych, kompletnego języka wykonawczego, modelu
inferencji ani integracji starego runtime'u.

[Archiwum](../../archive/poc-2026-10-11/README.md) rozlicza 3117 plików
bez niezgodności hashy. Stan roboczy zachowano, nie cofnięto go.
Oryginalne .git, środowisko i wcześniejsze archiwa pozostały na miejscu.
