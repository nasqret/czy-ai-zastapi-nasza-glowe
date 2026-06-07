# Plan wykładu i projektu

## Cel

Przygotować lekki, błyskotliwy i matematycznie uczciwy wykład dla uczniów klas
7-8 oraz liceum. Uczniowie mają po nim:

- rozumieć intuicję przewidywania tokenów, atencji, treningu i pracy agenta;
- wiedzieć, dlaczego matematyka daje AI wyjątkowo dobrą informację zwrotną;
- odróżniać płynność odpowiedzi, eksperyment obliczeniowy i dowód;
- umieć użyć AI jako korepetytora, krytyka i narzędzia do testowania;
- zachować odpowiedzialność za założenia, sprawdzenie i znaczenie wyniku.

## Architektura

| Profil | Zawartość | Przeznaczenie |
|---|---|---|
| `core` | 22 slajdy, 35:00 | standardowy wykład |
| `math` | rdzeń + 6 slajdów | klasa matematyczna lub dłuższe spotkanie |
| `full` | rdzeń + matematyka + 4 slajdy techniczne | grupa zaawansowana |
| dodatki | źródła i ściąga | pytania po wykładzie |

Slajdy opcjonalne pozostają w logicznych miejscach narracji i są oznaczone.

## Rdzeń 35 minut

1. Tytuł, sonda i nieabsolutna teza.
2. Przewidywanie tokenu oraz intuicja ważenia kontekstu.
3. Pretrening, posttrening, generowanie i agent.
4. Dlaczego matematyka daje strukturę, testy i informację zwrotną.
5. Pętla pracy agenta typu Codex oraz granice generowania pomysłów.
6. Fałszywy dowód, audyt pierwszego błędu i zasada „płynność ≠ prawda”.
7. Prostokąty na planszy `m×k`: hipoteza, kod, testy i dowód wzoru.
8. AI jako korepetytor, dobry prompt i pięć pytań kontrolnych.
9. Własna próba przez 3-5 minut i zasady używania AI w szkole.
10. Materiały do dalszej pracy i finał o odpowiedzialności.

## Moduły opcjonalne

- techniczne: tokenizacja, `Q/K/V`, maska przyczynowa i stos transformera;
- matematyczne: Gauss, `0,999…`, Euler oraz małe twierdzenie Fermata;
- dodatki: bibliografia i trzy rozróżnienia do pytań z sali.

## Kryteria ukończenia

- obie lokalizacje mają identyczną strukturę i naturalny język;
- profil `core` ma dokładnie 22 slajdy i 2100 sekund;
- wszystkie wzory i przykłady przechodzą automatyczną kontrolę;
- każde laboratorium działa w PL i EN, także z sensowną treścią bez JavaScriptu;
- na każdym pokazie widoczna jest różnica między przypadkiem sprawdzonym przez
  komputer a argumentem matematycznym;
- prezentacja nie ma przepełnień w typowych rozdzielczościach;
- publiczna strona GitHub Pages zawiera landing page, slajdy, źródła i laboratoria.
