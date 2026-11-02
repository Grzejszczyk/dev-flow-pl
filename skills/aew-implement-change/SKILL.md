---
name: aew-implement-change
description: "Zrealizuj uzgodnioną zmianę kodu lub dokumentacji wraz z proporcjonalnymi testami i self-review; użyj przy zleceniu implementacji lub konkretnej poprawki."
---

# Implementacja uzgodnionej zmiany

Doprowadź autoryzowany zakres do sprawdzalnego rezultatu.

## Wykonanie

1. Odczytaj lokalne instrukcje, kryteria akceptacji i zakres zgody. Sprawdź
   branch i stan plików; zachowaj niepowiązane zmiany.
2. Przygotuj branch zgodny z regułami projektu. Dla nowej pracy użyj aktualnej
   bazy; kontynuując istniejący PR, sprawdź jego branch zamiast zakładać nowy.
3. Dla większej zmiany wykonuj działające, sprawdzalne fragmenty; najpierw
   sprawdź istotne ryzykowne założenie. Kontroluj dotknięte obszary po zmianie,
   bez sztywnego limitu linii i obowiązkowego commitu po każdym kroku.
   Przy niepewnym użyciu API ustal wersję w źródłach projektu i sprawdź
   właściwą oficjalną dokumentację. Oznacz brak dostępu lub potwierdzenia;
   nie wymagaj wyszukiwania dla prostych operacji niezależnych od wersji.
   Wykonaj najmniejszą spójną zmianę kodu, właściwych testów i dokumentacji.
   Utrzymuj jedno źródło każdej decyzji. ADR dodaj dla istotnego trwałego wyboru.
4. Nowy istotny konflikt wymagań lub rozszerzenie zakresu przekaż właścicielowi.
   Kontynuuj niezależną pracę. Nie pytaj ponownie o rutynowe czynności już
   objęte zgodą.
5. Dla odtwarzalnego błędu zachowania najpierw uruchom scenariusz regresji
   na wersji z błędem, potem zastosuj poprawkę i potwierdź powodzenie.
   Użyj właściwych komend projektu. Sprawdź, czy niepowodzenie wynika z błędu
   produktu, a nie brakującego narzędzia lub usługi. Nie cofaj obcych zmian,
   aby uzyskać dowód; w razie potrzeby użyj izolowanego środowiska.
   Jeśli reprodukcja jest niedostępna, opisz dowody, hipotezę i ograniczenie;
   nie deklaruj wykonania testu przed poprawką.
6. Uruchom kontrole odpowiednie do wpływu i dostępnego środowiska.
   Odróżniaj build, testy, bazę/migracje i odbiór UI. Potwierdź aktualność
   uruchomionej wersji i trwałość zapisu, gdy dotyczą kryteriów.
7. Wykonaj self-review diffu względem bazy. Sprawdź regresje, przypadkowe pliki,
   sekrety, dokumentację i niewykonane kontrole. Oceń również usunięte asercje,
   pominięte testy, wyłączone reguły i obniżone progi. Nie osłabiaj kontroli
   wyłącznie dla zielonego wyniku; uzasadnioną zmianę testu lub konfiguracji
   opisz wraz z dowodem zachowania wymaganego kontraktu.
8. Przy rzeczywistym przerwaniu lub przekazaniu pracy zapisz w istniejącym
   zadaniu lub krótkiej notatce zakres, źródła decyzji i zgód, branch/PR,
   stan zmian, dowody kontroli z wersją oraz następny krok i otwarte sprawy.
   Przy wznowieniu sprawdź aktualność tych danych; nie unieważniaj wcześniejszej
   zgody ani nie uznawaj starych wyników za dowód dla nowego kodu.
9. Commit, push i PR wykonaj, jeśli obejmuje je zadanie lub stała reguła
   projektu. Merge i publikację traktuj jako osobne zakresy zgody.

## Wynik

Działająca zmiana albo precyzyjnie opisany brak, dowody kontroli, wynik
self-review i ograniczenia. Wskazuj pominięte testy oraz ich skutek.
Nie deklaruj „wdrożono” na podstawie samego PR lub zielonego CI.
Jawne polecenie użytkownika ma pierwszeństwo przed wskazówkami skilla
w granicach zasad środowiska.
