---
name: aew-setup-project
description: "Przygotuj adaptację standardu dev-flow do nowego lub istniejącego projektu; użyj przy wdrażaniu standardu lub przeglądzie jego lokalnej konfiguracji."
---

# Adaptacja standardu do projektu

Przygotuj spójny sposób zastosowania standardu w docelowym repozytorium.
Sama prośba o analizę adaptacji oznacza pracę bez edycji.

## Wykonanie

1. Ustal docelowe repozytorium, obowiązujące instrukcje, branch i zmiany
   użytkownika. Nie zmieniaj repozytorium źródłowego zamiast docelowego.
2. Rozpoznaj istniejące zasady, źródła wymagań, komendy weryfikacji,
   wymagane usługi i sposób dostarczania zmian. Czytaj tylko potrzebne materiały.
3. Wskaż wersję źródłową standardu jako pełny SHA, dostępne skille i lokalne
   odstępstwa. Nie deklaruj, że zainstalowano plugin po samym odczycie plików.
4. Przygotuj propozycję profilu: cel, źródła decyzji, środowisko, build/test/UI,
   dane i migracje, Git/PR/review, merge, publikacja oraz właściciele zgód.
   Rozpoznaj istniejące progi jakości i wyjątki z ich uzasadnieniem;
   nie ustanawiaj uniwersalnych progów pokrycia lub wydajności.
   Braki oznacz jako otwarte; nie wymyślaj komend ani uprawnień.
5. Jeśli adaptacja jest zlecona, wykonaj najmniejszą zmianę zachowującą
   istniejące instrukcje i pracę użytkownika. Nie zastępuj całego AGENTS.md.
   Nie instaluj globalnie narzędzi, nie zmieniaj ustawień GitHub ani innych
   projektów, jeśli nie obejmuje ich polecenie.
6. Sprawdź spójność instrukcji i dostępność wskazanych plików. Rozróżnij
   napisanie procedury, jej wykrycie przez hosta i wykonany pilotaż.

## Wynik

Profil albo propozycja adaptacji, wybrane materiały, źródłowy SHA,
odstępstwa, wykonane kontrole i pozostałe decyzje.
Jawne polecenie użytkownika ma pierwszeństwo przed wskazówkami skilla
w granicach zasad środowiska. Zachowaj wcześniej udzielone zgody.
