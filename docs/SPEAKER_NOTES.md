# Notatki prowadzącego

## Przed wykładem

1. Uruchom `npm run serve`.
2. Otwórz `http://127.0.0.1:4173/pl/?track=core`.
3. Sprawdź profil w prawym górnym rogu: `Rdzeń 35 min`.
4. Naciśnij `F`, a następnie `N`, aby sprawdzić pełny ekran i notatki.
5. Uruchom symulację prostokątów.
6. Dla profilu `math` sprawdź pokazy Eulera i Fermata.
7. Sprawdź kod QR na slajdzie „Materiały”.

## Rytm rdzenia

- 0-3 min: tytuł, anonimowa sonda, teza bez prognoz rynku pracy.
- 3-8 min: następny token i mechanizm uwagi.
- 8-14 min: trening, matematyka, agent i granice idei.
- 14-20 min: zagadka `1=2`, audyt i płynność kontra prawda.
- 20-26 min: prostokąty `m×k`, błąd programu, testy i argument ogólny.
- 26-32 min: korepetytor, prompt, pytania kontrolne i własna próba.
- 32-35 min: zasady szkolne, materiały i finał.

## Najważniejsze momenty

### Atencja

Metafora „słuchania” ma pomóc, ale od razu dopowiedz: to mnożenie macierzy,
softmax i ważona suma, nie świadoma uwaga. W module technicznym pokaż maskę `M`.

### Trening

Rozdziel cztery rzeczy: pretrening, posttrening, dodatkowe kroki podczas
generowania oraz agent z narzędziami. Rozmowa zwykle nie doucza modelu na żywo.

### Fałszywy dowód

Najpierw pokaż tylko zagadkę. Poproś o numer pierwszego błędnego przejścia
i warunek potrzebny do jego wykonania. Dopiero na następnym slajdzie pokaż,
że `a-b=0`, więc skrócenie oznacza dzielenie przez zero.

### Prostokąty

Zacznij od planszy `2×3`. Każdy prostokąt wybiera dwie z `m+1` linii poziomych
i dwie z `k+1` pionowych. Symulacja pokazuje błąd „o jeden”; program sprawdza
przypadki, a bijekcja między parami linii i prostokątami uzasadnia wzór.

### Korepetytor

Uczeń pokazuje własną próbę i zakazuje podawania całego rozwiązania. AI zadaje
jedno pytanie, daje jedną wskazówkę i czeka. Sukcesem jest samodzielne rozwiązanie
nowego wariantu, nie samo uzyskanie odpowiedzi.

## Moduły matematyczne

- Gauss: zmiana reprezentacji ujawnia symetrię.
- `0,999…`: nieskończony zapis oznacza granicę.
- Euler: komputer znajduje `n=40`, algebra pokazuje `f_p(p-1)=p²`.
- Fermat: rozdziel twierdzenie od testu; pokaż `NWD(a,n)=1` oraz `341=11·31`.

## Warianty czasu

- 25 minut: profil `core`, skrócić sondę, trening i zasady szkolne; nie usuwać
  fałszywego dowodu ani prostokątów.
- 45 minut: profil `math`; wybrać Euler albo Fermat jako główny moduł.
- 55-60 minut: profil `full`; dodać tokenizację, wzór uwagi, maskę i pytania.
