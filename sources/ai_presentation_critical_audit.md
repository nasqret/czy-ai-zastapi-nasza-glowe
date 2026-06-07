# Critical flaws and improvement suggestions  
## Presentation: “Czy AI zastąpi naszą głowę?” / “Will AI replace our minds?”

**Reviewed URL:** https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/  
**Audience stated in project materials:** grades 7–8 and high school students  
**Format stated on landing page:** 35 minutes, 22 main slides in Polish and English  
**Review date:** 2026-06-07

---

## Scope and method

I reviewed:

- the public landing page;
- the Polish and English slide decks;
- the JavaScript-defined “Codex Math Lab” examples linked from the landing page;
- the repository README, plan, memory notes, sources, speaker notes, and test suite;
- current official OpenAI Codex / prompting references for context around product-specific claims.

Where the lab content is JavaScript-rendered, I audited the source that defines the clickable lab behavior and the tests that exercise the pages. I focused on critical flaws: issues that could cause student misconceptions, factual/math errors, failed classroom flow, accessibility barriers, or misleading expectations about AI use.

---

## Executive summary

The presentation has a strong core: it avoids both panic and hype, uses mathematics to show why “fluent” is not the same as “true,” and repeatedly frames AI as a tool that should be checked rather than obeyed. The best parts are the false proof, rectangle-counting, tutor dialogue, and “mental hygiene” rules.

The main critical problems are:

1. **Too much conceptual load for 35 minutes.** The deck covers next-token prediction, tokenization, attention, transformers, training, agents, proof checking, several mathematical examples, prompting, Codex, Fermat tests, and ethics/rules. For most high-school audiences this is too dense for one session.
2. **The landing page and lab hub are inconsistent.** The landing page advertises four numbered lab cards, while the project source and tests define five labs. Prompt Dojo is effectively hidden behind the lab hub instead of surfaced as its own card.
3. **The Euler lab has a real mathematical edge-case bug.** For `c = 1`, the expression at `n = 0` is `1`, which is neither prime nor composite, but the current code treats non-prime as composite and reports it as a composite counterexample.
4. **The Fermat lab hides a key mathematical condition.** The code filters to `gcd(a, n) = 1`, but the slide/lab framing mostly says “test `a^n ≡ a (mod n)`.” Students may miss the role of coprimality and mistake a computational filter for the theorem.
5. **The AI-product framing is too Codex-specific for a general school audience.** Codex is useful as an example, but many students will use other tools. The transferable idea should be “agentic AI can inspect, edit, and test work,” not “Codex is the method.”
6. **Missing school-use safeguards.** The deck should explicitly cover disclosure, teacher policy, personal data, exam/assignment rules, and “do not paste private or copyrighted material.” This matters more than another technical slide.
7. **Several phrases risk anthropomorphizing the model.** “Thinking machine,” “each token asks whom should I listen to,” and similar wording are memorable but can reinforce exactly the misconception the deck tries to avoid.
8. **Accessibility and no-JavaScript robustness need attention.** The lab wrappers are empty without JavaScript, terminal updates likely need live-region semantics, formulas need screen-reader-friendly alternatives, and several extracted strings show missing spaces.
9. **The source appendix is present but underused.** For students, a source slide at the end is not enough. Provide a visible QR/short link and distinguish stable concepts from fast-changing product/benchmark claims.

---

## Priority fixes

### P0 — Fix before presenting again

#### 1. Correct the Euler lab’s treatment of `1`

**Problem**  
The Euler lab searches for the first `n` such that `n² + n + c` is not prime and labels that value as “composite.” The current source uses a condition equivalent to `if (!isPrime(value))`, so `1` is treated as a composite value. With `c = 1` and `n = 0`, the lab can report `1` as a composite counterexample.

**Why it matters**  
This is exactly the kind of mistake the presentation teaches students to catch: “non-prime” does not mean “composite.” If the demo makes that mistake, it undermines the credibility of the mathematical message.

**Suggested fix**

Use an explicit classification:

```js
function classifyInteger(n) {
  if (n < 2n) return "unit-or-neither";
  return isPrime(n) ? "prime" : "composite";
}
```

Then in the Euler lab:

```js
const status = classifyInteger(value);
if (status === "composite") {
  // report composite counterexample
}
```

