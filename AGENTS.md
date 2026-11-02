# Praca nad dev-flow-pl

To repozytorium rozwija instrukcje, skille i szablony. Wspólny standard opisuje
[workflow](docs/workflow.md), a zakres uprawnień [authorization](docs/authorization.md).
Czytaj pozostałe dokumenty wtedy, gdy dotyczą zadania.
W tym repozytorium nie ma GitHub Actions. Wymagane kontrole wykonuj lokalnie
przed przygotowaniem PR i podawaj ich wyniki.

## Zakres i źródła

- Wykonuj polecenie użytkownika w uzgodnionym zakresie. Prośba o samą analizę
  nie upoważnia do implementacji.
- Uwzględniaj wcześniej udzieloną zgodę; nie pytaj ponownie o rutynowe kroki.
- Zachowuj rozróżnienie między decyzją przyjętą, propozycją i niezweryfikowanym
  założeniem. Nie uznawaj napisanej instrukcji za dowód jej działania.
- Wspólny standard pozostaje niezależny od domeny, systemu operacyjnego,
  dostawcy chmury i stosu aplikacji. Przykłady oznaczaj jako przykłady.
- Nie kopiuj reguł biznesowych, konfiguracji ani historii klientów do wspólnych
  instrukcji. Ustawienia projektu należą do jego profilu.
- Szablony w templates/ są materiałem do adaptacji, a nie instrukcjami
  obowiązującymi w tym repozytorium.
- Skille są samodzielne: po skopiowaniu pojedynczego folderu nie mogą wymagać
  plików spoza niego. Nie duplikuj w nich całego standardu.

## Git i publikacja

- Główna gałąź to main. Nie usuwaj jej lokalnie ani zdalnie.
- Przed edycją sprawdź branch i stan plików. Zachowaj niepowiązane zmiany.
- Zmiany po inicjalizacji wykonuj na codex/<nazwa>, z aktualnego origin/main.
- Autor i committer commitów Codex: Codex <codex@local>, wyłącznie per commit;
  nie zmieniaj trwałej tożsamości Git.
- Po proporcjonalnej weryfikacji wykonaj commit, push i otwórz PR do main
  gotowy do review. Draft tylko na polecenie użytkownika.
- Wykonaj self-review względem bieżącej bazy PR. Podaj wyniki kontroli i braki.
- Merge wymaga zgody użytkownika i przechodzi przez squash merge.
- Zgoda na merge obejmuje usunięcie wyłącznie potwierdzonego feature brancha,
  po potwierdzeniu merge na GitHubie; zachowaj niepowiązane zmiany lokalne.
- Publikacja wydania/pluginu, instalacja, adopcja w innym projekcie i zmiana
  ustawień GitHub wymagają objęcia zakresem polecenia. Utworzenie PR tego nie
  upoważnia.

## Jakość

- Instrukcje i opisy pisz po polsku; nazwy skilli i plików po angielsku.
- Zmieniaj najmniejszy potrzebny zestaw zasad. Sprawdzaj sprzeczności,
  zbędne zgody i rozszerzenie zakresu, także przy edycji samych instrukcji.
- Nowy skill: wyraźny cel, warunki uruchomienia, wejście, wynik i ograniczenia.
  Nazwę folderu i frontmatter poprzedzaj aew-.
- Frontmatter skilli utrzymuj w obsługiwanym przez walidator formacie:
  name jako zwykły identyfikator i description jako jednowierszowy string JSON.
- Uruchom python scripts/validate.py, python scripts/validate_evals.py,
  python -m unittest discover -s tests -v
  i git diff --check. Zmiana walidatora wymaga odpowiednich testów.
- Zmiana znaczenia procedury wymaga sprawdzenia odpowiednich scenariuszy
  w docs/pilot.md. Odnotuj, czy przegląd był statyczny, czy wykonano przebieg
  z agentem; nie utożsamiaj tych kontroli.
- Nie commituj sekretów, lokalnych logów, śladów z danymi klientów ani ustawień
  zawierających dane dostępowe.
