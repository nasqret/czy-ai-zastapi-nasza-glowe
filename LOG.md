# Dziennik projektu

## 2026-06-07

### Rozpoznanie

- Katalog roboczy był pusty i nie był repozytorium git.
- Wybrano samodzielne slajdy HTML/CSS/JS, bez frameworka prezentacyjnego.
- Sprawdzono aktualny oficjalny podręcznik Codex z 7 czerwca 2026.
- Potwierdzono w dokumentacji nacisk na kontekst, kryterium „done when”,
  narzędzia, testy i przegląd pracy.

### Projekt

- Ustalono 21 slajdów podstawowych i 2 dodatki.
- Czas głównej części ustawiono na dokładnie 35:00.
- Wybrano przykłady matematyczne: suma Gaussa, `0,999…=1`,
  fałszywy dowód `1=2` i wielomian `n²+n+41`.
- Zmieniono zbyt mocne „AI nie generuje idei” na rozróżnienie:
  propozycja, nowość, wartość i intuicja.

### Grafika

- Wygenerowano trzy autorskie ilustracje w jednej konwencji.
- Skopiowano je do `assets/`.
- Zweryfikowano wymiary: 1672×941.

### Implementacja

- Dodano nawigację klawiaturą, dotykiem i przyciskami.
- Dodano stopniowe ujawnianie treści.
- Dodano panel notatek, zegar, przegląd slajdów i pełny ekran.
- Dodano lokalny mini-eksperyment dla wielomianu Eulera.
- Dodano tryb druku i obsługę `prefers-reduced-motion`.

### Weryfikacja

- Walidacja statyczna: 19/19 kontroli.
- Test przeglądarkowy: 23/23 slajdy.
- Rozdzielczości: 1366×768, 1440×900, 1920×1080.
- Sprawdzono pełne ujawnienie treści, granice kadru, błędy konsoli i strony.
- Sprawdzono nawigację do przodu i do tyłu, fragmenty, panel notatek,
  przegląd slajdów oraz demo Eulera.
- Pierwszy przebieg wykrył i pomógł poprawić przepełnienie cytatu na slajdzie
  Gaussa, układ par liczb oraz brak pustej ikony strony.
- Końcowy przebieg: brak przepełnień i błędów.

### Redakcja językowa

- Zastąpiono kalki z angielskiego i techniczny żargon naturalnymi polskimi
  sformułowaniami.
- Zachowano ustalony tytuł wykładu: „Czy AI zastąpi naszą głowę?”.
- Uproszczono podpisy, przykłady i instrukcje kierowane do uczniów.
- Po redakcji ponownie sprawdzono 23 slajdy w trzech rozdzielczościach:
  brak przepełnień i błędów.

### Poprawki slajdów 12-13

- Slajd `0,999…=1` otrzymał układ w trzech wierszach, który oddziela puentę
  od ramek z dowodami także na niższych ekranach.
- Do fałszywego dowodu `1=2` dodano ilustrację sposobu pracy Codex:
  precyzyjne polecenie, analiza założenia, wyliczenie `a−b=0` i wskazanie
  pierwszej niedozwolonej operacji.
- Test przeglądarkowy sprawdza teraz również nakładanie się głównych sekcji
  na obu slajdach.

### Konkretne studium przypadku Codex

- Slajdy 15, 16 i 18 przebudowano wokół pytania:
  „Ile prostokątów ma szachownica 8×8?”.
- Slajd 15 pokazuje błędny szybki strzał `64`, pomysł wyboru linii, program
  sprawdzający i pytanie człowieka o zaliczanie kwadratów.
- Slajd 16 zawiera klikalną symulację terminala: wynik `784`, nieudany test
  planszy `1×1`, diagnozę błędu `n` zamiast `n+1`, poprawkę i wynik `1296`.
- Dodano odtwarzalny skrypt `scripts/rectangle_demo.py`.
- Slajd 18 pokazuje konkretną rozmowę ucznia z Codexem oraz przeniesienie metody
  na planszę `10×10`.
- Test przeglądarkowy uruchamia symulację i wymaga obecności `784`, `FAIL`
  oraz końcowego `1296`.
