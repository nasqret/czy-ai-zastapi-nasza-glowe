# Czy AI zastąpi naszą głowę?

Dwujęzyczny, interaktywny serwis do popularnonaukowego wykładu dla klas 7-8
szkoły podstawowej i liceum.

Autor: Bartosz Naskręcki, UAM/CCAI. Warszawa, 8.06.2026.

Strona: <https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/>

## Profile prezentacji

- `core` - 22 slajdy i dokładnie 35 minut;
- `math` - rdzeń oraz opcjonalne moduły matematyczne;
- `full` - rdzeń, matematyka i techniczne szczegóły transformera.

Profil można wybrać w panelu prowadzącego albo przez parametr adresu:
`/pl/?track=math`, `/en/?track=full`.

## Zawartość

- `/pl/` i `/en/` - prezentacje z notatkami prowadzącego;
- `/experiments/pl/` i `/experiments/en/` - pięć laboratoriów Codex Math Lab;
- `REVAMP_PLAN.md` - plan przebudowy wynikający z krytycznego audytu;
- `sources/ai_presentation_critical_audit.md` - dokument źródłowy audytu;
- `scripts/build_english_presentation.py` - ścisłe generowanie wersji angielskiej;
- `docs/` - notatki prowadzącego i bibliografia.

Laboratoria wykonują obliczenia lokalnie w przeglądarce. Nie łączą się z API
i odróżniają wynik eksperymentu od matematycznego wyjaśnienia.

## Uruchomienie

```bash
npm run serve
```

Otwórz <http://127.0.0.1:4173/>.

## Sterowanie

- `→`, `↓`, `Spacja`, `Enter` - następny element lub slajd;
- `←`, `↑`, `Backspace` - poprzedni element lub slajd;
- `N` - notatki prowadzącego;
- `O` - przegląd slajdów;
- `F` - pełny ekran;
- `Home`, `End` - początek lub koniec aktywnej ścieżki.

## Testy

```bash
npm test
npm run test:browser
```

Testy sprawdzają strukturę i lokalizację obu wersji, matematykę, profile slajdów,
interakcje, dostępność podstawową, laboratoria i układ w kilku rozdzielczościach.

## Prawa

Copyright © 2026 Bartosz Naskręcki. All rights reserved.

Kod i materiały są publicznie widoczne, ale nie zostały udostępnione na licencji
zezwalającej na kopiowanie lub redystrybucję. Szczegóły: [LICENSE](LICENSE).
