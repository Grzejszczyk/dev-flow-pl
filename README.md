# dev-flow-pl

Wspólny standard współpracy człowieka i agentów AI: od ustalenia celu do
sprawdzenia działającej zmiany po publikacji.

**Status: standard v0.2 do pilotażu.** Repozytorium zawiera źródła oraz pakiet
pluginu do instalacji z własnego marketplace. Wersję i SHA sprawdzaj przed
instalacją; obecność manifestu nie zastępuje odbioru ani pilotażu.
Język materiałów: polski. Nazwy plików i skilli: angielskie.

Repozytorium `dev-flow-pl` udostępnia polskie instrukcje. Plugin zachowuje
nazwę `dev-flow`, marketplace identyfikator `aew`, a skille prefiks `aew-`.
Zmianę źródła istniejącej instalacji opisuje
[instrukcja](docs/plugin-installation.md#zmiana-źródła-marketplace).

## Instalacja i aktualizacja w PowerShell

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
codex plugin remove dev-flow@aew
codex plugin marketplace remove aew
codex plugin marketplace add Grzejszczyk/dev-flow-pl --ref main
codex plugin add dev-flow@aew
codex plugin list --marketplace aew --json
```

Jeśli krok zakończy się błędem, sprawdź stan przed kontynuacją.
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

## Zacznij tutaj

1. Aby używać pluginu w Codex, wykonaj [instalację](docs/plugin-installation.md).
   Przy adaptacji projektu przeczytaj [przebieg pracy](docs/workflow.md) i [granice uprawnień](docs/authorization.md).
2. Wybierz konkretny commit standardu i przygotuj
   [profil projektu](templates/project-profile.md).
3. Zastosuj [instrukcję wdrożenia standardu](docs/adoption.md).
4. Sprawdź rezultat według [zasad weryfikacji](docs/verification.md).
5. Oceń pierwsze zadania przy użyciu [scenariuszy pilotażu](docs/pilot.md).

## Co jest gdzie

| Materiał | Odpowiedzialność |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Zasady rozwijania tego repozytorium. |
| [docs/](docs/) | Wspólny proces, uprawnienia, adopcja, weryfikacja i pilotaż. |
| [templates/](templates/) | Materiały do dostosowania do projektu i zadania. |
| [skills/](skills/) | Sześć samodzielnych procedur dla agentów, z metadanymi Codex. |
| [plugin.json](plugin.json) | Tożsamość, wersja i opis instalowalnego pakietu. |
| [Marketplace](.agents/plugins/marketplace.json) | Katalog aew wskazujący ten pakiet. |
| [scripts/validate.py](scripts/validate.py) | Lokalna kontrola struktury, skilli, pakietu i linków. |

## Skille

| Skill | Kiedy go użyć |
| --- | --- |
| [aew-setup-project](skills/aew-setup-project/SKILL.md) | Przygotowanie lub zatwierdzona adaptacja standardu do projektu. |
| [aew-analyze-change](skills/aew-analyze-change/SKILL.md) | Analiza zmiany przed implementacją. |
| [aew-implement-change](skills/aew-implement-change/SKILL.md) | Realizacja uzgodnionego zakresu i proporcjonalna weryfikacja. |
| [aew-debug-change](skills/aew-debug-change/SKILL.md) | Diagnoza błędu i naprawa wyłącznie w zleconym zakresie. |
| [aew-review-change](skills/aew-review-change/SKILL.md) | Przegląd ustalonej wersji diffu i wymagań. |
| [aew-prepare-pr](skills/aew-prepare-pr/SKILL.md) | Przygotowanie zmiany do review oraz utworzenie PR w dozwolonym zakresie. |

Katalog `skills/` jest wspólnym źródłem procedur i pluginu. Samo sklonowanie
repozytorium nie instaluje skilli. Instalację opisuje [instrukcja](docs/plugin-installation.md),
a zastosowanie w projektach [adopcja](docs/adoption.md).
Rzeczywisty wynik instalacji i wykrywania skilli opisuje [odbiór](docs/plugin-verification.md).

## Zasady projektowania

- Kryteria akceptacji i dowody weryfikacji określają ukończenie zadania.
- Zakres procedury zależy od ryzyka: literówka nie wymaga pełnego planu ani ADR.
- Uzgodnione decyzje, propozycje, niewiadome i obserwacje mają odrębny status.
- Jedna informacja ma jedno utrzymywane źródło; pozostałe pliki do niego odsyłają.
- Instrukcje wspierają wykonanie; kontrole CI i ustawienia repozytorium egzekwują
  wybrane wymagania technicznie.
- Standard nie nadaje uprawnień do cudzych systemów ani do produkcji.

## Rozwój v0.2

Pierwszy pilotaż powinien objąć małą poprawkę, funkcję z testami i zmianę
wymagającą analizy migracji. Wnioski trafiają do PR zmieniającego standard.
Pakiet pluginu jest częścią repozytorium. Konfiguracja ochrony main, gotowy
template repozytorium i publikacja wydania pozostają odrębnymi zadaniami. Obecne szablony są pojedynczymi materiałami,
a nie kompletnym generatorem projektu.

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
uruchamiaj lokalnie i podawaj ich wyniki przy przygotowaniu PR.

Walidacja struktury nie potwierdza skuteczności workflow ani zachowania modelu.
Katalog przypadków i przebiegi na żądanie opisuje [ewaluacja](evals/README.md),
a zakres wykonanych prób [raport](docs/pilot-2026-11-02.md).
Do tego służy pilotaż; jego wyników nie należy deklarować przed wykonaniem.

## Źródła techniczne

Sprawdzone 2026-10-29. Materiały opisują nasz proponowany proces; poniższe źródła
wyjaśniają mechanizmy Codex, na których opieramy dystrybucję.

- [Instrukcje AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Tworzenie i odkrywanie skilli](https://learn.chatgpt.com/docs/build-skills)
- [Pakowanie pluginu](https://developers.openai.com/plugins/build/plugins)

## Licencja

Materiały są udostępniane na licencji [MIT](LICENSE).
