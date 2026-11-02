# Przebieg pracy

Status: propozycja standardu v0.2 do pilotażu. Zasady uprawnień opisuje
[authorization](authorization.md), a wymagane dowody [verification](verification.md).

## Dobór zakresu

- Mała zmiana: krótki opis oczekiwanego zachowania, właściwa kontrola i PR.
- Funkcja: kryteria akceptacji, analiza wpływu, implementacja, testy i review.
- Zmiana podwyższonego ryzyka: dodatkowo kontrakty, dane/migracje,
  uprawnienia, awarie i sposób odzyskania działania.

Ryzyko wynika z wpływu, nie z liczby linii. Mała zmiana może wpływać na płatności,
autoryzację lub dane. Nie twórz obowiązkowych dokumentów dla każdego etapu.
Większe zmiany dziel na działające, sprawdzalne fragmenty; ryzykowne założenie
sprawdź wcześnie. Nie wiąż tego z uniwersalnym limitem linii ani obowiązkiem
commitu po każdym kroku. Istotne, niepewne użycie API weryfikuj w oficjalnym
źródle właściwym dla wersji zależności ustalonej w projekcie. Brak potwierdzenia
jest ograniczeniem, nie wynikiem pozytywnym.

## Etapy i warunki przejścia

| Etap | Wynik umożliwiający przejście dalej |
| --- | --- |
| Cel i zakres | Problem, oczekiwany rezultat, granice i obserwowalne kryteria akceptacji. |
| Analiza i porozumienie | Istotne decyzje rozstrzygnięte; znane zależności, wpływ na dane i migracje. Implementacja objęta zgodą. |
| Utrwalenie decyzji | Przyjęte ustalenia zapisane w odpowiednim miejscu; ADR tylko dla trwałej decyzji. |
| Implementacja | Spójny zakres kodu, testów i aktualnej dokumentacji, bez zmian przypadkowych. |
| Weryfikacja i self-review | Proporcjonalne kontrole wykonane; wynik i braki odniesione do kryteriów akceptacji. |
| PR i review | Konkretna wersja zmiany sprawdzona; uwagi poprawione albo jawnie rozstrzygnięte. |
| Merge | Zgoda właściciela na aktualną zmianę, wymagane kontrole i squash zgodnie z profilem. |
| Publikacja | Osobno autoryzowana wersja, środowisko, migracje i sposób odzyskania działania. |
| Sprawdzenie działania | Potwierdzona aktywna wersja i scenariusze wymagane dla tego wdrożenia. |

Wykonanie to pętla: review może skierować do implementacji, a odkryty problem
wymagań do analizy. Dokumentacja opisuje końcową decyzję i zachowanie.
Nie otwieraj ponownie rozstrzygniętej decyzji bez nowej istotnej przesłanki.

## Zrozumienie przed implementacją

Dla istotnej zmiany przedstaw przykład „przed / po”, kryteria akceptacji,
wpływ na dane i niewiadome blokujące pracę. Do analizy użyj istniejącego issue,
rozmowy lub [szablonu](../templates/change-analysis.md), według potrzeby.

Nie wymagaj osobnej odpowiedzi „rozumiemy się”, jeśli polecenie i wcześniejsze
ustalenia już jednoznacznie określają rezultat oraz zgodę na wykonanie.
Nowy zakres, sprzeczne wymagania albo istotny wybór produktowy wracają do właściciela.

## Dokumentowanie

- Decyzja przyjęta: źródło, status i konsekwencje, np. [ADR](../templates/adr.md).
- Propozycja: oznaczenie propozycji i pytanie do rozstrzygnięcia.
- Odkrycie: obserwacja wraz z dowodem i datą, gdy ma to znaczenie.
- Instrukcja operacyjna: sposób wykonania i weryfikacji konkretnej czynności.

Nie zapisuj wszystkich rozważań w ADR-ach. Nie utrzymuj tych samych reguł
biznesowych w README, skillu i kilku planach. Wybierz właściciela informacji.

## Wznowienie i przekazanie pracy

Przy przerwaniu lub przekazaniu utrwal tylko stan potrzebny do kontynuacji:
zakres i źródła decyzji/zgód, branch/PR, SHA oraz zmiany robocze, wyniki kontroli
z wersją, otwarte sprawy i następny krok. Użyj istniejącego zadania lub
[krótkiej notatki](../templates/handoff.md); nie wymagaj jej po każdej czynności.
Przy wznowieniu sprawdź rzeczywisty stan i aktualność dowodów. Wcześniejsze
zgody obowiązują w swoim zakresie; istotną niejasność wyjaśnij dla zależnej czynności.

## Review i poprawki

Self-review autora jest obowiązkową częścią przygotowania zmiany.
Dodatkowe AI review wykonuj, gdy wymaga tego profil lub uzasadnia je ryzyko.
W miarę możliwości użyj osobnego kontekstu z wymaganiami i diffem, bez sugerowania
oczekiwanego werdyktu. Delegowanie musi być dozwolone w danym środowisku.

Review podaje bazowy i końcowy SHA, zakres oraz ograniczenia. Nowy commit
zmieniający zachowanie wymaga przeglądu zmienionej części i właściwych kontroli.
Uwagi ocenia się według dowodów; nie należy automatycznie wdrażać wszystkich
propozycji AI. Review bezpieczeństwa jest odrębną kontrolą, gdy zakres jej wymaga.

## CI i zakończenie

Domyślnie nowy projekt uruchamia automatyczne sprawdzenia na PR przed merge.
Profil może opisać inny uzgodniony wariant i jego konsekwencje.
Zielony check z wcześniejszej wersji nie jest dowodem dla nowej zmiany.

Instrukcja „wymagaj CI” nie konfiguruje ochrony brancha. Sprawdź oddzielnie,
czy wymagania są egzekwowane w ustawieniach repozytorium.

Rozróżniaj zakończenie implementacji, gotowość PR, merge i sprawdzone wdrożenie.
Zadanie implementacyjne może zakończyć się gotowym PR bez publikacji.
Na końcu podaj rezultat, wykonane kontrole, ograniczenia i decyzję oczekiwaną
od właściciela.
