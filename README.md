# dev-flow-pl

Wspólny standard współpracy człowieka i agentów AI: od ustalenia celu do
sprawdzenia działającej zmiany po publikacji.

**Standard jest w fazie pilotażu.** Wersję pluginu podaje [manifest pakietu](plugin.json).
Przed instalacją sprawdź wersję i SHA wybranego commitu.

Instrukcje są po polsku, a nazwy plików i skilli po angielsku. Plugin
nazywa się `dev-flow`, marketplace ma identyfikator `aew`, a nazwy skilli zaczynają się od `aew-`.
Zmianę źródła istniejącej instalacji opisuje
[instrukcja](docs/plugin-installation.md#zmiana-źródła-marketplace).

## Zacznij tutaj

- [Instalacja w Codex przez PowerShell](#instalacja-i-aktualizacja-w-powershell)
- [Instalacja w Claude Code](#instalacja-w-claude-code)
- [Wdrożenie standardu we własnym projekcie](docs/adoption.md) jest opcjonalne.
  Jeśli je wybierasz, zapisz w [profilu projektu](templates/project-profile.md) pełny SHA
  standardu i reguły swojego repozytorium. Weź pod uwagę [przebieg pracy](docs/workflow.md)
  i [zakres uprawnień](docs/authorization.md).

W pierwszym [pilotażu](docs/pilot.md) możesz wypróbować standard na małej poprawce,
funkcji z testami i zmianie wymagającej analizy migracji. Oceń wyniki według
[zasad weryfikacji](docs/verification.md).

Po pilotażu zrezygnowaliśmy z rozszerzenia skilli o pracę z subagentami.
W trzech badanych zadaniach jeden agent osiągnął te same wyniki przy mniejszym
zużyciu tokenów. [Pomiary i uzasadnienie decyzji](docs/pilot-2026-11-26.md)

## Instalacja w Claude Code

W sesji Claude Code (od wersji 2.1.275) wpisz:

```text
/plugin install dev-flow --marketplace Grzejszczyk/dev-flow-pl
```

[Instrukcja dla Claude Code](docs/claude-code.md) opisuje instalację z GitHuba,
sprawdzenie siedmiu skilli oraz użycie zasad projektu z `AGENTS.md`.
Claude Code i Codex korzystają z tych samych plików w `skills/`.

## Instalacja i aktualizacja w PowerShell

Poniższe polecenia dotyczą Codex.

Wymagane są Codex CLI obsługujący pluginy, Git oraz dostęp do tego repozytorium.
Jeśli repozytorium jest prywatne, potrzebne jest także uwierzytelnienie Git.
Sprawdź dostępność poleceń:

```powershell
codex --version
codex plugin add --help
```

Gdy PowerShell zgłasza, że nie rozpoznaje `codex`, użyj
[instrukcji poniżej](#powershell-nie-rozpoznaje-codex).

### Pierwsza instalacja

```powershell
codex plugin marketplace add Grzejszczyk/dev-flow-pl --ref main
codex plugin add dev-flow@aew
codex plugin list --marketplace aew --json
```

`--ref main` wybiera gałąź `main`, której zawartość zmienia się po merge.
Dla instalacji powtarzalnej wybierz pełny SHA zamiast `main`, zgodnie
z [instrukcją instalacji](docs/plugin-installation.md#instalacja-z-githuba).
Samo opublikowanie nowej wersji nie zmienia źródła przypiętego do starego SHA.

### Aktualizacja istniejącej instalacji

Poniższa procedura ponownie instaluje plugin i pozwala przejść ze starego
SHA na `main`. Najpierw sprawdź istniejące źródło i instalację:

```powershell
codex plugin marketplace list --json
codex plugin list --marketplace aew --json
```

Potwierdź, że `aew` jest źródłem tego pluginu i nie udostępnia innych
pluginów. Zapisz poprzedni adres źródła i pełny SHA, aby móc wrócić do instalacji.
Poniższe polecenia zastępują źródło wersją z `Grzejszczyk/dev-flow-pl`:

```powershell
& {
    $ErrorActionPreference = 'Stop'
    function Invoke-CodexStep {
        codex @args
        if ($LASTEXITCODE -ne 0) {
            throw "Polecenie 'codex $args' zwróciło kod $LASTEXITCODE."
        }
    }

    Invoke-CodexStep plugin remove dev-flow@aew
    Invoke-CodexStep plugin marketplace remove aew
    Invoke-CodexStep plugin marketplace add Grzejszczyk/dev-flow-pl --ref main
    Invoke-CodexStep plugin add dev-flow@aew
    Invoke-CodexStep plugin list --marketplace aew --json
}
```

Po błędzie blok zatrzyma się. Sprawdź listę źródeł i stan pluginu, zanim wznowisz aktualizację.
Na końcu potwierdź wersję zgodną z [manifestem](plugin.json),
`installed: true` i `enabled: true`. Rozpocznij nowy chat; jeśli aplikacja
nadal pokazuje stare skille, uruchom ją ponownie.
Wariant z przypiętym SHA i odzyskiwanie instalacji opisuje
[pełna instrukcja](docs/plugin-installation.md).

### PowerShell nie rozpoznaje codex

Komunikat „codex nie jest rozpoznawany jako nazwa polecenia” oznacza, że
PowerShell nie znajduje CLI. W aplikacji polecenie może być dostępne,
chociaż zwykły terminal nie ma go w `PATH`.

Jeśli CLI jest już na dysku, poniższy przykład szuka go w typowym katalogu
instalatora oraz w katalogach aplikacji Windows i tworzy alias w bieżącej sesji.
Gdy znajdzie kilka plików, wybiera ostatnio zmodyfikowany:

```powershell
$codexPaths = @(
    "$env:LOCALAPPDATA\Programs\OpenAI\Codex\bin\codex.exe"
    "$env:LOCALAPPDATA\OpenAI\Codex\bin\*\codex.exe"
)
$codexExe = Get-ChildItem -Path $codexPaths -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $codexExe) {
    throw "Nie znaleziono codex.exe. Zainstaluj Codex CLI lub wskaż jego pełną ścieżkę."
}

Set-Alias -Name codex -Value $codexExe.FullName
codex --version
```

Alias działa tylko do zamknięcia tego okna PowerShella; nie zmienia trwale
`PATH` ani profilu użytkownika. Następnie można wykonać powyższe polecenia
`codex plugin …`. Przy innej lokalizacji wskaż istniejący `codex.exe`:

```powershell
Set-Alias -Name codex -Value 'C:\sciezka\do\codex.exe'
```

Zastąp przykładową ścieżkę własną. Jeśli CLI nie jest zainstalowany, skorzystaj
z [oficjalnej instrukcji instalacji Codex CLI](https://learn.chatgpt.com/docs/cli)
i otwórz nowe okno PowerShella.

## Co jest gdzie

| Materiał | Odpowiedzialność |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Zasady rozwijania tego repozytorium. |
| [docs/](docs/) | Wspólny proces, uprawnienia, adopcja, weryfikacja i pilotaż. |
| [templates/](templates/) | Materiały do dostosowania do projektu i zadania. |
| [skills/](skills/) | Siedem samodzielnych procedur dla agentów, z metadanymi Codex. |
| [plugin.json](plugin.json) | Tożsamość, wersja i opis instalowalnego pakietu. |
| [Marketplace](.agents/plugins/marketplace.json) | Katalog aew wskazujący ten pakiet. |
| [scripts/validate.py](scripts/validate.py) | Lokalna kontrola struktury, skilli, pakietu i linków. |

## Skille

| Skill | Kiedy go użyć |
| --- | --- |
| [aew-setup-project](skills/aew-setup-project/SKILL.md) | Przygotowanie lub zatwierdzona adaptacja standardu do projektu. |
| [aew-analyze-change](skills/aew-analyze-change/SKILL.md) | Analiza zmiany przed implementacją. |
| [aew-plan-change](skills/aew-plan-change/SKILL.md) | Plan implementacji z ustaleń rozmowy, w repozytorium lub tylko w czacie. |
| [aew-implement-change](skills/aew-implement-change/SKILL.md) | Realizacja uzgodnionego zakresu i proporcjonalna weryfikacja. |
| [aew-debug-change](skills/aew-debug-change/SKILL.md) | Diagnoza błędu i naprawa wyłącznie w zleconym zakresie. |
| [aew-review-change](skills/aew-review-change/SKILL.md) | Przegląd ustalonej wersji diffu i wymagań. |
| [aew-prepare-pr](skills/aew-prepare-pr/SKILL.md) | Przygotowanie zmiany do review oraz utworzenie PR w dozwolonym zakresie. |

Katalog `skills/` jest wspólnym źródłem procedur i pluginu. Samo sklonowanie
repozytorium nie instaluje skilli. Instalację opisuje [instrukcja](docs/plugin-installation.md),
a zastosowanie w projektach [adopcja](docs/adoption.md).
[Historyczny odbiór instalacji pluginu 0.1.0](docs/plugin-verification.md) opisuje
instalację i wykrywanie skilli z poprzedniego repozytorium.

## Zasady projektowania

- Kryteria akceptacji i dowody weryfikacji określają ukończenie zadania.
- Zakres procedury zależy od ryzyka: literówka nie wymaga pełnego planu ani ADR.
- Uzgodnione decyzje, propozycje, niewiadome i obserwacje mają odrębny status.
- Jedna informacja ma jedno utrzymywane źródło; pozostałe pliki do niego odsyłają.
- Instrukcje wspierają wykonanie; kontrole CI i ustawienia repozytorium egzekwują
  wybrane wymagania technicznie.
- Standard nie nadaje uprawnień do cudzych systemów ani do produkcji.

## Weryfikacja repozytorium

Wymagany Python 3.11+; walidator i jego testy korzystają wyłącznie z biblioteki
standardowej.

```text
python scripts/validate.py
python scripts/validate_evals.py
python -m unittest discover -s tests -v
git diff --check
```

W tym repozytorium nie skonfigurowano GitHub Actions. Powyższe kontrole
uruchamiaj lokalnie. Po commicie sprawdź cały zakres PR poleceniem
`git diff --check origin/main...HEAD` względem aktualnej bazy i podaj wyniki w PR.

Zachowanie agenta sprawdza się osobno. [Instrukcja ewaluacji](evals/README.md)
opisuje przypadki i sposób przeprowadzenia prób.
[Raport z pilotażu z 2 listopada 2026](docs/pilot-2026-11-02.md) dokumentuje
próby wcześniejszej wersji standardu w jednorazowych repozytoriach testowych.

## Źródła techniczne

Sprawdzone 2026-10-29. Materiały opisują nasz proponowany proces; poniższe źródła
wyjaśniają mechanizmy Codex, na których opieramy dystrybucję.

- [Instrukcje AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Tworzenie i odkrywanie skilli](https://learn.chatgpt.com/docs/build-skills)
- [Pakowanie pluginu](https://developers.openai.com/plugins/build/plugins)

## Licencja

Materiały są udostępniane na licencji [MIT](LICENSE).