For `status === "unit-or-neither"`, show:

> `1` is neither prime nor composite. The polynomial already fails to produce primes, but this is not a composite counterexample.

Also add a test case:

```text
c = 1 should not display “1 is composite”.
```

---

#### 2. Make the landing page, hub, README, and tests agree about the labs

**Problem**  
The landing page shows four numbered examples:

1. rectangle hunting;
2. pseudoprime hunting;
3. Euler laboratory;
4. proof audit and prompt dojo.

But the project source, README, and tests define five labs:

1. rectangles;
2. Fermat/pseudoprimes;
3. Euler;
4. proof audit;
5. prompt dojo.

**Why it matters**  
This is a navigation and expectation failure. Students and teachers see “four examples” on the landing page, then the hub exposes five labs. The Prompt Dojo is pedagogically important but visually demoted.

**Suggested fix**

On the landing page, show five cards and link each card directly:

1. `Polowanie na prostokąty` / `Rectangle hunt`;
2. `Łowca pseudopierwszych` / `Pseudoprime hunter`;
3. `Laboratorium Eulera` / `Euler laboratory`;
4. `Audyt dowodu` / `Proof audit`;
5. `Prompt dojo`.

Keep the hub link as a secondary “all labs” option. The main landing page should not require students to enter the hub first.

---

#### 3. Add a school-policy, privacy, and disclosure slide

**Problem**  
The deck gives good intellectual rules, but it does not make the classroom rules explicit enough. Students need practical boundaries:

- when AI use must be disclosed;
- whether AI is allowed on this assignment;
- whether a teacher expects original attempts first;
- what not to paste into a model;
- how to cite or describe AI assistance;
- what to do in exams, contests, and graded homework.

**Why it matters**  
For high-school students, the immediate risk is not only “AI is wrong.” It is “I used AI in a way my school considers dishonest or unsafe.” This should be a first-class slide, not a footnote.

**Suggested fix**

Add a slide after the tutor dialogue or before the final rules:

### AI use in school: five non-negotiables

1. **Follow the assignment rules.** If the teacher says no AI, do not use it.
2. **Disclose help when required.** Write what the tool helped with: idea, hint, code, wording, checking.
3. **Do not paste private data.** No names, grades, medical details, addresses, family problems, private chats.
4. **Do not outsource the learning target.** If the task is to learn a proof, do not ask for a final proof first.
5. **Keep your draft trail.** Save your own first attempt, AI suggestions, and final corrected version.

Polish version:

### AI w szkole: pięć zasad

1. **Stosuj zasady zadania.** Jeśli nauczyciel mówi „bez AI”, nie używaj AI.
2. **Ujawnij pomoc, gdy trzeba.** Napisz, w czym narzędzie pomogło: pomysł, wskazówka, kod, styl, sprawdzenie.
3. **Nie wklejaj danych prywatnych.** Bez nazwisk, ocen, zdrowia, adresów, rodzinnych spraw i prywatnych rozmów.
4. **Nie oddawaj celu nauki maszynie.** Jeśli celem jest nauczyć się dowodu, nie zaczynaj od gotowego dowodu.
5. **Zachowaj ślad pracy.** Własna próba → pomoc AI → twoja poprawiona wersja.

---

#### 4. Reduce the technical section or split it into a main track and optional appendix

**Problem**  
Slides 4–9 cover next-token prediction, tokenization, attention, transformer blocks, pretraining/post-training, agents, tool use, and Codex. This is a lot before the core student takeaway begins.

**Why it matters**  
Many students will remember isolated words — “tokens,” “attention,” “transformer” — without a usable mental model. The deck risks teaching vocabulary instead of judgment.

**Suggested fix**

For the 35-minute version, keep only:

- next-token prediction in one example;
- attention as “the model weighs relevant parts of the context”;
- “training changes the model; chatting or agent work usually does not”;
- “agents can use tools, read files, run tests, and still need supervision.”

Move the exact attention formula and transformer internals to an optional appendix. Use the formula only if the audience is mathematically advanced and there is time.

---

#### 5. Clarify the Fermat/pseudoprime demo

