# Plan wprowadzenia pracy z subagentami do dev-flow

Propozycja do review. Celem jest skrócenie drogi do zweryfikowanego wyniku lub
wykrycie istotnego pominięcia przy akceptowalnym koszcie. Zadanie nadal prowadzi
jeden koordynator. Poniższe etapy opisują przyszłe zmiany w standardzie i skillach.

## 1. Ustalić, kiedy dzielić pracę

W [standardzie pracy](../workflow.md) opisać decyzję koordynatora. Delegowanie
ma sens, gdy da się wskazać odrębne pytania lub zakresy edycji, wspólny punkt
wyjścia i sposób sprawdzenia wyników. Przy małej poprawce, silnych zależnościach
lub braku możliwości delegowania jeden agent prowadzi zadanie do końca.
Niezależne, gotowe komendy może uruchomić równolegle samo narzędzie.

Przydział zawiera cel, źródła i wersję, zakres odczytu lub edycji oraz oczekiwany
wynik. Subagent zwraca ustalenie albo zmianę, dowód i istotne niewiadome.
Koordynator odpowiada za wspólne pliki, komunikowanie zmian kontraktu, integrację
i jedną odpowiedź dla użytkownika. Przy przerwanym podzadaniu sprawdza jego
rzeczywisty stan, po czym kończy je sam lub przekazuje innemu wykonawcy.
Wszyscy działają w granicach [uprawnień zadania](../authorization.md).

**Odbiór etapu.** Dla poprawki literówki agent wybiera pracę samodzielną.
Dla większej zmiany potrafi wskazać zależność wymagającą kolejności i zadania,
które mogą się rozpocząć równolegle. Każdy zmieniony skill ma działać także
po skopiowaniu wyłącznie jego katalogu.

## 2. Wprowadzić analizę z pytaniami uzupełniającymi

Pierwszą zmianę po opisaniu zasad wprowadzić do skilla `aew-analyze-change`.
Koordynator rozdziela rozpoznanie według obszarów, zestawia odpowiedzi i sprawdza,
czy nowe odkrycie albo sprzeczność może zmienić rekomendację, zakres lub kryteria
akceptacji. W takim przypadku przekazuje konkretne pytanie subagentowi, który zna
już źródła. Może wybrać innego wykonawcę, jeśli pytanie dotyczy nowego obszaru
lub wymaga niezależnego sprawdzenia.

**Przykład do pilotażu.** Użytkownik rozważa dodanie obowiązkowego pola do formularza.

| Krok | Praca i oczekiwany wynik |
| --- | --- |
| Rozpoznanie równoległe | Jeden agent bada walidację formularza, drugi klientów API, trzeci istniejące dane. Agent od API odnajduje import korzystający z tego samego endpointu. Agent od danych odnajduje starsze rekordy bez wartości pola. |
| Pytanie wynikające z ustaleń | Koordynator łączy oba fakty i pyta agenta od API „Czy import aktualizuje takie rekordy przez ten endpoint i co stanie się po włączeniu walidacji?”. Agent wskazuje ścieżkę od importu do zapisu oraz miejsce sprawdzania pola. |
| Domknięcie | Jeśli ścieżka dotyczy starszych rekordów, koordynator pokazuje konsekwencje i pyta właściciela, jakie zachowanie importu przyjąć, o ile źródła tego nie rozstrzygają. Jeśli kod wyklucza tę ścieżkę, zamyka wątek z dowodem. |

Kolejna runda ma odpowiadać na pytanie, którego rozstrzygnięcie wpłynie na wynik.
Koordynator kończy analizę, gdy może uzasadnić rekomendację, wskazać brakujący
dowód wraz z jego znaczeniem lub przedstawić właścicielowi decyzję produktową.
Wcześniejsze ustalenia pozostają podstawą dalszej pracy, dopóki nowe źródło ich
nie podważy.

**Odbiór etapu.** Ślad próby pokazuje związek między pierwszymi ustaleniami,
kolejnym pytaniem, odpowiedzią i wnioskiem. Koordynator rozstrzyga sprzeczność
na podstawie źródeł. Przy poleceniu „tylko analiza” stan plików po analizie jest zgodny ze stanem początkowym.

## 3. Rozszerzyć planowanie, implementację i testy

W `aew-plan-change` uwzględnić kolejność wynikającą z zależności, właściciela
wspólnego kontraktu i moment połączenia prac. W `aew-implement-change` opisać
wykonanie i sprawdzenie połączonej zmiany. Poniższe przykłady dotyczą zmiany API.

