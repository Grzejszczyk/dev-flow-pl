# Ewaluacja skilli

Status: katalog przypadków do wykonania, bez zadeklarowanych wyników.
Przebiegi z agentem uruchamia się na żądanie. Automatyczny runner pozostaje
następnym etapem po pilotażu; CI sprawdza wyłącznie strukturę danych.

## Kontrakt

Plik cases/aew-*.json zawiera skill, triggers i cases. triggers.positive to
realistyczne polecenia wymagające skilla, negative to sąsiednie polecenia,
które nie powinny go uruchomić. Sam katalog nie mierzy trafności wyboru.

Przypadek ma globalnie unikalne id, prompt, fixture (katalog względem fixtures/),
setup (stan początkowy), expected (obserwowalne rezultaty), forbidden
(niedozwolone skutki) i evidence (wymagane dowody). Walidator sprawdza te pola,
istnienie skilla i bezpieczne ścieżki; nie ocenia znaczenia oczekiwań.

Polecenie kontroli: python scripts/validate_evals.py.
Testy kontraktu są częścią python -m unittest discover -s tests -v.

## Przebieg na żądanie

1. Wybierz przypadek i skopiuj jego fixture do jednorazowego repozytorium,
   poza źródłowym checkoutem i katalogiem zainstalowanych skilli. Ustaw main
   i zapisz bazowy commit; tożsamość Git stosuj per commit.
2. Wykonaj setup i zapisz początkowy SHA, status i diff. Nie przenoś plików
   z produkcji ani sekretów. Fixture nie zawiera prawdziwego remote.
3. Zapisz pełny SHA źródeł skilla, model, host i jego wersję, system,
   dostępne narzędzia, ograniczenia oraz sposób udostępnienia skilla.
   Dla niecommitowanych instrukcji zachowaj dokładny diff i sumy plików.
4. Dla zachowania udostępnij agentowi badany SKILL.md oraz prompt przypadku.
   Oceniającemu pozostaw expected, forbidden i evidence, aby nie podpowiadać
   agentowi werdyktu. Nie dopisuj nowych uprawnień do promptu.
5. Zapisz ślad odczytów, poleceń, wyników, mutacji i odpowiedzi. Porównaj stan
   końcowy z bazą; brak śladu nie dowodzi braku działania.
6. Oceń każde oczekiwanie osobno: zaliczone, niezaliczone albo niewykonane,
   z dowodem i ograniczeniem. Naruszenie forbidden oznacza niezaliczenie;
   brak wymaganych dowodów nie może zostać oznaczony jako sukces.
7. Do porównania przed/po użyj tego samego przypadku, bazowego stanu,
   modelu i zestawu narzędzi w osobnych sesjach. Zapisz odstępstwa.
   Przebieg w kontekście autora nie jest niezależnym eksperymentem.

Surowe ślady i wyniki przechowuj lokalnie w .local/evals/ (katalog ignorowany).
Do repozytorium mogą trafić jedynie sprawdzone podsumowania syntetycznych prób,
z dowodami dostępnymi oceniającemu i jawnymi ograniczeniami.

## Dobór skilla a przestrzeganie procedury

Jawne podanie SKILL.md sprawdza zachowanie po jego wczytaniu.
Osobno sprawdzaj positive/negative w świeżej sesji z badanym katalogiem:
nie wskazuj nazwy skilla i zanotuj rzeczywisty wybór oraz rezultat.
Jeśli katalog nie jest dostępny, oznacz kontrolę doboru jako niewykonaną.
Nie instaluj pluginu ani dodatkowych narzędzi wyłącznie na podstawie tego opisu.

## Raport

Użyj [szablonu](../templates/evaluation-report.md). Osobno podaj statyczny
przegląd, wykonany przebieg i dobór skilla. Naruszenia zakresu lub zgód wymagają
naprawy i ponowienia właściwego przypadku przed rekomendacją szerszego użycia.