**Problem**  
The lab code searches for composite `n` satisfying the congruence while also requiring `gcd(a, n) = 1`. The slide/lab wording does not make that restriction central.

**Why it matters**  
The mathematical lesson depends on careful conditions. If students see a counterexample hunt but do not see the conditions, they may learn the wrong theorem.

**Suggested fix**

Use consistent variables:

- Let `p` mean “a prime.”
- Let `n` mean “a candidate number, possibly composite.”
- Let `a` be the base.

Recommended wording:

> Fermat says: if `p` is prime and `gcd(a, p) = 1`, then `a^(p−1) ≡ 1 (mod p)`.  
> A Fermat pseudoprime to base `a` is a composite `n` with `gcd(a, n) = 1` that still passes the same test.

If you want to use the equivalent `a^n ≡ a (mod n)` version, explicitly say it is equivalent under the coprime condition for the usual Fermat test framing, and keep the UI consistent.

---

### P1 — Strongly recommended before a classroom delivery

#### 6. Stop calling the model a “thinking machine” unless you immediately deconstruct the phrase

**Problem**  
The opening subtitle says the talk is “a short instruction for collaborating with a thinking machine.” This is catchy, but for students it can reinforce the idea that the system thinks like a person.

**Why it matters**  
The deck’s thesis depends on separating fluency, agency, and truth from human understanding. Anthropomorphic language makes that harder.

**Suggested fix**

Replace:

> machine for thinking / maszyna do myślenia

with one of:

> a tool for working with thinking tasks  
> narzędzie do pracy nad zadaniami wymagającymi myślenia

or:

> a prediction system that can help us think — if we verify it  
> system przewidujący tekst, który może pomagać w myśleniu — jeśli go sprawdzamy

A good compromise:

> I will sometimes say “thinking machine” as shorthand. But today’s first rule is: it does not think like a person.

---

#### 7. Rephrase attention without personification

**Problem**  
The slide says each token asks something like “whom should I listen to?” The explanation is vivid but suggests intention.

**Why it matters**  
Students often over-attribute understanding and motives to AI systems. The slide can avoid this without becoming dry.

**Suggested fix**

Replace:

> Each token asks: whom should I listen to?

with:

> The model assigns weights to other tokens: which earlier pieces of context are most useful for the next prediction?

Polish:

> Model przypisuje wagi innym tokenom: które wcześniejsze fragmenty kontekstu są najbardziej przydatne do następnego przewidywania?

Also avoid using **atencja** as the main Polish term. Use:

> mechanizm uwagi / ważenia zależności (*attention*)

---

#### 8. Add a transfer slide: “This is not only about Codex”

**Problem**  
Codex is a strong demo vehicle, but many students will not have access to it, and the product can change. The presentation should emphasize transferable habits.

**Why it matters**  
Students need methods they can use with whatever tool their school permits. Product-specific demos age quickly.

**Suggested fix**

Add a small bridge slide:

### What transfers to any AI tool?

- Ask for **questions**, not just answers.
- Ask it to **show assumptions**.
- Ask it to **test edge cases**.
- Ask it to **separate calculation from proof**.
- Ask it to **say what would change its answer**.
- Verify with your own reasoning, teacher, textbook, or code.

Polish:

### Co działa w każdym narzędziu AI?

- Proś o **pytania**, nie tylko o odpowiedzi.
- Proś o **założenia**.
- Proś o **przypadki brzegowe**.
- Oddziel **rachunek od dowodu**.
- Zapytaj: **co zmieniłoby tę odpowiedź?**
- Sprawdź samodzielnie, z nauczycielem, podręcznikiem albo kodem.

---

#### 9. Make the “fluency ≠ truth” slide more general

**Problem**  
The message is correct, but most examples are mathematical. Some students may think the warning applies only to math.

**Why it matters**  
The same failure mode occurs in history, biology, law, current events, citations, and personal advice.

**Suggested fix**

Add one non-math example:

> A model can invent a convincing quote, a fake source, or a plausible date. The sentence can sound perfect and still be false.

Polish:

> Model może wymyślić przekonujący cytat, fałszywe źródło albo wiarygodnie brzmiącą datę. Zdanie może brzmieć idealnie i nadal być fałszywe.

---

#### 10. Make “try first” operational