| Sytuacja | Kolejność i sprawdzenie |
| --- | --- |
| Kontrakt API dopiero powstaje | Najpierw potwierdzić na najmniejszym działającym fragmencie backendu żądanie, odpowiedź sukcesu i istotny błąd. Frontend może w tym czasie rozwijać część niezależną od API. |
| Kontrakt jest ustalony | Backend i frontend mogą powstawać równolegle według tej samej wersji kontraktu, z przykładami i znaczeniem pól. Kiedy kontrakt wymaga zmiany, koordynator wstrzymuje zależne prace, uzgadnia nową wersję i przekazuje ją obu wykonawcom. |
| Równoległe pisanie testów | W przykładzie powtórnego zapisu agent BE sprawdza odpowiedź `409` i brak drugiego rekordu. Agent FE sprawdza komunikat i zachowanie wpisanych danych przy `409`. Piszą testy w rozłącznych plikach. |

**Odbiór etapu.** Po integracji koordynator sprawdza na tej samej wersji
rzeczywisty przepływ od klienta do endpointu. W celowo wadliwej wersji przykładu
klient wyświetla komunikat o konflikcie tylko przy `400`. Atrapa w teście FE zwraca
właśnie `400`, więc test przechodzi. Serwer zgodnie z kontraktem zwraca `409`.
Po powtórzeniu zapisu przez formularz koordynator wykrywa brak komunikatu.
Po poprawieniu klienta i testu potwierdza komunikat, zachowanie danych formularza
i brak drugiego rekordu na połączonej wersji.

## 4. Zastosować ten podział w diagnozie, review i ewaluacji

Po sprawdzeniu sposobu przekazywania wyników rozszerzyć poniższe procedury
tylko o wskazówki właściwe dla ich celu.

| Miejsce | Podział pracy i kryterium odbioru |
| --- | --- |
| `aew-debug-change` | Dla tego samego objawu i wersji jeden agent bada żądanie wysyłane przez klienta, drugi jego obsługę na serwerze. Koordynator porównuje dowody, wskazuje przyczynę lub otwartą hipotezę. Przy zleconej naprawie jeden wykonawca potwierdza regresję przed poprawką i wynik po niej, o ile reprodukcja jest dostępna. |
| `aew-review-change` | Gdy dodatkowy przegląd uzasadnia ryzyko lub profil projektu, recenzent dostaje wymagania i diff z bazowym oraz końcowym SHA w osobnym kontekście. Autor może równolegle wykonywać self-review i kontrole tej samej wersji. Koordynator sprawdza dowody, łączy uwagi o tej samej przyczynie i aktualizuje ocenę po zmianie kodu. |
| [Ewaluacja skilli](../../evals/README.md) | Różni agenci wykonują niezależne scenariusze na osobnych kopiach danych syntetycznych. Koordynator przypisuje obserwacje do przypadku i wersji oraz raportuje pominięte kontrole. |

## 5. Porównać wyniki i zdecydować o zakresie wdrożenia

Próby prowadzić wraz z odpowiednimi etapami. Do istniejących pakietów
`evals/cases/` dodać dwa przypadki. Dla analizy przygotować syntetyczny przykład
ze starszym rekordem i ścieżką od importu przez endpoint do walidacji. Polecenie
agenta opisuje zmianę formularza. Wzorcową ścieżkę i skutki udostępnić oceniającemu,
żeby można było sprawdzić, czy agent sam odkrył zależność. Dla BE/FE przygotować
małego klienta i serwer z opisaną rozbieżnością. Użyć formatu oczekiwań, zabronionych skutków
i dowodów. Dla review użyć przypadku `review-deduplicate-candidates`.
Dodać próbę zwykłej małej zmiany oraz wykonania zadania bez dostępnych subagentów.

Dla analizy, testów BE/FE i review porównać jednego agenta z koordynatorem
i wykonawcami w świeżych sesjach, na tym samym modelu, bazie, poleceniu
i kryteriach odbioru. Odpowiedzi właściciela w obu wariantach mają być jednakowe.
Zachować ślad pytań, działań, wersji i wyników. Zmierzyć czas do zweryfikowanego
rezultatu, łączne zużycie tokenów wszystkich agentów, jeśli host je udostępnia,
oraz przeróbki po integracji. Ocenić też pokrycie kryteriów, przeoczone błędy
i fałszywe uwagi. Statyczny przegląd scenariusza i faktyczne wykonanie z agentem
odnotować osobno w [pilotażu](../pilot.md).

**Decyzja po próbach.** Zalecić delegowanie dla tych klas zadań, w których
powtórzone próby pokazują krótszy czas przy zachowaniu jakości lub wykrycie
istotnych pominięć przy uzasadnionym koszcie. Gdy dominuje koszt koordynacji,
zachować pracę jednym agentem dla danej klasy. Przy naruszeniu zakresu poprawić
instrukcję i powtórzyć przypadek. Wyniki pilotażu będą podstawą decyzji
o udostępnieniu zmian w kolejnej wersji pluginu.
