# Pamięć projektu

## Odbiorca i ton

- Odbiorcy: uczniowie klas 7-8 i liceum, bez wymaganego przygotowania technicznego.
- Języki: polski i angielski, lekko, bez infantylizacji.
- Humor ma wynikać z trafnych metafor i kontrastów, nie z memów wymagających
  znajomości bieżącego internetu.
- Główna ambicja: połączyć rozrywkę z uczciwością epistemiczną.

## Decyzje merytoryczne

- Nie używać absolutnego stwierdzenia „AI nie generuje idei”.
- Mówić: AI tworzy propozycje, łączy pomysły i bada możliwości, ale ma problem z oceną
  nowości, znaczenia, kosztu i długofalowej wartości.
- Nie antropomorfizować mechanizmu atencji. To obliczanie wag zależności, nie
  świadome skupianie uwagi.
- Nie sugerować, że współczesne modele ujawniają pełny skład danych treningowych
  lub kompletną recepturę posttreningu.
- Nie utożsamiać eksperymentu obliczeniowego z dowodem.
- Agent korzystający z narzędzi nie jest „trzecim etapem treningu”. Pretrening
  i posttrening uczą model; agent to sposób użycia gotowego modelu w pętli działań.
- Codex przedstawiać jako agenta pracującego w cyklu: kontekst, plan, działanie,
  test, poprawka, przegląd.
- Symulowane okna Codexa trzeba nazywać symulacją, a nie zapisem prawdziwej sesji.

## Konwencja wizualna

- Paleta: granat `#061b35`, krem `#f6ebce`, koral `#ff654d`,
  cyjan `#2db9da`, żółty `#ffc64b`.
- Styl: retrofuturystyczna ilustracja redakcyjna, faktura sitodruku,
  nocna tablica / laboratorium idei.
- Obrazy są dodatkiem do narracji; diagramy techniczne są kodowane w HTML/CSS,
  aby pozostały ostre i łatwe do zmiany.
- Brak zewnętrznych zależności, fontów sieciowych i odtwarzanych filmów.

## Serwis publiczny

- Landing page pod `/` pozwala wybrać wersję polską lub angielską.
- Kanonicznym źródłem prezentacji jest `pl/index.html`; wersję angielską generuje
  `scripts/build_english_presentation.py`.
- Codex Math Lab zawiera pięć dwujęzycznych eksperymentów: prostokąty, test
  Fermata, wielomian Eulera, audyt fałszywego dowodu i prompt dojo.
- Wszystkie eksperymenty liczą lokalnie. Nie należy dodawać kluczy API ani
  sugerować, że symulowany terminal jest zapisem prawdziwej sesji.
- Publikacja GitHub Pages korzysta z gałęzi `main` i katalogu głównego.
- Każda publiczna strona zawiera:
  `Copyright © 2026 Bartosz Naskręcki. All rights reserved.`

## Zasady prowadzenia

- Ujawniać elementy pojedynczo; nie pokazywać odpowiedzi przed pytaniem.
- Po pytaniach matematycznych zostawić realną ciszę.
- Przy wzorze atencji nie robić wyprowadzenia. Wyjaśnić Q/K/V.
- Przy slajdzie 1=2 szukać „pierwszego nielegalnego ruchu”.
- Finał nie jest prognozą rynku pracy, lecz pytaniem o osobistą odpowiedzialność.
- Slajdy 15, 16 i 18 tworzą jedno studium przypadku: liczenie prostokątów
  na szachownicy 8×8. Najpierw pomysł, potem kod i testy, na końcu rozmowa ucznia
  z Codexem bez podawania gotowej odpowiedzi.
- Slajd 21 przekłada wszystkie pięć zasad ze slajdu 20 na jeden eksperyment:
  uczeń stawia hipotezę o `2^p-2`, prosi Codex o kontrprzykład, sprawdza wynik
  programem, nie przekazuje prywatnych danych i kończy samodzielnym rachunkiem
  `3^100 mod 7 = 4`.
- W zabawie z Fermatem trzeba wyraźnie rozdzielić prawdziwe twierdzenie
  `p` pierwsza `⇒ a^p ≡ a (mod p)` dla każdego całkowitego `a` od testu
  pierwszości opartego na jednej podstawie. Liczba `341 = 11·31` pokazuje,
  że warunek `341 | 2^341−2` nie wystarcza do stwierdzenia pierwszości.
- Dane autora na slajdzie tytułowym: Bartosz Naskręcki, UAM/CCAI,
  Warszawa, 8.06.2026.

## Grafiki

Wbudowane narzędzie `imagegen` utworzyło trzy ilustracje bez tekstu:

- `assets/hero-human-ai.png`
- `assets/attention-party.png`
- `assets/idea-garden.png`

Oryginały pozostają również w katalogu generowanych obrazów Codex. Grafiki projektu
mają format 1672×941, czyli proporcje bliskie 16:9.
