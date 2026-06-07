# Notatki prowadzącego

## Przed wykładem

1. Uruchom `npm run serve`.
2. Otwórz `http://localhost:4173`.
3. Naciśnij `F`, aby wejść w pełny ekran.
4. Naciśnij `N`, aby sprawdzić notatki, a potem zamknij panel.
5. Przejdź do slajdu „Euler” i sprawdź przycisk eksperymentu.
6. Wróć `Home` na początek.

## Rytm

- Pierwsze 4 minuty: szybko, kontakt z salą, bez terminologii.
- Część techniczna: jedna metafora i jeden konkretny szczegół na slajd.
- Matematyka: zwolnić; cisza jest częścią wykładu.
- Część praktyczna: znów przyspieszyć i dać zdania gotowe do użycia.
- Finał: zwolnić, nie dopowiadać po ostatnim pytaniu.

## Skrócony skrypt

### 1-3. Hak i teza

Nie pytamy, czy AI jest „mądrzejsza”. Pytamy, w których czynnościach związanych
z myśleniem potrafi nas szybko i skutecznie wyręczyć. Kalkulator zmienił rachunki; modele
zmieniają także pisanie, szukanie wzorców i tworzenie procedur.

### 4-8. Jak działa GPT

Model dostaje tokeny i przewiduje kolejny token. Atencja pozwala każdemu tokenowi
ważyć informacje z kontekstu. Wiele warstw transformera buduje użyteczne,
rozproszone reprezentacje. Nie ma jednego „neuronu od Pitagorasa”.

### 9-10. Trening i matematyka

Pretrening uczy regularności. Posttrening kształtuje wykonywanie poleceń
i rozumowanie. Agent dodaje narzędzia oraz możliwość wielokrotnego sprawdzania pracy.
Matematyka jest wdzięczna, bo ma wyraźną strukturę i często szybko pokazuje błąd.

### 11-13. Przykłady

Gauss: dobra reprezentacja usuwa pracę. `0,999…=1`: różne dowody budują różne
intuicje. `1=2`: płynność lokalnych kroków nie gwarantuje poprawności globalnej.
Na końcu pokaż, jak Codex powinien przeprowadzić audyt: przeczytać założenie,
sprawdzić warunek każdej operacji i wskazać pierwszy niepoprawny krok.

### 14-15. Granice

Pewny ton nie jest certyfikatem. Przejdź do problemu szachownicy 8×8 i przyjmij
z sali szybkie odpowiedzi. „64” jest użytecznym błędem: liczy pola, nie prostokąty.
Pokaż zaznaczony prostokąt i zapytaj, co naprawdę go wyznacza. Codex łączy geometrię
z kombinatoryką, proponuje wybór dwóch linii pionowych i dwóch poziomych oraz program
sprawdzający. Człowiek doprecyzowuje, czy kwadraty także zaliczamy do prostokątów.

### 16-17. Codex i Euler

Kliknij symulację. Pierwsza wersja kodu zwraca `784`, bo liczy osiem linii zamiast
dziewięciu. Test `1×1` powinien dać jeden prostokąt, a daje zero. Codex poprawia
`range(n)` na `range(n+1)`, uruchamia testy `1×1`, `2×2`, `8×8` i uzyskuje `1296`.
Następnie wielomian Eulera pokazuje podobny schemat: kod znajduje `n=40`,
a matematyka wyjaśnia `1681=41²`.

### 18-21. Praktyka i finał

Odegraj rozmowę uczeń-Codex. Uczeń zaczyna od własnego błędu „64” i wyraźnie prosi,
by nie podawać wyniku. Codex pyta kolejno o dziewięć linii i liczbę ich par.
Na końcu uczeń stosuje tę samą metodę do planszy `10×10`, otrzymując
`C(11,2)²=3025`. Dobry prompt określa cel, kontekst, ograniczenia i kryterium
ukończenia.

## Awaryjne skrócenie do 25 minut

- Pominąć slajd z formalnym wzorem atencji.
- Pokazać tylko jedną drogę dla `0,999…=1`.
- Skrócić sondę i listę zasad.
- Zostawić Gaussa, fałszywy dowód, Codex/Euler i finał.

## Rozszerzenie do 45 minut

- Dodać pytania po każdej części.
- Przy atencji policzyć ręcznie trzy proste wagi.
- Przy Eulerze poprosić uczniów o wyjaśnienie `n=40`.
- Otworzyć dodatki o źródłach i pytaniach definicyjnych.
