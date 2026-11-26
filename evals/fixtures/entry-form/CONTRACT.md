# Formularz wpisów

Formularz pod `GET /` wysyła pole `code` metodą `POST /`. Przyjęty wpis
wyświetla komunikat „Zapisano.” i czyści pole. Przy powtórzeniu kodu
formularz wyświetla „Taki kod już istnieje.” i zachowuje wpisaną wartość.

API przyjmuje `POST /api/entries` z polem `code` w formacie
`application/x-www-form-urlencoded`. Nowy niepusty kod zwraca `201`,
powtórzony kod zwraca `409` i pozostawia jeden wpis, a pusty kod zwraca
`400`. `GET /api/entries` zwraca tablicę zapisanych kodów w JSON.
Dane przykładowe istnieją przez czas działania serwera.

## Uruchomienie

Przykład korzysta z wbudowanych modułów Node.js 22 lub nowszego.
`node server.mjs` wypisuje lokalny adres formularza.
Z katalogu przykładu uruchom `node --test api.test.mjs form.test.mjs`.
