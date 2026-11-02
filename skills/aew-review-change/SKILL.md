---
name: aew-review-change
description: "Przeprowadź review wskazanego PR, zakresu commitów lub diffu względem wymagań; raportuj udokumentowane usterki i ograniczenia bez edycji kodu."
---

# Review konkretnej wersji zmiany

Wykonaj przegląd bez edycji kodu, wysyłania komentarzy i scalania zmian.
Raport w bieżącej rozmowie jest domyślnym wynikiem.

## Wykonanie

1. Ustal repozytorium, wymagania, instrukcje lokalne i kryteria akceptacji.
   Potwierdź, że katalog główny Git zawiera wskazane źródła. Przy pracy
   w innym katalogu jawnie kieruj polecenia do repozytorium docelowego;
   SHA startowego checkoutu nie identyfikuje plików z innego repozytorium.
2. Ustal bazowy i końcowy SHA. Dla working tree zapisz bazę i jednoznaczny
   stan diffu. Nie zmieniaj po cichu przeglądanej wersji.
3. Przejrzyj zmianę i dotknięte ścieżki wykonania, kontrakty, dane, uprawnienia,
   scenariusze błędów oraz testy według wpływu. Kosmetykę pozostaw linterom.
4. Zanim potwierdzisz zarzut, sprawdź osiągalny kod wywołujący, zabezpieczenia
   i testy. Odrzuć zarzut, jeśli wykluczają go dowody; brak kontekstu oznacz
   jako niewiadomą. Porównaj z bazą: nowe regresje oddziel od starych usterek.
   Połącz opisy tej samej przyczyny zamiast mnożyć ustalenia.
5. Dla usterki wskaż lokalizację, warunek wystąpienia, skutek i dowód.
   Podejrzenia oraz sugestie oddziel od potwierdzonych problemów.
   Zero potwierdzonych nowych usterek jest prawidłowym wynikiem.
6. Sprawdź, czy zielony wynik nie pochodzi z usuniętych asercji, pominiętych
   testów, wyłączonych reguł lub obniżonych progów. Oceń uzasadnienie zmiany
   kontroli względem wymagań; sama obecność takiej zmiany nie dowodzi usterki.
7. Kontrole wykonuj w dozwolonym środowisku. Jeśli checkout ma obce zmiany,
   nie przełączaj ani nie resetuj go kosztem tych zmian.
8. Opisz zakres i niewykonane kontrole. Brak wykrytych usterek nie stanowi
   gwarancji poprawności. Nowe commity wymagają kontroli zmienionej części.
9. Naprawa, komentarz na GitHubie i merge wymagają objęcia zakresem polecenia.
   Review samo ich nie upoważnia. Dodatkowe niezależne AI review wykonuj
   tylko wtedy, gdy delegowanie jest dostępne i dozwolone.

## Wynik

Wersja zmiany, zakres, nowe usterki, oddzielnie istniejące problemy i hipotezy,
wyniki wykonanych kontroli oraz ograniczenia. Ustalenia uporządkuj według skutku.
Gdy użytkownik wyraźnie zleca także poprawki lub publikację komentarza,
wykonaj je w granicach tej zgody; jawne polecenie ma pierwszeństwo
przed domyślnym trybem skilla w granicach zasad środowiska.