**Problem**  
The final hygiene rules are good but abstract. “Try first” needs a concrete threshold.

**Why it matters**  
Students often do not know what “try” means. One minute of staring is not the same as a real attempt.

**Suggested fix**

Change the rule to:

> Before asking AI, write for 3–5 minutes: what you know, what you tried, where you got stuck.

Polish:

> Zanim zapytasz AI, pisz przez 3–5 minut: co wiesz, czego próbowałeś/próbowałaś, gdzie utknąłeś/utknęłaś.

Then give the AI the stuck point, not the whole assignment.

---

#### 11. Strengthen the tutor-dialogue slide

**Problem**  
The tutor example is one of the best slides, but the prompt can be made safer and more teachable.

**Suggested replacement prompt**

English:

> I am learning this topic. Do not solve the whole task.  
> First ask me one diagnostic question.  
> Then give one hint based on my answer.  
> Stop after each hint and wait.  
> Here is my attempt: …

Polish:

> Uczę się tego tematu. Nie rozwiązuj całego zadania.  
> Najpierw zadaj mi jedno pytanie diagnostyczne.  
> Potem daj jedną wskazówkę na podstawie mojej odpowiedzi.  
> Zatrzymaj się po każdej wskazówce i poczekaj.  
> Oto moja próba: …

---

#### 12. Do not let the proof-audit lab reveal the answer too early

**Problem**  
The current proof lab appears to reveal the key condition even if the student chooses the wrong step. That makes the lab less diagnostic.

**Why it matters**  
The point is to train careful proof reading, not just reveal “division by zero.”

**Suggested fix**

Use staged feedback:

- first wrong attempt: “This step is suspicious later, but not the first invalid step. Try again.”
- second wrong attempt: “Look for the first operation that assumes something about `a − b`.”
- correct attempt or final reveal: “Since `a = b`, we have `a − b = 0`; division by zero is not allowed.”

Add a “reveal answer” button for teachers.

---

#### 13. Fix text spacing issues in the slide DOM

**Problem**  
The extracted Polish and English slide text shows missing spaces in several places, for example:

- `GOTOWE, GDY…Co`
- `Najpierw spróbuj sam.Zapisz`
- `Try first.Write`
- `Check fluency?No`

These may be invisible or less obvious visually but problematic for copying, screen readers, and search.

**Suggested fix**

Insert literal spaces or line breaks in the HTML between inline elements. Add a text-extraction test that fails on common patterns:

```text
[a-ząęćłńóśźż]\.[A-ZĄĘĆŁŃÓŚŹŻ]
[a-z]\?[A-Z]
…[A-Z]
```

---

### P2 — Improvements that will noticeably improve learning

#### 14. Split the audience track

**Problem**  
Project notes target both grades 7–8 and high school. That is a wide span.

**Why it matters**  
The attention formula, Fermat pseudoprimes, and Euler polynomials can work for older or stronger students, but they may overload younger students.

**Suggested fix**

Create two visible paths:

- **Core version:** grades 7–8 / general high school.
- **Advanced version:** math-profile high school students.

Core version should omit the attention formula and either Fermat or Euler. Advanced version can keep the formula and both number theory labs.

---

#### 15. Shorten the number of mathematical examples in the live talk

**Problem**  
The deck includes Gauss, `0.999… = 1`, a false proof, rectangles, Euler, tutor dialogue, and Fermat.

**Why it matters**  
All examples are defensible individually. Together, they compete for attention.

**Suggested 35-minute flow**

1. Hook and poll — 3 minutes.
2. One model explanation — 5 minutes.
3. False proof — 5 minutes.
4. Rectangle counting with AI/debugging — 8 minutes.
5. Tutor dialogue and prompting — 7 minutes.
6. AI school rules and finale — 5 minutes.
7. Questions or one optional lab — 2 minutes.

Move Gauss, `0.999…`, Euler, and Fermat into optional “choose one” modules.

---

#### 16. Make the rectangle lab handle rectangular boards, not just square boards

**Problem**  
The slide says “every board,” but the lab uses an `n × n` board. The full result is more general and still accessible.

**Suggested fix**

Add two inputs: width `m` and height `k`.

Formula:

```text
number of axis-aligned rectangles in an m × k grid of cells
= C(m + 1, 2) × C(k + 1, 2)
```

