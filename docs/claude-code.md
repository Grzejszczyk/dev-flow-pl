# Instalacja dev-flow w Claude Code

Wymagane są Git i Claude Code z obsługą poleceń `plugin`. W terminalu sprawdź
`claude --version` i `claude plugin --help`.

## Instalacja z GitHuba

W katalogu użytkownika lub projektu uruchom w terminalu:

```powershell
claude plugin marketplace add Grzejszczyk/dev-flow-pl
claude plugin install dev-flow@aew
claude plugin list
claude plugin details dev-flow
```

Domyślny zakres użytkownika udostępnia wtyczkę w kolejnych projektach.
Aby powtórzyć instalację konkretnej rewizji, w Claude Code 2.1.324 lub nowszym
dodaj źródło jako `Grzejszczyk/dev-flow-pl#PELNY_SHA`, podstawiając pełny SHA
commitu zawierającego katalog Claude. Jeśli masz już marketplace o nazwie
`aew`, sprawdź jego źródło poleceniem `claude plugin marketplace list`.

Otwórz nową sesję Claude Code w projekcie docelowym lub wykonaj
`/reload-plugins` w otwartej sesji. Wpisz `/dev-flow:` i sprawdź, czy
podpowiedzi obejmują siedem [skilli](../README.md#skille). Przykładowe użycie:

```text
/dev-flow:aew-analyze-change Przeanalizuj zmianę opisaną w tym issue. Na razie tylko analiza.
```

Aby pobrać zmiany ze śledzonej gałęzi, uruchom kolejno
`claude plugin marketplace update aew` i `claude plugin update dev-flow@aew`,
a następnie rozpocznij nową sesję. [Zarządzanie wtyczkami](https://code.claude.com/docs/en/plugins/install)

## Wspólne instrukcje projektu

[Marketplace Claude](../.claude-plugin/marketplace.json) wskazuje katalog główny
pakietu. Claude wykrywa w nim `skills/`, z którego korzysta również Codex.
Procedurę zmieniaj raz, w odpowiednim `SKILL.md`.

Zasady danego projektu utrzymuj w jego własnym `AGENTS.md`. Aby wczytać je
w Claude Code, umieść poniższy import w sąsiednim `CLAUDE.md`. Jeśli plik
już istnieje, dopisz import, zachowując istniejące instrukcje.

```text
@AGENTS.md
```

Tak działa [plik tego repozytorium](../CLAUDE.md). Przy domyślnej konfiguracji
Claude Code od wersji 2.1.277 potrafi też odczytać `AGENTS.md` bezpośrednio,
gdy w katalogu roboczym i nadrzędnych brakuje projektowych plików instrukcji
Claude. W nowej sesji sprawdź załadowane pliki poleceniem `/memory`.
Instalacja skilli udostępnia procedury. Przyjęte dokumenty standardu,
szablony i profil projektu wybierz zgodnie z [zasadami adopcji](adoption.md).
[Wczytywanie instrukcji projektu](https://code.claude.com/docs/en/memory)

## Sprawdzenie przed instalacją z GitHuba

W katalogu sklonowanego repozytorium uruchom `claude plugin validate .`.
Aby sprawdzić również dystrybucję, dodaj lokalny katalog przez
`claude plugin marketplace add ./` w osobnej konfiguracji testowej,
zainstaluj `dev-flow@aew` i sprawdź komplet skilli w nowej sesji.

Dobór skilla przez model i wykonanie procedury sprawdzaj osobno według
[przypadków ewaluacyjnych](../evals/README.md). Dla przykładu porównaj
jawną analizę oraz prośbę o analizę bez nazwy skilla. Zapisz wybrany skill,
wynik i ewentualne zmiany plików. [Tworzenie i testowanie marketplace](https://code.claude.com/docs/en/plugins/create-marketplace)
