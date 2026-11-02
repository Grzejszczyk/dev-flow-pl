# Odbiór instalacji pluginu 0.1.0

Raport historyczny sprzed utworzenia `dev-flow-pl`. Wskazany commit nie należy
do historii tego repozytorium. Wyniki nie potwierdzają instalacji z nowego źródła;
wykonaj osobny odbiór wybranego SHA z `dev-flow-pl`.

Data: 2026-10-29. Środowisko: Windows, Codex CLI 0.165.0-alpha.1.2.
Przedmiot: pakiet instrukcji i pięciu skilli, bez MCP i hooków.
Pierwszy sprawdzony commit pakietu:
`c8e734162bd219b1df2a516f3c13d3b3759b3d84`.

## Wykonane kontrole

| Kontrola | Zaobserwowany wynik |
| --- | --- |
| Walidacja plików i powiązań pakietu | 20 plików Markdown i 5 skilli; manifest i katalog poprawne według kontraktów repozytorium przed dodaniem tego raportu. |
| Testy walidatora | 13/13 zaliczonych, w tym błędne tożsamości, ścieżki, JSON i nieoczekiwany komponent MCP. |
| Dodanie źródła z GitHuba | Marketplace aew pobrany z powyższego pełnego SHA. |
| Odkrycie pakietu przed instalacją | ai-engineering-workflow, wersja 0.1.0, installed=false. |
| Instalacja przez codex plugin add | installed=true, enabled=true; wersja 0.1.0. |
| Odczyt w nowym procesie Codex | skills/list po initialize/initialized zwróciło komplet 5 włączonych skilli z cache pluginu. |
| Niezależność od katalogu projektu | Komplet 5 skilli dostępny w dwóch kontekstach: źródłowym repozytorium i innym istniejącym projekcie, bez edycji jego plików. |
| Zgodność instalacji ze źródłem | SHA256 zgodne dla wszystkich 10 plików: 5 SKILL.md i 5 metadanych UI. |

Wykryte nazwy:

- `ai-engineering-workflow:aew-setup-project`
- `ai-engineering-workflow:aew-analyze-change`
- `ai-engineering-workflow:aew-implement-change`
- `ai-engineering-workflow:aew-review-change`
- `ai-engineering-workflow:aew-prepare-pr`

## Zakres dowodu i ograniczenia

Sprawdzono rzeczywistą instalację oraz wykrywanie skilli przez nowy proces
klienta. Nie uruchamiano thread/start ani turn/start; odczyt listy nie zużywał
wywołań modelu i nie był niezależnym review AI.

To potwierdza gotowość techniczną dystrybucji. Nie jest wynikiem
[pilotażu zachowania agenta](pilot.md). Nie wykonywano odbioru interfejsu
graficznego aplikacji desktopowej ani restartu działającej aplikacji.
Nie publikowano pluginu w publicznym katalogu, nie tworzono tagu wydania
i nie zmieniano lokalnych instrukcji innych projektów.

Raport wskazuje dokładnie sprawdzony commit. Późniejsze zmiany dokumentacji
nie stanowią automatycznie ponownego odbioru innej wersji pakietu.
Aktualny wynik lokalnych kontroli i potwierdzenie końcowej wersji wymagają
osobnej weryfikacji; to repozytorium nie uruchamia GitHub Actions.

## Powtórzenie odbioru

Powyższy wynik dotyczy historycznej nazwy `ai-engineering-workflow`.
Po zmianie nazwy na `dev-flow` wymagany jest osobny odbiór nowego SHA;
oczekiwane nazwy skilli mają wówczas prefiks `dev-flow:` i zachowują `aew-*`.

Wykonaj [instalację](plugin-installation.md) dla wybranego SHA i sprawdź
installed/enabled. W nowej sesji potwierdź komplet nazw właściwych dla wersji z manifestu
(sześć w pakiecie 0.2.0) w selektorze skilli.
Dla odbioru automatycznego można użyć odczytu skills/list w świeżym procesie
app-server, zgodnie z [protokołem](https://learn.chatgpt.com/docs/app-server).
Weryfikuj ścieżki cache oraz enabled; nie dodawaj dodatkowych katalogów skilli
tylko po to, żeby uzyskać oczekiwany wynik.
