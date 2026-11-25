# Formatowanie C#

Przed edycją ustal reguły obowiązujące dla danego pliku, korzystając z instrukcji
projektu (np. AGENTS.md) i konfiguracji (np. .editorconfig). Dla każdej kwestii
stosuj regułę projektu, jeśli ją określono. Poniższe reguły domyślne uzupełniają
pozostałe kwestie i dotyczą tylko nowego lub zmienianego kodu C#.

- Stosuj styl Allmana. Klamrę otwierającą typ, konstruktor, metodę lub blok
  sterujący zapisuj w osobnej linii.
- Zapisuj ciała konstruktorów i metod jako wieloliniowe bloki. Preferuj zapis
  blokowy także dla właściwości i funkcji lokalnych. Każdą deklarację i
  instrukcję zapisuj osobno. Czytelna właściwość automatyczna lub krótka lambda
  używana przez API albo LINQ może pozostać w jednej linii.
- Oddziel pustą linią blok pól `private readonly` od konstruktora oraz kolejne
  konstruktory, metody i właściwości.
- Długi łańcuch wywołań zapisuj z jednym wywołaniem na linię i wcięciem
  kontynuacji. Usuwaj końcowe białe znaki.
