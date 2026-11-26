---
name: aew-plan-change
description: "Przygotuj plan implementacji na podstawie rozmowy, analizy i uzgodnionych wymagań. Użyj, gdy użytkownik prosi o plan lub przyjmuje propozycję planowania."
---

# Plan implementacji

1. Zbierz ustalenia z czatu, dostępnej analizy i źródeł projektu. Możesz
   planować bez osobnego dokumentu analizy. Krótko opisz oczekiwany efekt,
   granice i kryteria akceptacji. Zachowaj wcześniejsze decyzje.
2. Jeśli możliwe interpretacje zmieniają wynik lub kolejność prac, najpierw
   sprawdź dostępne źródła. Gdy wybór należy do użytkownika, zadaj konkretne
   pytanie. Jeśli to możliwe, zilustruj problem przykładem. Podaj rekomendowaną
   odpowiedź i krótkie uzasadnienie. Poczekaj na rozstrzygnięcie zależnej
   części planu. Odróżnij propozycję od przyjętej decyzji.

   Przykład pytania przy dodawaniu obowiązkowego pola:
   „Co ma się stać przy otwarciu starego wpisu bez tej wartości? Proponuję
   pozwolić na odczyt i wymagać uzupełnienia przy zapisie, bo nie znamy
   wartości historycznej.”

3. Ułóż kroki według zależności. Przy każdym wskaż zakres prac, oczekiwany
   rezultat i sposób jego sprawdzenia. Powiąż kontrole z kryteriami akceptacji.
   Uwzględnij migrację lub odzyskanie danych, gdy wymaga tego zmiana.
   Przy podziale pracy wskaż, co musi być gotowe przed kolejnym krokiem, kto
   odpowiada za wspólny kontrakt i kiedy sprawdzisz wynik po połączeniu prac.
   Przykładowo, gdy API dopiero powstaje, zaplanuj mały działający fragment
   backendu potwierdzający żądanie, odpowiedź sukcesu i istotny błąd. Frontend
   może w tym czasie rozwijać część niezależną od API. Po ustaleniu kontraktu
   obie strony i ich testy mogą powstawać równolegle. Przy małej zmianie,
   silnych zależnościach lub braku możliwości delegowania zaplanuj jednego wykonawcę.
4. Domyślnie zapisz plan w pliku Markdown w repozytorium. Użyj ścieżki
   uzgodnionej w rozmowie lub dobierz nazwę do tematu i konwencji projektu.
   Jeśli analiza i plan mają wspólny dokument, dodaj sekcję, zachowując
   wcześniejsze ustalenia. Podaj użytkownikowi ścieżkę zapisanego planu.
   Przy wyborze „tylko w czacie” przedstaw cały plan w odpowiedzi i pomiń
   zapis do pliku.

Samo zlecenie planowania kończy się dostarczeniem planu. Do implementacji
przejdź, gdy obejmuje ją polecenie użytkownika.
