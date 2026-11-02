# Instalacja pluginu w Codex

Plugin: `dev-flow`. Marketplace: `aew`.
Wersja pakietu: [plugin.json](../plugin.json).
Pakiet udostępnia sześć skilli, bez serwera MCP, konektorów i hooków.

Wymagany klient obsługujący pluginy i dostęp do repozytorium GitHub.
Dopóki repozytorium jest prywatne, potrzebne jest działające uwierzytelnienie Git. Przed rozpoczęciem sprawdź `codex --version`
oraz `codex plugin add --help`. Rozszerzenie IDE nie obsługuje pluginów według
dokumentacji sprawdzonej 2026-10-29.

Szybkie polecenia PowerShell dla pierwszej instalacji i aktualizacji z gałęzi
main oraz rozwiązanie problemu nierozpoznawanego polecenia codex mają źródło
w [README](../README.md#instalacja-i-aktualizacja-w-powershell).
Poniżej opisano wariant powtarzalny, przypięty do pełnego SHA.

## Instalacja z GitHuba

Wybierz pełny SHA sprawdzonego commitu zawierającego manifest i marketplace.
Przed merge może to być commit PR; po merge wybierz commit main. Poniższy
znacznik trzeba zastąpić rzeczywistym SHA z tego repozytorium. Historyczne SHA
ze starszego źródła nie należą do historii `dev-flow-pl`.

```text
codex plugin marketplace add Grzejszczyk/dev-flow-pl --ref PELNY_SHA --json
codex plugin list --marketplace aew --available --json
codex plugin add dev-flow@aew --json
codex plugin list --marketplace aew --json
```

Pierwsza komenda rejestruje źródło i pobiera konkretną wersję marketplace.
Druga potwierdza widoczność pakietu, trzecia instaluje i włącza go dla użytkownika.
Lista po instalacji powinna potwierdzić `installed: true` i `enabled: true`.
Pakiet nie wymaga osobnego logowania do usługi; pole `ON_INSTALL` jest
wymaganą metadaną katalogu, a repozytorium prywatne nadal wymaga dostępu Git.

Nie dodawaj tokenu do URL ani plików konfiguracyjnych tego repozytorium.
Jeśli pobranie nie działa, sprawdź dostęp do repozytorium i konfigurację Git.
W razie konfliktu istniejącego źródła `aew` odczytaj jego pochodzenie;
nie zastępuj go bez sprawdzenia.

## Użycie i sprawdzenie

Rozpocznij nową sesję Codex. Wybierz plugin w katalogu pluginów lub sprawdź
dostępność dołączonych skilli w selektorze. Klient może pokazywać ich nazwy
z prefiksem pluginu.

Przykład pierwszego zadania:

> Użyj $dev-flow:aew-analyze-change do analizy tej zmiany.
> Na razie tylko analiza, bez edycji plików.

Pierwszy [raport odbioru](plugin-verification.md) dotyczy poprzedniej nazwy
pluginu i wskazanego tam commitu; nie potwierdza odbioru `dev-flow`.
Instalacja, wykrycie skilli i poprawne wykonanie zadania to trzy odrębne kontrole.
Lista pluginów potwierdza instalację, a lista skilli w nowej sesji ich wykrycie.
Pilotaż według [scenariuszy](pilot.md) sprawdza zachowanie agenta.
Instalacja nie kopiuje AGENTS.md do projektów i nie zmienia ich zasad.
Adaptację projektu wykonaj według [adopcji](adoption.md).

## Lokalny rozwój

W katalogu roboczym z manifestem można dodać lokalne źródło:

```text
codex plugin marketplace add . --json
```

Instaluj dopiero po sprawdzeniu zestawu plików. Lokalna kopia może zawierać
niecommitowane materiały, dlatego do powtarzalnego odbioru preferuj Git i pełny SHA.
Instalacja z lokalnego źródła trafia do cache, więc edycja źródeł nie jest
dowodem aktualizacji zainstalowanej kopii.

## Zmiana źródła marketplace

Repozytorium `dev-flow-pl` ma własną historię. Plugin nadal nazywa się
`dev-flow@aew`, a marketplace `aew`; zmiana adresu nie aktualizuje instalacji.
Dwa źródła o identyfikatorze `aew` nie są w tej procedurze używane równocześnie.

W ramach zleconej migracji odczytaj `codex plugin list --marketplace aew --json`
oraz `codex plugin marketplace list --json`. Potwierdź, że źródło `aew`
udostępnia wyłącznie ten plugin. Zapisz poprzedni adres źródła, pełny SHA
i identyfikator zainstalowanego pluginu na potrzeby powrotu.

Dla istniejącej instalacji `dev-flow@aew` wykonaj kolejno, zastępując znacznik
sprawdzonym SHA z `dev-flow-pl`:

```text
codex plugin remove dev-flow@aew --json
codex plugin marketplace remove aew --json
codex plugin marketplace add Grzejszczyk/dev-flow-pl --ref NOWY_PELNY_SHA --json
codex plugin list --marketplace aew --available --json
codex plugin add dev-flow@aew --json
codex plugin list --marketplace aew --json
```

Jeżeli stan wskazuje starszy identyfikator pluginu, usuń wyłącznie potwierdzony
identyfikator zamiast zakładać `dev-flow@aew`. Nie usuwaj innych pluginów ani
źródeł. Gdy krok nie powiedzie się, odczytaj aktualny stan przed kontynuacją.

Potwierdź `installed: true`, `enabled: true` i wersję z manifestu. W nowej sesji
sprawdź sześć skilli z prefiksem `dev-flow:` dla pakietu 0.2.0.
Adaptacja instrukcji innych projektów wymaga objęcia zakresem zadania.

Aby wrócić po nieudanej migracji, najpierw sprawdź stan. Usuń wyłącznie
częściowo dodaną instalację i jej źródło, następnie ponownie dodaj zapisany
poprzedni adres z jego SHA oraz zainstaluj zapisany identyfikator pluginu.
Starego SHA nie używaj z adresem nowego repozytorium. Nie usuwaj całego cache.

## Aktualizacja i usunięcie

Przejrzyj zmiany i wybierz kolejny commit. Dla przypiętego źródła wykonaj
reinstalację wyłącznie tego pluginu i źródła, po potwierdzeniu, że aew wskazuje
właściwe repozytorium:

```text
codex plugin remove dev-flow@aew --json
codex plugin marketplace remove aew --json
codex plugin marketplace add Grzejszczyk/dev-flow-pl --ref NOWY_PELNY_SHA --json
codex plugin add dev-flow@aew --json
codex plugin list --marketplace aew --json
```

Porównaj faktyczny ref i zawartość pakietu. Nie usuwaj innych źródeł ani
ręcznie całego cache Codex.

`codex plugin marketplace upgrade aew --json` odświeża wybrane źródło;
przy pełnym SHA nie przesuwa go automatycznie na nową wersję main.
Po zmianie instalacji rozpocznij nową sesję. Aktualizacja pluginu nie nadpisuje
lokalnych instrukcji projektu.

Aby usunąć wyłącznie ten plugin i jego źródło:

```text
codex plugin remove dev-flow@aew --json
codex plugin marketplace remove aew --json
```

Te polecenia zmieniają konfigurację użytkownika; wykonuj je w ramach zleconej
instalacji, aktualizacji lub usunięcia. Publikacja w publicznym katalogu,
zmiana widoczności repozytorium i tag wydania są osobnymi działaniami.

## Źródła i zgodność

- [Pakiet, marketplace i ścieżki](https://developers.openai.com/plugins/build/plugins)
- [CLI: plugin add, list i marketplace](https://learn.chatgpt.com/docs/cli/reference)
- [Dostępność pluginów](https://learn.chatgpt.com/docs/plugins)

Dokumentacja i lokalny CLI mogą różnić się zakresem funkcji. Weryfikuj polecenia
na używanej wersji; opis wyniku odbioru powinien podawać wersję klienta i SHA.
