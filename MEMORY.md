# Pamięć projektu

## Odbiorca i ton

- Uczniowie klas 7-8 i liceum, w tym grupy matematycznie zainteresowane.
- Lekko i żartobliwie, lecz bez infantylizacji i bez udawania pewności.
- Matematyka jest osią opowieści, nie dekoracją.
- Warto zachować więcej slajdów i świadomie pomijać moduły zależnie od grupy.

## Decyzje merytoryczne

- Tytuł pozostaje: **„Czy AI zastąpi naszą głowę?”**.
- AI może generować kandydatów na pomysły, ale nie gwarantuje ich nowości,
  znaczenia, prawdy ani wartości.
- Atencja to operacja algebraiczna. W GPT obowiązuje maska przyczynowa:
  `softmax((QK^T+M)/sqrt(d_k))V`.
- Pretrening i posttrening zmieniają parametry modelu. Rozmowa i agent opisują
  sposób użycia gotowego modelu.
- Agent typu Codex pracuje w pętli: czyta, planuje, działa, obserwuje wynik,
  sprawdza i poprawia.
- Eksperyment komputerowy sprawdza przypadki; dowód wyjaśnia ogół.
- Płynny język nie jest certyfikatem prawdy ani istnienia cytowanego źródła.

## Matematyka

- `0,999…` jest definiowane jako granica skończonych rozwinięć w liczbach rzeczywistych.
- Liczba prostokątów na planszy `m×k` wynosi
  `C(m+1,2)C(k+1,2)`; kwadraty są wliczane.
- Dla `f_p(n)=n²+n+p` zachodzi `f_p(p-1)=p²`.
- `1` nie jest ani liczbą pierwszą, ani złożoną.
- Małe twierdzenie Fermata:
  `p` pierwsza `=> a^p ≡ a (mod p)` dla każdego całkowitego `a`.
- Standardowy test `a^(n-1) ≡ 1 (mod n)` wymaga `NWD(a,n)=1` i nie jest
  wystarczającym testem pierwszości; `341=11·31` przechodzi go dla `a=2`.

## Profile i prowadzenie

- `core`: 22 slajdy, 35 minut.
- `math`: rdzeń plus Gauss, granica, Euler i Fermat.
- `full`: wszystkie slajdy matematyczne i techniczne.
- Nie ujawniać odpowiedzi przed pytaniem.
- Przy fałszywym dowodzie szukać pierwszego niedozwolonego przejścia.
- Przy prostokątach zaczynać od małego przypadku `2×3`.
- AI jako korepetytor ma zadawać jedno pytanie i dawać jedną wskazówkę naraz.
- Przed użyciem AI uczeń wykonuje zapisaną własną próbę przez 3-5 minut.

## Serwis

- Polska prezentacja jest źródłem kanonicznym; generator EN ma kończyć się błędem,
  jeśli nie zna tłumaczenia lub pozostawi polski tekst.
- Pięć laboratoriów działa lokalnie i ma wersje PL/EN oraz treść `noscript`.
- Landing page prowadzi bezpośrednio do każdego laboratorium.
- Wszystkie publiczne strony zawierają:
  `Copyright © 2026 Bartosz Naskręcki. All rights reserved.`
- Publikacja: publiczne repozytorium GitHub, gałąź `main`, katalog główny.

## Grafiki

- `assets/hero-human-ai.png`
- `assets/attention-party.png`
- `assets/idea-garden.png`
- `assets/site-qr.svg`