For a square `n × n` board, this becomes:

```text
C(n + 1, 2)^2
```

Also explicitly state whether squares count as rectangles.

---

#### 17. Make the “computation vs proof” distinction visible in every lab

**Problem**  
The deck says this in speaker notes and sources, but students need it on screen.

**Suggested recurring label**

For each lab output, add:

```text
Computer found: an example / no example in this range.
Mathematics still needs: a proof / a reason why.
```

Polish:

```text
Komputer znalazł: przykład / brak przykładu w tym zakresie.
Matematyka nadal potrzebuje: dowodu / powodu dlaczego.
```

---

#### 18. Add a “bad prompt → better prompt” before Prompt Dojo

**Problem**  
Prompt Dojo asks students to construct a good prompt but does not first show the contrast sharply enough.

**Suggested micro-example**

Bad:

> Solve this.

Better:

> I am learning, not submitting. Ask me one question first. Then give one hint. Do not give the final answer until I show my attempt. Check edge cases at the end.

Polish:

> Uczę się, nie oddaję gotowca. Najpierw zadaj mi jedno pytanie. Potem daj jedną wskazówkę. Nie podawaj końcowej odpowiedzi, dopóki nie pokażę próby. Na końcu sprawdź przypadki brzegowe.

---

#### 19. Add non-math prompt examples

**Problem**  
The talk is math-heavy. Some students may not see how the habits apply to other subjects.

**Suggested examples**

History:

> Ask me questions that help me compare two causes of an event. Do not write the essay.

Biology:

> Check whether my explanation confuses correlation and causation. Ask one question first.

Literature:

> Help me find evidence in the text. Do not invent quotes.

Polish equivalents should be included on the Polish lab page or in a language toggle.

---

#### 20. Add a source/QR slide before the finale, not only in the appendix

**Problem**  
The source appendix is useful but easy to skip.

**Why it matters**  
A talk about checking sources should model source-checking visibly.

**Suggested fix**

Add a near-final slide:

> Slides, sources, and labs: [short URL / QR code]  
> Stable idea: verify claims.  
> Fast-changing part: exact product features and benchmarks.

---

## Slide-by-slide critical notes

### Slide 1 — Title and promise

**Issue:** “machine for thinking” / “thinking machine” is engaging but anthropomorphic.  
**Fix:** Use “tool for working with thinking tasks” or explicitly say the phrase is shorthand and will be questioned.

### Slide 2 — Poll

**Issue:** The “I want AI to do it for me” option can feel like a trap or moral judgment.  
**Fix:** Make it anonymous and normalize honesty: “Many people have felt all three at different times.” Add a transition: “The goal is not guilt; the goal is control.”

### Slide 3 — Main thesis

**Issue:** “AI will not replace our mind” is inspiring but absolute.  
**Fix:** Reframe: “AI can replace some outputs, but not your responsibility for understanding, checking, and choosing.”

### Slide 4 — Next-token prediction

**Issue:** “World’s most expensive guessing game” is memorable but can trivialize learned structure.  
**Fix:** “It predicts continuations using patterns learned from vast training data. That is more than random guessing, but less than guaranteed understanding.”

### Slide 5 — Tokenization

**Issue:** Useful but secondary.  
**Fix:** Keep only if it supports later prompt advice. Otherwise move to appendix.

### Slide 6 — Attention

**Issue:** Formula plus personification is too much for a general 35-minute session.  
**Fix:** Keep the intuition on the main slide; put the formula behind an “advanced” reveal or appendix.

### Slide 7 — Transformer layers

**Issue:** Adds vocabulary but little immediate student action.  
**Fix:** Replace with a “what this means for you” sentence: “The model can connect distant parts of your prompt, but it can still miss the condition that matters.”

### Slide 8 — Training, post-training, agent

**Issue:** Very important but compressed.  
**Fix:** Use a three-row table: “training changes model weights,” “chatting uses the model,” “agent mode uses tools.” This is clearer than dense prose.

### Slide 9 — Codex memory

**Issue:** Good caveat: “agent is not training.”  
**Fix:** Make the caveat more prominent and less product-specific.

### Slide 10 — Mathematics leaves traces

