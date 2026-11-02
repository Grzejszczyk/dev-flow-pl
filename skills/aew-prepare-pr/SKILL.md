---
name: aew-prepare-pr
description: "Przygotuj zweryfikowaną zmianę do review, commit, push i PR zgodnie z uprawnieniami projektu; użyj przy finalizowaniu implementacji do przeglądu."
---

# Przygotowanie zmiany do PR

Dostarcz zmianę gotową do oceny przez właściciela.

## Wykonanie

1. Ustal repozytorium, branch, aktualną bazę PR, zakres wymagań i dozwolone
   czynności. Sprawdź istniejący PR, aby uniknąć duplikatu.
2. Przejrzyj końcowy diff, wyniki kontroli oraz ich związek z aktualną wersją.
   Sprawdź przypadkowe pliki, dane wrażliwe i zgodność dokumentacji.
   Gdy wznawiasz pracę po przekazaniu, porównaj zapisane SHA i wyniki
   z aktualnym stanem; zachowaj wcześniejsze zgody w ich zakresie.
3. Wykonaj brakujące kontrole proporcjonalne do zmiany. Nie przedstawiaj
   pominiętych lub niewykonanych testów jako zaliczonych.
4. Przygotuj opis: problem i wynik, istotne decyzje, dowody weryfikacji,
   ograniczenia oraz sposób wdrożenia/odzyskania działania, jeśli dotyczy.
   Użyj szablonu repozytorium, jeśli istnieje.
5. Jeśli zadanie lub lokalne zasady upoważniają do commit/push/PR, wykonaj je
   bez ponownego pytania. Zachowaj wymaganą tożsamość Git per commit.
   Dla PR sprawdzonego stosuj ready for review, chyba że użytkownik lub
   projekt wymaga draftu. Nie ukrywaj niespełnionych kontroli.
6. Po utworzeniu odczytaj stan i URL PR. Sprawdź kontrole aktualnej wersji,
   jeśli środowisko je udostępnia; brak checków opisz jako brak.
7. Zatrzymaj się przed merge, jeśli nie został autoryzowany. Gdy zgoda na merge
   już obejmuje aktualną zmianę, wykonaj lokalną procedurę i potwierdź rezultat.
   Zgoda na PR lub merge nie jest zgodą na publikację produkcyjną.

## Wynik

URL i status PR albo przygotowany opis oraz konkretny brak uprawnienia.
Podaj wyniki kontroli i decyzję oczekiwaną od właściciela.
Jawne polecenie użytkownika ma pierwszeństwo przed wskazówkami skilla
w granicach zasad środowiska.
