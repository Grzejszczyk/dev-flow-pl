# Weryfikacja i dowody

Dobieraj kontrole do ryzyka i kryteriów akceptacji.
[Raport](../templates/verification-report.md) może być sekcją PR;
osobny plik jest potrzebny, gdy ma trwałą wartość.

## Rodzaje dowodów

| Kontrola | Co potwierdza | Czego sama nie potwierdza |
| --- | --- | --- |
| Przegląd diffu | Zakres, kontrakty i zauważone problemy w kodzie. | Wykonania kodu. |
| Build / lint / typy | Wynik konkretnych kontroli statycznych i kompilacji. | Poprawności reguł biznesowych i UI. |
| Testy automatyczne | Obserwowane zachowanie w uruchomionych scenariuszach. | Scenariuszy niewykonanych lub pominiętych. |
| Kontrola bazy i migracji | Zastosowanie schematu, ograniczenia i trwałość w danym środowisku. | Działania produkcji, jeśli sprawdzano bazę jednorazową. |
| Odbiór UI | Obserwowane scenariusze na podanej wersji, urządzeniu i danych. | Wszystkich rozdzielczości i trwałości danych bez jej sprawdzenia. |
| CI | Wynik workflow dla wskazanego commitu. | Poprawnego wdrożenia ani znaczenia pominiętych testów. |
| Sprawdzenie po publikacji | Aktywną wersję i wykonane scenariusze w danym środowisku. | Braku wszystkich regresji. |

Dla każdej istotnej kontroli podaj: wersję kodu, środowisko, polecenie/scenariusz,
wynik i ograniczenie. Rozróżniaj „zaliczone”, „nieudane”, „pominięte”,
„niewykonane” i „nie dotyczy” wraz z uzasadnieniem.

## Praktyka

- Zmiana zachowania wymaga właściwego scenariusza regresji. Dla odtwarzalnego
  błędu potwierdź niepowodzenie na wersji z błędem i powodzenie po poprawce.
  Awaria środowiska nie jest dowodem reprodukcji; brak wykonania ujawnij.
- Nie uzyskuj zielonego wyniku przez osłabienie kontroli. Usunięcie asercji,
  pominięcie testu, wyłączenie reguły lub obniżenie progu wymaga uzasadnienia
  względem kontraktu i oceny w review, a nie automatycznego zakazu.
- Wybieraj testy sprawdzające rezultat, kontrakt lub skutek uboczny.
  Nie dodawaj testów odtwarzających wyłącznie strukturę implementacji.
- Zmiana danych lub migracji: sprawdź właściwe ograniczenia i zachowanie
  na danych syntetycznych w izolowanym środowisku, jeśli jest dostępne.
- Zmiana zapisu: sprawdź trwałość i właściwy scenariusz błędu, jeśli są
  częścią ryzyka. Wyświetlony komunikat sukcesu nie jest sam dowodem zapisu.
- Zmiana UI: potwierdź, że uruchomiona aplikacja zawiera aktualny kod.
- Stabilizuj testy przez oczekiwanie na warunek; nie maskuj wyścigów stałym snem.
- Po poprawkach uruchom kontrole dotknięte zmianą. Powtarzaj pełny zestaw,
  jeśli zmiana, błąd lub niepewność uzasadniają taki koszt.
- Nie używaj produkcji jako środowiska testowego bez odpowiedniej zgody.

## Wdrożenie i odzyskiwanie działania

Przed publikacją zidentyfikuj wersję, środowisko, migracje oraz wymagane zgody.
Określ sposób weryfikacji i działania przy awarii. Po migracji danych cofnięcie
samej aplikacji może być niewystarczające; plan może wymagać naprawy do przodu,
odtworzenia danych lub wznowienia przerwanego etapu.

Przed ponowieniem częściowo udanej operacji ustal, co faktycznie wykonano.
Sukces wcześniejszego kroku nie znika po błędzie kolejnego. Nie ponawiaj
migracji lub publikacji bez sprawdzenia stanu i zasad konkretnego projektu.

## Kontrole tego repozytorium

`python scripts/validate.py` sprawdza pliki tekstowe, ograniczony format
frontmatter skilli, ich metadane UI oraz lokalne linki Markdown do plików.
Dla materiałów wewnątrz skilla lokalne odwołania muszą pozostawać w jego
folderze; sprawdzane są też zasoby pomocnicze i dowiązania. To kontrola linków
i ścieżek, nie dowód samodzielności dowolnych instrukcji zapisanych prozą.
Nie odpytuje adresów zewnętrznych, nie sprawdza anchorów ani zgodności z pełnym
schematem YAML/Codex. Przykłady w blokach kodu pomija przy sprawdzaniu linków.
Nazwy i opisy frontmatter są celowo ograniczone do formatu opisanego w AGENTS.md.

`python -m unittest discover -s tests -v` sprawdza, czy walidator wykrywa
rzeczywiste uszkodzenia i odrzuca ścieżki wychodzące poza repozytorium.
Walidator sprawdza także manifest i lokalny katalog marketplace: spójność nazw,
wersję, wymagane metadane, bezpieczną ścieżkę pakietu i zakres bez MCP/hooków.
To kontrola kontraktów tego repozytorium, a nie pełna walidacja schematu pluginów.
Testy obejmują także uszkodzony JSON, błędne powiązanie pakietu i wyjście poza katalog.
CI wykonuje te same kontrole i `git diff --check`.
Dodatkowo `python scripts/validate_evals.py` sprawdza kontrakt katalogu
[ewaluacji](../evals/README.md), identyfikatory, pokrycie skilli pakietami
oraz ścieżki danych. Nie uruchamia agenta i nie ocenia rezultatów.

Kontrole struktury i statyczny przegląd scenariuszy nie zastępują pilotażu
z agentem. Sposób oceny zachowania opisuje [pilot](pilot.md).