**Issue:** Strong slide.  
**Fix:** Add “This is why math is a good testing ground for AI, not why AI is always reliable in math.”

### Slide 11 — Gauss sum

**Issue:** Good example, but it may be too familiar or too fast.  
**Fix:** Use it only if students actively compute one smaller case first, such as `1 + … + 10`.

### Slide 12 — `0.999… = 1`

**Issue:** This can derail into philosophical decimal debates.  
**Fix:** Add one explicit condition: “In real numbers, with the usual meaning of an infinite decimal.” Keep it optional if time is tight.

### Slide 13 — False proof

**Issue:** Excellent core activity.  
**Fix:** Ensure the red “alarm” is revealed only after students commit to a suspected step.

### Slide 14 — Fluency is not truth

**Issue:** Correct but should include a non-math falsehood.  
**Fix:** Add fake citation / invented quote as a second example.

### Slides 15–16 — Rectangle counting and Codex simulation

**Issue:** Very strong. Current lab only covers square boards.  
**Fix:** Add `m × k` generalization or adjust wording to say square board.

### Slide 17 — Euler laboratory

**Issue:** Good concept, but the lab has the `1` edge-case bug.  
**Fix:** Correct classification and add the factorization reason for `n = c − 1`: `n² + n + c = c²` when `n = c − 1`.

### Slide 18 — Student + Codex

**Issue:** Strongly aligned with the talk’s thesis.  
**Fix:** Use it as a central story; cut weaker technical slides if needed.

### Slide 19 — AI as tutor

**Issue:** Strong.  
**Fix:** Add the “stop after one hint and wait” prompt pattern.

### Slide 20 — Mental hygiene rules

**Issue:** Good rules but missing policy/privacy/disclosure; extracted text shows missing spaces.  
**Fix:** Add the school-use rules and repair spacing.

### Slide 21 — Fermat experiment

**Issue:** Good final experiment, but notation and coprime conditions need tightening.  
**Fix:** Use `p` for prime, `n` for candidate; explicitly state `gcd(a, n) = 1`.

### Slide 22 — Finale

**Issue:** Strong ending.  
**Fix:** Add one concrete action: “Tonight, use AI once as a tutor, not as a solver, and write down what changed in your answer.”

### Appendix — Sources

**Issue:** Present but easy to skip.  
**Fix:** Add QR/short link and divide sources into “AI concepts,” “Codex/product docs,” and “math examples.”

### Appendix — Audience questions

**Issue:** Useful.  
**Fix:** Promote one or two of these as interactive moments during the talk instead of leaving all as backup.

---

## Lab-by-lab notes

### Lab 1 — Rectangle hunt

**Works well**

- Off-by-one error is concrete and teachable.
- The contrast between `C(n,2)^2` and `C(n+1,2)^2` is excellent.

**Critical issue**

- It says “board” generally, but only supports square `n × n` boards.

**Fix**

- Either rename it “square board” or add width/height controls.
- Show formula with boundary lines, not just cells.

---

### Lab 2 — Pseudoprime / Fermat hunter

**Works well**

- Good demonstration that many tests can pass without proof.
- Good antidote to “checked many cases = proved.”

**Critical issue**

- The coprime condition is hidden in code rather than taught.

**Fix**

- Surface `gcd(a, n) = 1` in the UI.
- Explain why composites that pass the test are dangerous.
- Add one known example as a guided “try this” button.

---

### Lab 3 — Euler laboratory

**Works well**

- Excellent story: a pattern can hold for many values and then fail.

**Critical issue**

- `1` is incorrectly handled as composite when `c = 1`.

**Fix**

- Add prime/composite/neither classification.
- Add the algebraic explanation for why `n = c − 1` often gives an immediate composite when `c` itself is not carefully chosen.

---

### Lab 4 — Proof audit

**Works well**

- The false proof is one of the best teaching devices in the project.

**Critical issue**

- Feedback should not reveal the answer too soon.

**Fix**

- Add staged hints and a final reveal.
- Let teachers reset attempts.

---

### Lab 5 — Prompt Dojo

**Works well**

- Converts the talk from theory to practical behavior.
- The GOAL/CONTEXT/CONSTRAINTS/DONE WHEN pattern is strong.

