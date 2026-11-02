# Zastosowanie standardu w projekcie

Standard jest wersjonowanym materiałem źródłowym. Dostęp do repozytorium
nie powoduje automatycznego wczytania go przez agenta.

## Adaptacja istniejącego projektu

1. Przeczytaj lokalne instrukcje i sprawdź stan repozytorium.
2. Wybierz pełny SHA tego standardu. Do czasu wydania tagu nie nazywaj go
   stabilnym wydaniem. Repozytorium prywatne wymaga własnego dostępu.
3. Uzupełnij [profil](../templates/project-profile.md) na podstawie
   potwierdzonej konfiguracji projektu. Nieznane wartości oznacz jako otwarte.
4. Dostosuj [fragment AGENTS.md](../templates/project-agents.md), zachowując
   lokalne decyzje. Nie zastępuj całego istniejącego pliku.
5. Wskaż potrzebne szablony i sposób udostępnienia skilli.
6. Wykonaj zmianę przez PR. Konfigurację ochrony brancha i CI sprawdź oddzielnie.
7. Przeprowadź pilotaż, odnotowując faktyczne wyniki.

Można wykonać analizę adaptacji bez edycji plików. Zapis i konfiguracja
wymagają objęcia zakresem zadania. Setup nie instaluje globalnie narzędzi
i nie zmienia ustawień GitHub bez takiego polecenia.

## Korzystanie ze źródeł skilli

Foldery w skills/ nie są automatycznie wykrywane po samym klonowaniu.
W obecnej wersji można:

- Wskazać agentowi pełną ścieżkę do wybranego SKILL.md i polecić jego użycie.
- Skopiować wybrane foldery do .agents/skills/ docelowego repozytorium,
  jeżeli adopcja została zlecona. Zanotować źródłowy SHA w profilu.
- Utrzymywać własną instalację lokalną według dokumentacji danego narzędzia.

Każdy skill zawiera instrukcje potrzebne do swojego zadania i nie wymaga
rodzeństwa ani tego repozytorium po skopiowaniu. Szablony są opcjonalne.
Unikaj podwójnego instalowania tych samych skilli z repozytorium i pluginu.

Przykładowe polecenie po udostępnieniu skilla:

> Użyj $aew-analyze-change do analizy zmiany opisanej w tym issue.
> Przedstaw kryteria akceptacji i wpływ na dane. Na razie tylko analiza.

## Dystrybucja jako plugin

Repozytorium zawiera [manifest](../plugin.json) i [marketplace aew](../.agents/plugins/marketplace.json).
Plugin korzysta bezpośrednio z skills/; nie utrzymujemy drugiej kopii procedur.
Instalację i aktualizację z przypiętego commitu opisuje
[instrukcja](plugin-installation.md).

Pakiet nie wymaga MCP ani hooków. Instalacja udostępnia skille w obsługiwanym
kliencie; lokalne instrukcje i profil projektu nadal określają jego zasady.
Nie utożsamiaj poprawnego JSON, instalacji, wykrycia skilli i pilotażu zachowania.
Każda z tych kontroli wymaga właściwego dowodu.

## Aktualizacje

Projekt zapisuje repozytorium źródłowe, pełny commit oraz listę przyjętych
materiałów i lokalnych odstępstw. Nie opieraj powtarzalnego procesu wyłącznie
na zmiennym main.

Aktualizacja to przegląd zmian standardu, adaptacja lokalnych różnic, właściwe
sprawdzenia i PR w projekcie. Nie nadpisuj lokalnych instrukcji automatycznie.
Wersję pakietu odczytuj z plugin.json, a dokładne źródło z przypiętego SHA marketplace.

## Nowy projekt

Użyj profilu i szablonów, wybierając tylko potrzebne materiały.
Nie kopiuj stosu technologicznego, danych i zasobów projektu wzorcowego.
Ten zestaw nie jest jeszcze skonfigurowanym GitHub Template Repository.
