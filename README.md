# Czy AI zastąpi naszą głowę?

Dwujęzyczny, interaktywny serwis do 35-minutowego wykładu popularnonaukowego
dla klas 7-8 szkoły podstawowej i liceum.

Autor: Bartosz Naskręcki, UAM/CCAI. Warszawa, 8.06.2026.

Strona: <https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/>

## Zawartość

- `/` - landing page z wyborem języka;
- `/pl/` - polska prezentacja;
- `/en/` - angielska prezentacja;
- `/experiments/pl/` - pięć polskich laboratoriów Codex Math Lab;
- `/experiments/en/` - pięć angielskich laboratoriów;
- `scripts/build_english_presentation.py` - odtwarzalne generowanie wersji EN;
- `docs/` - notatki prowadzącego, źródła i materiały organizacyjne.

Laboratoria wykonują obliczenia lokalnie w przeglądarce. Nie łączą się z API,
nie wysyłają danych i jasno oznaczają dzienniki pracy Codexa jako symulacje.

## Uruchomienie

```bash
npm run serve
```

Otwórz <http://127.0.0.1:4173/>.

## Sterowanie prezentacją

- `→`, `↓`, `Spacja`, `Enter` - następny element lub slajd;
- `←`, `↑`, `Backspace` - poprzedni element lub slajd;
- `N` - notatki prowadzącego;
- `O` - przegląd slajdów;
- `F` - pełny ekran;
- `Home`, `End` - początek lub finał.

## Testy

```bash
npm test
npm run test:browser
```

`npm test` generuje wersję angielską, wykonuje 85 kontroli struktury i ponownie
przelicza wszystkie przykłady matematyczne. Test przeglądarkowy sprawdza 48
slajdów w trzech rozdzielczościach, interakcje, landing page i laboratoria
na desktopie oraz telefonie.

## Publikacja

Serwis jest statyczny i działa bez procesu budowania po stronie GitHub Pages.
Publikowana jest gałąź `main`, katalog `/`.

## Prawa

Copyright © 2026 Bartosz Naskręcki. All rights reserved.

Kod i materiały są publicznie widoczne, ale nie zostały udostępnione na licencji
zezwalającej na kopiowanie lub redystrybucję. Szczegóły: [LICENSE](LICENSE).
