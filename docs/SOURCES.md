# Źródła i zastrzeżenia

Stan materiałów produktowych OpenAI: **7 czerwca 2026**.

Punktem wyjścia do dużej przebudowy był również lokalny dokument
[`sources/ai_presentation_critical_audit.md`](../sources/ai_presentation_critical_audit.md).
Jego zalecenia zostały zweryfikowane matematycznie i przełożone na plan
[`REVAMP_PLAN.md`](../REVAMP_PLAN.md).

## Mechanizm modeli

1. Ashish Vaswani i in., [Attention Is All You Need](https://arxiv.org/abs/1706.03762),
   2017. Pierwotna praca o architekturze Transformer i mechanizmie atencji.
2. Tom B. Brown i in.,
   [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165),
   2020. Opis autoregresyjnego modelowania języka na dużą skalę.
3. Long Ouyang i in.,
   [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155),
   2022. Klasyczny opis instruktażowego dostrajania i informacji zwrotnej od ludzi.

## Rozumowanie i matematyka

4. Hunter Lightman i in.,
   [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050),
   2023. Praca o nadzorze procesu rozumowania matematycznego.
5. OpenAI,
   [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/),
   2024. Publiczny opis modeli uczonych wzmacnianiem do rozumowania.
6. OpenAI,
   [Advancing science and math with GPT-5.2](https://openai.com/index/gpt-5-2-for-science-and-math/),
   2025. Przykłady współpracy ekspertów z modelem w badaniach matematycznych
   i naukowych. Traktowane jako studia przypadków, nie dowód autonomicznej nauki.

## Codex

7. OpenAI, [Codex](https://developers.openai.com/codex/).
8. OpenAI, [Codex best practices](https://developers.openai.com/codex/learn/best-practices).
9. OpenAI, [Codex prompting](https://developers.openai.com/codex/prompting).
10. OpenAI, [Codex manual](https://developers.openai.com/codex/codex-manual.md).

Wykład korzysta z aktualnego oficjalnego opisu Codex jako agenta, który może
czytać kod, wykonywać działania, uruchamiać testy i przeglądać wynik. Dobre
praktyki podkreślają cztery elementy polecenia: cel, kontekst, ograniczenia
i kryterium ukończenia. Podręcznik sprawdzono ponownie 7 czerwca 2026.

## Ważne zastrzeżenia

- Slajdy upraszczają architekturę. Współczesne modele mogą zawierać dodatkowe
  mechanizmy niewidoczne na schemacie „tokeny → transformer → token”.
- Mechanizm atencji nie jest świadomą uwagą.
- W autoregresyjnym GPT pojedyncza głowa uwagi używa maski przyczynowej `M`,
  która blokuje dostęp do przyszłych pozycji.
- Publiczne materiały nie ujawniają pełnego składu danych ani wszystkich etapów
  treningu najnowszych modeli. Slajd o treningu opisuje publicznie znane klasy
  metod, a nie kompletną recepturę konkretnego modelu.
- Wyniki benchmarków szybko się starzeją, dlatego wykład nie opiera argumentu
  na jednym procencie ani rankingu.
- Wygenerowanie kontrprzykładu lub wykonanie obliczeń nie jest samo w sobie
  dowodem matematycznym.
- Test Fermata `a^(n-1) ≡ 1 (mod n)` jest stosowany przy `NWD(a,n)=1`;
  jego przejście nie dowodzi, że `n` jest pierwsza.
- Pretrening i posttrening są etapami uczenia modelu. Korzystanie z plików,
  kodu i testów przez agenta opisuje sposób użycia modelu, a nie kolejny etap treningu.

## Ilustracje

Trzy grafiki utworzono wbudowanym generatorem obrazów Codex w konwencji
retrofuturystycznej ilustracji redakcyjnej. Prompty wymagały braku tekstu,
logotypów i znaków wodnych oraz wspólnej palety granat/krem/koral/cyjan/żółty.
