# Plan dużej przebudowy po audycie GPT Pro

## Założenie

Prezentacja pozostaje matematyczna i techniczna, ale otrzymuje trzy jawne ścieżki:

- **rdzeń**: 22 slajdy i dokładnie 35 minut;
- **matematyka**: rdzeń plus Gauss, `0,999…`, Euler i Fermat;
- **pełna**: rdzeń, matematyka oraz techniczne szczegóły transformera.

Slajdy opcjonalne pozostają w miejscu wynikającym z narracji. Prowadzący może
zmienić ścieżkę z poziomu prezentacji albo otworzyć konkretny slajd przez adres URL.

## Narracja

1. Tytuł, anonimowa sonda i nieabsolutna teza.
2. Przewidywanie kolejnego tokenu i intuicja ważenia kontekstu.
3. Opcjonalny moduł techniczny: tokenizacja, macierze Q/K/V, maska przyczynowa
   i warstwy transformera.
4. Pretrening, posttrening, rozumowanie podczas generowania i agent z narzędziami.
5. Dlaczego matematyka daje modelom i agentom wyjątkowo dobrą informację zwrotną.
6. Pętla pracy agenta typu Codex oraz granice generowania pomysłów.
7. Opcjonalne przykłady: Gauss i `0,999…=1`.
8. Rdzeń matematyczny: fałszywy dowód, audyt pierwszego błędu i płynność różna od prawdy.
9. Studium przypadku prostokątów na planszy `m×k`, program, małe testy i dowód wzoru.
10. Opcjonalny moduł Eulera: eksperyment, klasyfikacja `1` i wyjaśnienie `f_p(p-1)=p²`.
11. AI jako korepetytor, dobry prompt i pięć pytań kontrolnych.
12. Zasada własnej próby przez 3–5 minut oraz reguły używania AI w szkole.
13. Opcjonalny moduł Fermata z jawnym warunkiem względnej pierwszości.
14. Widoczny adres/QR do slajdów, źródeł i laboratoriów oraz finał.

## Zmiany merytoryczne

- Zmniejszenie antropomorfizacji modelu i mechanizmu uwagi.
- Uzupełnienie wzoru uwagi o maskę przyczynową `M`.
- Rozdzielenie treningu, generowania odpowiedzi i działania agenta.
- Jawne rozróżnienie: kandydat na pomysł, nowość, wartość, prawda i intuicja.
- Definicja `0,999…` jako granicy w liczbach rzeczywistych.
- Uogólnienie prostokątów do `C(m+1,2)C(k+1,2)`.
- Jawna para na pokazach: „komputer sprawdził przypadek” / „matematyka wyjaśnia ogół”.
- Klasyfikacja wyników Eulera jako pierwsza, złożona albo ani jedna, ani druga.
- Standardowy test Fermata `a^(n-1) ≡ 1 (mod n)` z `gcd(a,n)=1`.
- Jedna pozamatematyczna ilustracja płynnej, lecz fałszywej odpowiedzi.

## Laboratoria

- Prostokąty: dwa wymiary, małe testy i wzór ogólny.
- Fermat: widoczny warunek NWD oraz znaczenie pseudopierwszości.
- Euler: poprawna obsługa `1` i algebraiczne wyjaśnienie wyniku.
- Audyt dowodu: stopniowane wskazówki, reset i osobne ujawnienie odpowiedzi.
- Prompt Dojo: matematyka, historia, biologia, literatura i programowanie.
- Wszystkie: `aria-live`, dostępne opisy wzorów, treść `noscript` i rozróżnienie
  eksperymentu od dowodu.

## Dostępność i testy

- Zgodna struktura PL/EN i identyczne profile slajdów.
- Test dokładnie 22 slajdów rdzenia i czasu `35:00`.
- Test pełnej talii oraz profili `core`, `math`, `full`.
- Test Eulera dla `c=1`.
- Test planszy prostokątnej.
- Test warunku `gcd(a,n)=1` w laboratorium Fermata.
- Test pięciu bezpośrednich kart laboratoriów.
- Test sklejonych zdań w tekście dostępnym.
- Test `noscript`, etykiet formularzy, `aria-live` i klawiatury.
- Test wizualny obu języków w trzech rozdzielczościach.
