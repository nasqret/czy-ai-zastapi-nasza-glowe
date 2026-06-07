# Czy AI zastąpi naszą głowę?

Lekka, 35-minutowa prezentacja popularnonaukowa dla klas 7-8 szkoły podstawowej
i uczniów liceum. Slajdy działają lokalnie, bez sieci i bez zewnętrznych bibliotek.

Autor: Bartosz Naskręcki, UAM/CCAI. Warszawa, 8.06.2026.

## Uruchomienie

```bash
npm run serve
```

Otwórz `http://localhost:4173`.

Można także otworzyć `index.html` bezpośrednio, ale lokalny serwer daje bardziej
przewidywalne zachowanie pełnego ekranu.

## Sterowanie

- `→`, `↓`, `Spacja`, `Enter`: ujawnij następny element lub przejdź dalej
- `←`, `↑`, `Backspace`: cofnij element lub slajd
- `N`: notatki prowadzącego
- `O`: przegląd slajdów
- `F`: pełny ekran
- `Home`, `End`: początek lub finał wykładu
- gest w lewo/prawo: nawigacja na ekranie dotykowym

Przycisk na slajdzie o wielomianie Eulera uruchamia lokalny mini-eksperyment.
Przycisk na slajdzie 16 odtwarza pracę Codex nad liczeniem prostokątów:
błędny program, test wykrywający błąd, poprawkę i końcowy wynik.
Przycisk na slajdzie 21 testuje hipotezę związaną z małym twierdzeniem Fermata,
znajduje kontrprzykład `341` i prowadzi do samodzielnego rachunku modulo 7.

Te same obliczenia można uruchomić w terminalu:

```bash
npm run demo:rectangles
npm run demo:fermat
```

## Pliki

- `index.html` - treść 22 slajdów i 2 dodatków
- `styles.css` - układ, typografia, animacje i tryb druku
- `app.js` - nawigacja, fragmenty, notatki i demo
- `PLAN.md` - plan projektu i rozkład czasu
- `MEMORY.md` - trwałe decyzje projektowe
- `LOG.md` - dziennik wykonania i testów
- `docs/SPEAKER_NOTES.md` - skrypt prowadzącego
- `docs/SOURCES.md` - bibliografia i zastrzeżenia
- `assets/` - trzy autorskie ilustracje wygenerowane dla prezentacji
- `scripts/rectangle_demo.py` - symulacja zadania użyta na slajdach 15-18
- `scripts/fermat_demo.py` - obliczenia użyte w zabawie z małym twierdzeniem Fermata
- `scripts/verify_math.py` - automatyczna kontrola wszystkich przykładów liczbowych

## Testy

```bash
npm test
npm run test:browser
```

Test statyczny sprawdza między innymi liczbę slajdów, łączny czas 35:00,
notatki prowadzącego, dane autora, unikalność identyfikatorów i istnienie lokalnych
zasobów. Test matematyczny ponownie oblicza sumę Gaussa, liczby prostokątów,
wartości wielomianu Eulera oraz przykłady związane z twierdzeniem Fermata.
Test przeglądarkowy wymaga działającego `npm run serve`, lokalnego Chrome i pakietu
Playwright dla Pythona. Otwiera każdą planszę w 1366×768, 1440×900 i 1920×1080,
sprawdza przepełnienia i interakcje oraz zapisuje kontrolne zrzuty w ignorowanym
katalogu `test-results/`.

## Druk / PDF

Style druku pokazują wszystkie ujawniane elementy i ukrywają dodatki oraz kontrolki.
W przeglądarce wybierz druk w orientacji poziomej, bez marginesów i z włączonym
drukowaniem tła.