**Critical issue**

- It is underexposed on the landing page and too math-centric.

**Fix**

- Give it its own landing card.
- Add examples for history, biology, literature, and programming.
- Include an option: “I need a tutor, not an answer.”

---

## Accessibility and technical issues

### JavaScript dependency

The lab wrapper pages contain very little content without JavaScript. Add:

```html
<noscript>
  This lab needs JavaScript. You can still read the task and formula here: …
</noscript>
```

Polish:

```html
<noscript>
  To laboratorium wymaga JavaScriptu. Treść zadania i wzór są dostępne tutaj: …
</noscript>
```

### Live output regions

For lab terminals and generated prompts, use:

```html
aria-live="polite"
```

and ensure updates are announced after button clicks.

### Formula accessibility

For formulas such as attention, binomial coefficients, and modular arithmetic:

- add MathML where practical;
- add `aria-label` text alternatives;
- avoid relying only on superscripts and visual layout.

Example:

```html
<span aria-label="a to the power n is congruent to a modulo n">
  a<sup>n</sup> ≡ a (mod n)
</span>
```

### Keyboard and focus

The slide deck already mentions keyboard navigation. Also check:

- visible focus outlines;
- no global key handler prevents typing in input fields;
- buttons and lab cards are reachable with Tab;
- current slide number is not the only navigation cue.

### Automated tests

The project already has useful structural and visual tests. Add tests for:

- the Euler `c = 1` edge case;
- lab card count and direct links from the landing page;
- missing spaces in extracted text;
- unlabeled form inputs;
- `aria-live` on dynamic lab output;
- no-JavaScript fallback text;
- Polish/English content parity.

---

## Language and wording fixes

### Polish

- Replace **atencja** as the main term with **mechanizm uwagi** or **ważenie zależności**; keep *attention* in parentheses.
- Replace **za niego** in “nie pracuje za niego” with **za ciebie / za ucznia / za człowieka**, depending on context.
- Define **posttrening** the first time it appears.
- Repair missing spaces:
  - `GOTOWE, GDY…Co`;
  - `Najpierw spróbuj sam.Zapisz`;
  - `Sprawdź płynność?Nie`;
  - similar joined sentences.
- Consider gender-inclusive phrasing in direct student instructions:
  - `utknąłeś/utknęłaś`;
  - or avoid gendered forms: `gdzie pojawił się problem`.

### English

- Replace **thinking machine** with **tool for thinking tasks** or immediately deconstruct the phrase.
- Replace **contractor** with **solver**, **doer**, or **executor**; “contractor” may sound like business/legal English.
- Replace **whom should I listen to?** with **which earlier pieces of context should receive more weight?**
- Repair missing spaces:
  - `DONE WHEN…What`;
  - `Try first.Write`;
  - `Check fluency?No`;
  - `Ask for question, not solution.Limit`.

---

## Recommended revised 35-minute version

### Version A — General high school

1. **Hook and anonymous poll** — 3 minutes  
   Fear / shortcut / tool.

2. **One simple model explanation** — 5 minutes  
   Prediction, context, why fluent text can be wrong.

3. **False proof activity** — 6 minutes  
   Students identify the first invalid step.

4. **Rectangle counting lab** — 8 minutes  
   Off-by-one error, tests, corrected formula.

5. **AI as tutor** — 6 minutes  
   Prompt: ask one diagnostic question, one hint, wait.

6. **School rules and privacy** — 4 minutes  
   Disclosure, assignment rules, private data.

7. **Final decision** — 3 minutes  
   “Do I understand more after using AI?”

### Version B — Math-profile / advanced group

Keep Version A and add one optional module:

- attention formula; or
- Euler polynomial; or
- Fermat pseudoprimes.

Do not add all three in the same 35-minute session.

---

## Suggested replacement slide: “AI in school”

### English

# AI in school: use it without losing the learning

1. Follow the teacher’s rules for the task.
2. Start with your own attempt.
3. Ask for a question or hint before asking for a solution.
4. Do not paste private data.
5. Say what AI helped with when disclosure is required.
6. Keep the final responsibility: you must be able to explain the answer.

### Polish

# AI w szkole: używaj tak, żeby nie stracić nauki

