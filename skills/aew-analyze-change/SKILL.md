---
name: aew-analyze-change
description: "Przeanalizuj planowaną zmianę oprogramowania przed implementacją: zakres, przykłady zachowania, kryteria akceptacji, wpływ na dane i istotne decyzje."
---

# Analiza zmiany

Przedstaw analizę pozwalającą właścicielowi podjąć decyzję o realizacji.
Skill analityczny sam nie udziela zgody na edycję.

## Wykonanie

1. Ustal problem, docelowe repozytorium, lokalne instrukcje i aktualny stan.
   Przeczytaj źródła wymagań i kod odpowiedni do zmiany.
2. Opisz cel, granice oraz przykład obecnego i oczekiwanego zachowania.
   Nie dodawaj wymagań niepopartych zadaniem.
3. Zdefiniuj obserwowalne kryteria akceptacji i istotny scenariusz błędu.
4. Oceń kontrakty, zgodność, dane, migracje, uprawnienia i wdrożenie
   w zakresie rzeczywistego wpływu. Wskaż dowód dla stwierdzenia o braku migracji
   albo oznacz je jako niewiadomą.
5. Oddziel przyjęte decyzje, propozycje, założenia i pytania blokujące.
   Rozstrzygniętych decyzji nie otwieraj bez nowej przesłanki.
6. Zaproponuj proporcjonalny zakres implementacji, dokumentacji i kontroli.
   Dla większej zmiany wyodrębnij działające, sprawdzalne fragmenty i wskaż
   ryzykowne założenie do wczesnego sprawdzenia. Nie narzucaj limitu linii
   ani commitu po każdym kroku. Drobna poprawka nie wymaga osobnego planu i ADR.
7. Gdy istotne rozwiązanie zależy od wersji biblioteki lub usługi, ustal ją
   w konfiguracji, lockfile lub CI i zweryfikuj niepewne API w oficjalnym źródle
   właściwym dla tej wersji. Zapisz źródło i zakres potwierdzenia; niedostępne
   źródło oznacz jako ograniczenie, zamiast deklarować weryfikację.
8. Przy poleceniu „tylko analiza” nie edytuj plików, nie twórz branchy,
   commitów ani PR. Jeśli w zadaniu już jednoznacznie zlecono realizację,
   nie żądaj ponownej zgody wyłącznie dlatego, że wykonano analizę.

## Wynik

Krótka analiza z kryteriami akceptacji, wpływem na dane, uzasadnionym kierunkiem
i pytaniami wymagającymi właściciela. Wskaż źródła oraz granice rozpoznania.
Jawne polecenie użytkownika ma pierwszeństwo przed wskazówkami skilla
w granicach zasad środowiska.