1. Stosuj zasady nauczyciela dla danego zadania.
2. Zacznij od własnej próby.
3. Poproś o pytanie albo wskazówkę, zanim poprosisz o rozwiązanie.
4. Nie wklejaj danych prywatnych.
5. Ujawnij, w czym pomogło AI, jeśli jest taki wymóg.
6. Odpowiedzialność zostaje u ciebie: musisz umieć wyjaśnić odpowiedź.

---

## Suggested replacement slide: “Good AI tutor prompt”

### English

```text
I am learning this topic. Do not solve the whole task.
First ask me one diagnostic question.
Then give one hint based on my answer.
Stop after each hint and wait.
At the end, ask me to explain the solution in my own words.
Here is my attempt: …
```

### Polish

```text
Uczę się tego tematu. Nie rozwiązuj całego zadania.
Najpierw zadaj mi jedno pytanie diagnostyczne.
Potem daj jedną wskazówkę na podstawie mojej odpowiedzi.
Zatrzymaj się po każdej wskazówce i poczekaj.
Na końcu poproś mnie o wyjaśnienie rozwiązania własnymi słowami.
Oto moja próba: …
```

---

## Suggested replacement slide: “How to check an AI answer”

### English

# Before you trust it

Ask:

1. What assumption is this using?
2. What is the smallest example?
3. What is the edge case?
4. Can I verify it another way?
5. Would I be able to explain it without the AI transcript?

### Polish

# Zanim zaufasz odpowiedzi

Zapytaj:

1. Jakie założenie jest tu użyte?
2. Jaki jest najmniejszy przykład?
3. Jaki jest przypadek brzegowy?
4. Czy mogę sprawdzić to inną metodą?
5. Czy umiałbym/umiałabym wyjaśnić to bez rozmowy z AI?

---

## Implementation checklist

### Fix content

- [ ] Correct Euler lab classification of `1`.
- [ ] Make the landing page show five lab cards.
- [ ] Add direct links from landing cards to individual labs.
- [ ] Clarify Fermat coprime condition.
- [ ] Add school policy / disclosure / privacy slide.
- [ ] Reduce main technical section for the 35-minute version.
- [ ] Move attention formula to optional/advanced material.
- [ ] Add non-math example to “fluency is not truth.”
- [ ] Add source QR/short link before finale.

### Fix language

- [ ] Reduce anthropomorphic wording.
- [ ] Replace “atencja” with “mechanizm uwagi / ważenie zależności.”
- [ ] Repair missing spaces in Polish and English slide text.
- [ ] Define “post-training” / “posttrening” on first use.
- [ ] Make English wording more student-natural: “tool,” “solver,” “hint,” “edge case.”

### Fix labs

- [ ] Add `c = 1` test for Euler.
- [ ] Add `gcd(a, n) = 1` explanation and UI indicator for Fermat.
- [ ] Add staged feedback to proof audit.
- [ ] Give Prompt Dojo its own landing card.
- [ ] Add non-math prompt templates.
- [ ] Add `m × k` support or rename rectangle lab to square-board lab.

### Fix accessibility

- [ ] Add `noscript` fallback for lab pages.
- [ ] Add `aria-live` to terminal/generated-output regions.
- [ ] Ensure all inputs have explicit labels.
- [ ] Add formula text alternatives.
- [ ] Verify focus order and keyboard-only lab use.
- [ ] Add automated accessibility checks.

---

## Bottom line

The presentation is worth keeping. Its strongest idea is that AI can be a partner in *checking, questioning, and improving* reasoning, but not a replacement for responsibility. The most important edits are not cosmetic: fix the Euler bug, expose the five labs consistently, add school-use safeguards, reduce the technical load, and make the math conditions explicit. After those changes, the talk will be much safer, clearer, and more useful for high-school students.

---

## Reviewed materials

- Landing page: https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/
- Polish deck: https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/slides/pl/
- English deck: https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/slides/en/
- Polish labs: https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/experiments/pl/
- English labs: https://nasqret.github.io/czy-ai-zastapi-nasza-glowe/experiments/en/
- Repository: https://github.com/nasqret/czy-ai-zastapi-nasza-glowe
- Official OpenAI Codex best practices and prompting references were also checked to avoid relying on outdated product assumptions.
