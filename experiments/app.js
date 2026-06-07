(() => {
  "use strict";

  const language = document.documentElement.lang === "en" ? "en" : "pl";
  const lab = document.body.dataset.lab || "hub";
  const root = document.querySelector("[data-lab-root]");

  const locales = {
    pl: {
      home: "Strona główna",
      presentation: "Prezentacja",
      labTitle: "Codex Math Lab",
      labLead: "Eksperymentuj, stawiaj hipotezy i uruchamiaj testy. Odróżniaj wynik eksperymentu komputerowego od matematycznego uzasadnienia.",
      simulation: "Ta strona odtwarza przykładowy tok pracy, ale nie łączy się z Codexem. Dane pozostają w przeglądarce, a gotowy prompt możesz skopiować do rzeczywistego Codexa.",
      open: "Otwórz eksperyment",
      copyright: "Copyright © 2026 Bartosz Naskręcki. All rights reserved.",
      controls: "Ustawienia eksperymentu",
      transcript: "Dziennik pracy",
      promptTitle: "Prompt do dalszej pracy w Codexie",
      run: "Uruchom eksperyment",
      copy: "Kopiuj prompt",
      copied: "Skopiowano",
      computerFound: "Obliczenie pokazało",
      mathStillNeeds: "Wciąż trzeba uzasadnić",
      labs: {
        rectangles: ["01", "Polowanie na prostokąty", "Błąd „o jeden”, małe testy i wzór dla prostokątnej planszy m×k."],
        fermat: ["02", "Łowca pseudopierwszych", "Standardowy test Fermata, warunek NWD i liczby złożone, które przechodzą test."],
        euler: ["03", "Laboratorium Eulera", "Klasyfikuj wartości n²+n+c i znajdź granicę efektownego wzorca."],
        proof: ["04", "Audyt fałszywego dowodu", "Korzystaj ze wskazówek od ogólnej do coraz bardziej konkretnej i wskaż pierwszy niedozwolony krok."],
        prompt: ["05", "Warsztat dobrych poleceń", "Buduj polecenia z pięciu dziedzin, które pomagają myśleć zamiast zdradzać odpowiedź."]
      },
      rectangles: {
        rows: "Liczba wierszy m",
        columns: "Liczba kolumn k",
        intro: "Każdy prostokąt jest wyznaczony przez dwie z m+1 linii poziomych oraz dwie z k+1 linii pionowych. Kwadraty również są prostokątami.",
        waiting: "$ ustaw wymiary planszy",
        found: "liczbę prostokątów przez wyliczenie wszystkich par linii i porównanie wyniku ze wzorem.",
        needs: "uzasadnić, dlaczego każdemu prostokątowi odpowiada dokładnie jedna para linii w każdym kierunku."
      },
      fermat: {
        base: "Podstawa a",
        limit: "Największe badane n",
        intro: "Dla NWD(a,n)=1 testujemy standardową kongruencję aⁿ⁻¹ ≡ 1 (mod n). Jej spełnienie jest konieczne dla pierwszości, ale nie wystarcza.",
        waiting: "$ wybierz podstawę testu",
        found: "złożone n względnie pierwsze z a, które przechodzi standardowy test Fermata.",
        needs: "wyjaśnić, dlaczego test jest tylko warunkiem koniecznym i skąd bierze się równoważna postać aⁿ ≡ a (mod n)."
      },
      euler: {
        c: "Stała c w n²+n+c",
        limit: "Największe badane n",
        intro: "Każdą wartość klasyfikujemy jako pierwszą, złożoną albo ani pierwszą, ani złożoną. Liczba 1 nie jest ani pierwsza, ani złożona.",
        waiting: "$ ustaw stałą c",
        found: "pierwszą wartość, która nie jest liczbą pierwszą, oraz jej poprawną klasyfikację.",
        needs: "wyjaśnić strukturę wzoru; gdy n=c−1, otrzymujemy c², co dla c>1 jest złożone."
      },
      proof: {
        question: "Które przejście jest pierwszym błędem?",
        check: "Sprawdź wybór",
        hint: "Daj wskazówkę",
        reset: "Zacznij od nowa",
        reveal: "Ujawnij rozwiązanie",
        waiting: "$ wskaż podejrzany krok lub poproś o wskazówkę",
        found: "lokalnie podejrzane przejście i warunek, który należy skontrolować.",
        needs: "sprawdzić, czy każdy krok jest dozwolony, a nie tylko ocenić absurdalny wynik końcowy."
      },
      prompt: {
        problem: "Twój problem, tekst lub hipoteza",
        level: "Poziom",
        mode: "Sposób pomocy",
        subject: "Dziedzina",
        tutorGuard: "Pomagaj krok po kroku, nie podawaj od razu odpowiedzi",
        generate: "Zbuduj prompt",
        waiting: "$ wybierz dziedzinę i opisz problem",
        found: "strukturę celu, kontekstu, ograniczeń i kryterium zakończenia.",
        needs: "ocenić odpowiedź, sprawdzić fakty i samodzielnie przenieść metodę na nowy problem.",
        subjects: {
          math: ["Matematyka", "Czy każda liczba postaci n²+n+41 jest pierwsza?"],
          history: ["Historia", "Które przyczyny najbardziej wpłynęły na wybuch I wojny światowej?"],
          biology: ["Biologia", "Jak zaprojektować doświadczenie sprawdzające wpływ światła na kiełkowanie?"],
          literature: ["Literatura", "Jak obronić interpretację motywu winy w wybranej lekturze?"],
          programming: ["Programowanie", "Mój program czasem zwraca zły wynik. Jak znaleźć najmniejszy przypadek testowy?"]
        },
        modes: {
          tutor: "Korepetytor: jedno pytanie naraz",
          critic: "Krytyk: znajdź błąd lub kontrprzykład",
          tester: "Eksperymentator: zaproponuj i uruchom testy",
          reviewer: "Recenzent: sprawdź rozumowanie krok po kroku"
        }
      }
    },
    en: {
      home: "Home",
      presentation: "Presentation",
      labTitle: "Codex Math Lab",
      labLead: "Experiment, form hypotheses, run tests, and then separate what the computer found from what mathematics must still explain.",
      simulation: "This is a local simulation of a Codex workflow. No data leaves your browser. You can copy the generated prompt into the real Codex.",
      open: "Open experiment",
      copyright: "Copyright © 2026 Bartosz Naskręcki. All rights reserved.",
      controls: "Experiment settings",
      transcript: "Work log",
      promptTitle: "Prompt for further work in Codex",
      run: "Run experiment",
      copy: "Copy prompt",
      copied: "Copied",
      computerFound: "Computer found",
      mathStillNeeds: "Mathematics still needs to",
      labs: {
        rectangles: ["01", "Rectangle hunt", "An off-by-one bug, small tests, and the formula for a rectangular m×k board."],
        fermat: ["02", "Pseudoprime hunter", "The standard Fermat test, its gcd condition, and composite numbers that pass."],
        euler: ["03", "Euler laboratory", "Classify values of n²+n+c and find where a striking pattern ends."],
        proof: ["04", "False-proof audit", "Use graduated hints and identify the first illegal transition."],
        prompt: ["05", "Prompt dojo", "Build prompts in five subjects that support thinking instead of revealing the answer."]
      },
      rectangles: {
        rows: "Number of rows m",
        columns: "Number of columns k",
        intro: "A rectangle selects two of m+1 horizontal lines and two of k+1 vertical lines. Squares count as rectangles.",
        waiting: "$ choose the board dimensions",
        found: "the rectangle count by enumerating pairs of lines and matching the combinatorial formula.",
        needs: "justify why each rectangle corresponds to exactly one pair of boundary lines in each direction."
      },
      fermat: {
        base: "Base a",
        limit: "Search up to",
        intro: "When gcd(a,n)=1, the standard test checks aⁿ⁻¹ ≡ 1 (mod n). Passing is necessary for primality, but not sufficient.",
        waiting: "$ choose a test base",
        found: "a composite n coprime to a that passes the standard Fermat test.",
        needs: "explain why the test is only necessary and how it is equivalent to aⁿ ≡ a (mod n)."
      },
      euler: {
        c: "Constant c in n²+n+c",
        limit: "Largest tested n",
        intro: "Every value is classified as prime, composite, or neither. The number 1 is never labelled composite.",
        waiting: "$ choose constant c",
        found: "the first value that is not prime and its correct classification.",
        needs: "explain the algebraic structure; at n=c−1 the value is c², which is composite for c>1."
      },
      proof: {
        question: "Which transition is the first error?",
        check: "Check selection",
        hint: "Give me a hint",
        reset: "Reset",
        reveal: "Reveal solution",
        waiting: "$ select a suspicious step or request a hint",
        found: "a locally suspicious transition and the condition that must be checked.",
        needs: "verify the legality of every step rather than judge only the absurd final result."
      },
      prompt: {
        problem: "Your problem, text, or hypothesis",
        level: "Level",
        mode: "Codex working mode",
        subject: "Subject template",
        tutorGuard: "“Tutor, not answer machine” mode",
        generate: "Build prompt",
        waiting: "$ choose a subject and describe the problem",
        found: "a structure containing a goal, context, constraints, and a completion criterion.",
        needs: "evaluate the response, verify facts, and transfer the method independently to a new problem.",
        subjects: {
          math: ["Mathematics", "Is every number of the form n²+n+41 prime?"],
          history: ["History", "Which causes contributed most to the outbreak of World War I?"],
          biology: ["Biology", "How can I design an experiment testing the effect of light on germination?"],
          literature: ["Literature", "How can I defend an interpretation of guilt in a chosen literary work?"],
          programming: ["Programming", "My program sometimes returns a wrong result. How do I find the smallest failing test case?"]
        },
        modes: {
          tutor: "Tutor: ask one question at a time",
          critic: "Critic: find an error or counterexample",
          tester: "Experimenter: propose and run tests",
          reviewer: "Reviewer: check the reasoning step by step"
        }
      }
    }
  };
  const t = locales[language];
  const pathName = lab === "hub" ? "" : `${lab}.html`;
  const pageTitle = lab === "hub" ? t.labTitle : t.labs[lab]?.[1] || t.labTitle;
  document.title = `${pageTitle} · Bartosz Naskręcki`;

  const shell = (content) => `
    <div class="lab-shell">
      <nav class="lab-nav" aria-label="${language === "pl" ? "Nawigacja laboratorium" : "Lab navigation"}">
        <div>
          <a href="../../">${t.home}</a>
          <span aria-hidden="true"> · </span>
          <a href="../../${language}/">${t.presentation}</a>
        </div>
        <div class="lab-language" aria-label="${language === "pl" ? "Wersja językowa" : "Language version"}">
          <a class="${language === "pl" ? "is-active" : ""}" href="../pl/${pathName}" lang="pl" ${language === "pl" ? 'aria-current="page"' : ""}>PL</a>
          <a class="${language === "en" ? "is-active" : ""}" href="../en/${pathName}" lang="en" ${language === "en" ? 'aria-current="page"' : ""}>EN</a>
        </div>
      </nav>
      ${content}
      <footer class="lab-footer">
        <span>${t.copyright}</span>
        <a href="https://github.com/nasqret/czy-ai-zastapi-nasza-glowe">GitHub</a>
      </footer>
    </div>`;

  const labHeader = (key, extra = "") => {
    const [, title, description] = t.labs[key];
    return `
      <header class="experiment-header">
        <p class="lab-kicker">Codex Math Lab · ${t.labs[key][0]}</p>
        <h1>${title}</h1>
        <p>${description} ${extra}</p>
        <div class="simulation-note">${t.simulation}</div>
      </header>`;
  };

  const line = (kind, text) => `<p class="${kind}">${text}</p>`;
  const liveTerminal = (initial) => `<div class="terminal" data-terminal role="status" aria-live="polite" aria-atomic="true">${line("plan", initial)}</div>`;
  const formulaBox = () => `<output class="formula-result" data-formula aria-live="polite" aria-atomic="true" aria-label="${language === "pl" ? "Wynik matematyczny" : "Mathematical result"}">—</output>`;
  const evidencePanel = (key) => `
    <aside class="evidence-panel" aria-live="polite" aria-atomic="true">
      <p><strong>${t.computerFound}:</strong> <span data-computer-found>${t[key].found}</span></p>
      <p><strong>${t.mathStillNeeds}:</strong> <span data-math-needs>${t[key].needs}</span></p>
    </aside>`;
  const copyButton = () => `<button class="copy-button" type="button" data-copy>${t.copy}</button>`;
  const promptPanel = (prompt) => `
    <section class="prompt-panel">
      <h2>${t.promptTitle}</h2>
      <textarea class="prompt-output" data-prompt-output aria-label="${t.promptTitle}" aria-live="polite" aria-atomic="true" readonly>${prompt}</textarea>
      ${copyButton()}
    </section>`;

  const setFormula = (text, accessibleText = text) => {
    const output = document.querySelector("[data-formula]");
    output.textContent = text;
    output.setAttribute("aria-label", accessibleText);
  };

  const bindCopy = () => {
    document.querySelector("[data-copy]")?.addEventListener("click", async (event) => {
      const output = document.querySelector("[data-prompt-output]");
      try {
        await navigator.clipboard.writeText(output.value);
      } catch {
        output.select();
        document.execCommand("copy");
      }
      event.currentTarget.textContent = t.copied;
      window.setTimeout(() => { event.currentTarget.textContent = t.copy; }, 1200);
    });
  };

  const comb2 = (n) => n * (n - 1) / 2;
  const isPrime = (n) => {
    if (n < 2 || !Number.isInteger(n)) return false;
    for (let divisor = 2; divisor * divisor <= n; divisor += 1) {
      if (n % divisor === 0) return false;
    }
    return true;
  };
  const classifyInteger = (n) => {
    if (n < 2) return "neither";
    return isPrime(n) ? "prime" : "composite";
  };
  const factor = (n) => {
    for (let divisor = 2; divisor * divisor <= n; divisor += 1) {
      if (n % divisor === 0) return [divisor, n / divisor];
    }
    return null;
  };
  const gcd = (a, b) => {
    let x = Math.abs(a);
    let y = Math.abs(b);
    while (y) [x, y] = [y, x % y];
    return x;
  };
  const modPow = (base, exponent, modulus) => {
    let result = 1n;
    let value = BigInt(base) % BigInt(modulus);
    let power = BigInt(exponent);
    const mod = BigInt(modulus);
    while (power > 0n) {
      if (power & 1n) result = (result * value) % mod;
      value = (value * value) % mod;
      power >>= 1n;
    }
    return result;
  };

  const renderHub = () => {
    const cards = Object.entries(t.labs).map(([key, [number, title, description]]) => `
      <a class="lab-card" href="${key}.html">
        <span>${number}</span>
        <h2>${title}</h2>
        <p>${description}</p>
        <b>${t.open} <span aria-hidden="true">→</span></b>
      </a>`).join("");
    root.innerHTML = shell(`
      <header class="lab-hero">
        <p class="lab-kicker">AI × MATH</p>
        <h1>${t.labTitle}</h1>
        <p>${t.labLead}</p>
        <div class="simulation-note">${t.simulation}</div>
      </header>
      <main class="lab-grid">${cards}</main>`);
  };

  const renderRectangles = () => {
    const prompt = language === "pl"
      ? "Mam planszę m×k. Nie podawaj od razu wzoru. Poproś mnie o testy 1×1, 1×2 i 2×3. Następnie pomóż mi uzasadnić bijekcję między prostokątami a wyborem dwóch z m+1 linii poziomych i dwóch z k+1 linii pionowych. Wyraźnie oddziel: „komputer znalazł” od „matematyka nadal musi wyjaśnić”."
      : "I have an m×k board. Do not reveal the formula immediately. Ask me to test 1×1, 1×2, and 2×3. Then help me justify the bijection between rectangles and choosing two of m+1 horizontal lines and two of k+1 vertical lines. Explicitly separate “computer found” from “mathematics still needs to explain”.";
    root.innerHTML = shell(`
      ${labHeader("rectangles", t.rectangles.intro)}
      <main class="experiment-layout">
        <form class="control-panel" data-rectangle-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="board-rows">${t.rectangles.rows}</label><input id="board-rows" name="rows" type="number" min="1" max="100" value="8" inputmode="numeric"></div>
          <div class="field"><label for="board-columns">${t.rectangles.columns}</label><input id="board-columns" name="columns" type="number" min="1" max="100" value="8" inputmode="numeric"></div>
          <button class="run-button" type="submit">${t.run}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          ${liveTerminal(t.rectangles.waiting)}
          ${formulaBox()}
          ${evidencePanel("rectangles")}
        </section>
        ${promptPanel(prompt)}
      </main>`);
    document.querySelector("[data-rectangle-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const rows = Math.max(1, Math.min(100, Number(data.get("rows")) || 1));
      const columns = Math.max(1, Math.min(100, Number(data.get("columns")) || 1));
      const buggy = comb2(rows) * comb2(columns);
      const correct = comb2(rows + 1) * comb2(columns + 1);
      document.querySelector("[data-terminal]").innerHTML = language === "pl"
        ? [
            line("plan", "[PLAN] wybieram 2 linie poziome i 2 pionowe"),
            line("run", `[RUN 1] błędnie używam m=${rows} i k=${columns} linii → ${buggy}`),
            line("fail", "[TEST] 1×1 → oczekuję 1, błędny kod daje 0 → FAIL"),
            line("run", "[TEST] 1×2 → 3; 2×3 → 18"),
            line("diagnosis", `[DIAGNOZA] ${rows}×${columns} pól ma ${rows + 1} linii poziomych i ${columns + 1} pionowych`),
            line("pass", `[KOMPUTER ZNALAZŁ] ${correct} prostokątów → PASS`),
            line("result", "[MATEMATYKA NADAL MUSI] uzasadnić jednoznaczną odpowiedniość wyborów linii i prostokątów")
          ].join("")
        : [
            line("plan", "[PLAN] choose 2 horizontal and 2 vertical lines"),
            line("run", `[RUN 1] incorrectly use m=${rows} and k=${columns} lines → ${buggy}`),
            line("fail", "[TEST] 1×1 → expect 1, buggy code gives 0 → FAIL"),
            line("run", "[TEST] 1×2 → 3; 2×3 → 18"),
            line("diagnosis", `[DIAGNOSIS] ${rows}×${columns} cells have ${rows + 1} horizontal and ${columns + 1} vertical lines`),
            line("pass", `[COMPUTER FOUND] ${correct} rectangles → PASS`),
            line("result", "[MATHEMATICS STILL NEEDS TO] justify the one-to-one correspondence between line choices and rectangles")
          ].join("");
      setFormula(
        `C(${rows + 1},2) · C(${columns + 1},2) = ${comb2(rows + 1)} · ${comb2(columns + 1)} = ${correct}`,
        language === "pl"
          ? `Liczba prostokątów: ${rows + 1} po 2 razy ${columns + 1} po 2, czyli ${correct}`
          : `Rectangle count: ${rows + 1} choose 2 times ${columns + 1} choose 2, equal to ${correct}`
      );
    });
    bindCopy();
  };

  const renderFermat = () => {
    const prompt = language === "pl"
      ? "Badam standardowy test Fermata dla podstawy a: przy założeniu NWD(a,n)=1 sprawdzam a^(n−1) ≡ 1 (mod n). Napisz mały program szukający pierwszej liczby złożonej, która przechodzi test. Pokaż NWD, faktoryzację i wyjaśnij równoważność z a^n ≡ a (mod n): mnożenie przez a działa w przód, a powrót wymaga odwracalności a modulo n. Oddziel eksperyment od dowodu."
      : "I am studying the standard Fermat test for base a: assuming gcd(a,n)=1, check a^(n−1) ≡ 1 (mod n). Write a small program that finds the first composite number passing the test. Show the gcd, factorization, and equivalence with a^n ≡ a (mod n): multiplying by a gives one direction, while the reverse needs a to be invertible modulo n. Separate experiment from proof.";
    root.innerHTML = shell(`
      ${labHeader("fermat", t.fermat.intro)}
      <main class="experiment-layout">
        <form class="control-panel" data-fermat-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="fermat-base">${t.fermat.base}</label><input id="fermat-base" name="base" type="number" min="2" max="30" value="2" inputmode="numeric"></div>
          <div class="field"><label for="fermat-limit">${t.fermat.limit}</label><input id="fermat-limit" name="limit" type="number" min="20" max="10000" value="400" inputmode="numeric"></div>
          <button class="run-button" type="submit">${t.run}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          ${liveTerminal(t.fermat.waiting)}
          ${formulaBox()}
          <div class="equivalence-note" aria-label="${language === "pl" ? "Równoważność dwóch postaci testu Fermata" : "Equivalence of two forms of the Fermat test"}">
            <strong>${language === "pl" ? "NWD" : "gcd"}(a,n)=1:</strong> a<sup>n−1</sup> ≡ 1 (mod n) ⇔ a<sup>n</sup> ≡ a (mod n)
          </div>
          ${evidencePanel("fermat")}
        </section>
        ${promptPanel(prompt)}
      </main>`);
    document.querySelector("[data-fermat-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const base = Math.max(2, Math.min(30, Number(data.get("base")) || 2));
      const limit = Math.max(20, Math.min(10000, Number(data.get("limit")) || 400));
      let found = null;
      for (let n = 4; n <= limit; n += 1) {
        if (!isPrime(n) && gcd(base, n) === 1 && modPow(base, n - 1, n) === 1n) {
          found = n;
          break;
        }
      }
      const terminal = document.querySelector("[data-terminal]");
      if (!found) {
        terminal.innerHTML = language === "pl"
          ? [
              line("run", `[SZUKAM] złożone n≤${limit} z NWD(${base},n)=1`),
              line("diagnosis", `[BRAK WYNIKU] zwiększ limit; brak kontrprzykładu do ${limit} nie jest dowodem`),
              line("result", "[MATEMATYKA NADAL MUSI] rozstrzygnąć twierdzenie dla wszystkich n")
            ].join("")
          : [
              line("run", `[SEARCH] composite n≤${limit} with gcd(${base},n)=1`),
              line("diagnosis", `[NO RESULT] increase the limit; no counterexample up to ${limit} is not a proof`),
              line("result", "[MATHEMATICS STILL NEEDS TO] settle the statement for every n")
            ].join("");
        setFormula("—");
        return;
      }
      const [left, right] = factor(found);
      terminal.innerHTML = language === "pl"
        ? [
            line("plan", `[HIPOTEZA] testuję a=${base}; wymagane NWD(a,n)=1`),
            line("run", `[SZUKAM] złożone n≤${limit}`),
            line("pass", `[WARUNEK] NWD(${base},${found})=${gcd(base, found)}`),
            line("fail", `[KONTRPRZYKŁAD] n=${found}=${left}·${right}`),
            line("pass", `[SPRAWDZENIE] ${base}^(${found}−1) mod ${found} = 1`),
            line("diagnosis", `[RÓWNOWAŻNOŚĆ] mnożymy przez ${base}; w drugą stronę używamy odwrotności modulo ${found}`),
            line("result", "[MATEMATYKA NADAL MUSI] wyjaśnić, dlaczego test nie charakteryzuje liczb pierwszych")
          ].join("")
        : [
            line("plan", `[HYPOTHESIS] test a=${base}; require gcd(a,n)=1`),
            line("run", `[SEARCH] composite n≤${limit}`),
            line("pass", `[CONDITION] gcd(${base},${found})=${gcd(base, found)}`),
            line("fail", `[COUNTEREXAMPLE] n=${found}=${left}·${right}`),
            line("pass", `[CHECK] ${base}^(${found}−1) mod ${found} = 1`),
            line("diagnosis", `[EQUIVALENCE] multiply by ${base}; reverse using its inverse modulo ${found}`),
            line("result", "[MATHEMATICS STILL NEEDS TO] explain why the test does not characterize primes")
          ].join("");
      setFormula(
        `${base}^(${found}−1) ≡ 1 (mod ${found}),  ${found} = ${left} · ${right}`,
        language === "pl"
          ? `${base} do potęgi ${found - 1} daje resztę 1 modulo ${found}; ${found} jest równe ${left} razy ${right}`
          : `${base} to the power ${found - 1} has remainder 1 modulo ${found}; ${found} equals ${left} times ${right}`
      );
    });
    bindCopy();
  };

  const renderEuler = () => {
    const prompt = language === "pl"
      ? "Zbadaj wielomian n²+n+c. Klasyfikuj każdą wartość jako: pierwsza, złożona albo ani pierwsza, ani złożona. Pamiętaj, że 1 nie jest złożona. Znajdź pierwszą wartość niepierwszą, a następnie sprawdź algebraicznie n=c−1, dla którego n²+n+c=c². Oddziel: „komputer znalazł” od „matematyka nadal musi wyjaśnić”."
      : "Explore n²+n+c. Classify every value as prime, composite, or neither. Remember that 1 is not composite. Find the first non-prime value, then check algebraically that at n=c−1, n²+n+c=c². Separate “computer found” from “mathematics still needs to explain”.";
    root.innerHTML = shell(`
      ${labHeader("euler", t.euler.intro)}
      <main class="experiment-layout">
        <form class="control-panel" data-euler-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="euler-c">${t.euler.c}</label><input id="euler-c" name="c" type="number" min="1" max="500" value="41" inputmode="numeric"></div>
          <div class="field"><label for="euler-limit">${t.euler.limit}</label><input id="euler-limit" name="limit" type="number" min="0" max="500" value="100" inputmode="numeric"></div>
          <button class="run-button" type="submit">${t.run}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          ${liveTerminal(t.euler.waiting)}
          ${formulaBox()}
          ${evidencePanel("euler")}
        </section>
        ${promptPanel(prompt)}
      </main>`);
    document.querySelector("[data-euler-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const c = Math.max(1, Math.min(500, Number(data.get("c")) || 41));
      const limit = Math.max(0, Math.min(500, Number(data.get("limit")) || 0));
      let result = null;
      for (let n = 0; n <= limit; n += 1) {
        const value = n * n + n + c;
        const classification = classifyInteger(value);
        if (classification !== "prime") {
          result = { n, value, classification, factors: classification === "composite" ? factor(value) : null };
          break;
        }
      }
      const identityN = c - 1;
      const identityVisible = identityN <= limit;
      const identityValue = c * c;
      const classLabels = language === "pl"
        ? { prime: "pierwsza", composite: "złożona", neither: "ani pierwsza, ani złożona" }
        : { prime: "prime", composite: "composite", neither: "neither prime nor composite" };
      const terminal = document.querySelector("[data-terminal]");
      if (!result) {
        terminal.innerHTML = language === "pl"
          ? [
              line("run", `[KOMPUTER ZNALAZŁ] same liczby pierwsze dla 0≤n≤${limit}`),
              line("diagnosis", identityVisible ? `[TOŻSAMOŚĆ] n=c−1=${identityN} daje c²=${identityValue}` : `[NASTĘPNY TROP] sprawdź n=c−1=${identityN}`),
              line("result", "[MATEMATYKA NADAL MUSI] wyjaśnić wzorzec; skończony test nie jest dowodem")
            ].join("")
          : [
              line("run", `[COMPUTER FOUND] only primes for 0≤n≤${limit}`),
              line("diagnosis", identityVisible ? `[IDENTITY] n=c−1=${identityN} gives c²=${identityValue}` : `[NEXT CLUE] test n=c−1=${identityN}`),
              line("result", "[MATHEMATICS STILL NEEDS TO] explain the pattern; a finite test is not a proof")
            ].join("");
        setFormula(identityVisible ? `${identityN}² + ${identityN} + ${c} = ${c}² = ${identityValue}` : "—");
        return;
      }
      const factorText = result.factors ? `${result.factors[0]}·${result.factors[1]}` : "—";
      terminal.innerHTML = language === "pl"
        ? [
            line("plan", `[PLAN] klasyfikuję n²+n+${c}: pierwsza / złożona / żadna z nich`),
            line("run", "[RUN] n=0,1,2,…"),
            line(result.classification === "composite" ? "fail" : "diagnosis", `[STOP] n=${result.n} daje ${result.value}: ${classLabels[result.classification]}`),
            result.factors ? line("pass", `[ROZKŁAD] ${result.value}=${factorText}`) : line("pass", "[KLASYFIKACJA] 1 nie jest ani pierwsza, ani złożona"),
            line("diagnosis", `[TOŻSAMOŚĆ] dla n=c−1=${identityN}: n²+n+c=c²=${identityValue}`),
            line("result", "[MATEMATYKA NADAL MUSI] wyjaśnić, dlaczego algebra przewiduje załamanie wzorca")
          ].join("")
        : [
            line("plan", `[PLAN] classify n²+n+${c}: prime / composite / neither`),
            line("run", "[RUN] n=0,1,2,…"),
            line(result.classification === "composite" ? "fail" : "diagnosis", `[STOP] n=${result.n} gives ${result.value}: ${classLabels[result.classification]}`),
            result.factors ? line("pass", `[FACTOR] ${result.value}=${factorText}`) : line("pass", "[CLASSIFICATION] 1 is neither prime nor composite"),
            line("diagnosis", `[IDENTITY] at n=c−1=${identityN}: n²+n+c=c²=${identityValue}`),
            line("result", "[MATHEMATICS STILL NEEDS TO] explain why the algebra predicts the pattern's failure")
          ].join("");
      setFormula(
        result.factors
          ? `${result.n}² + ${result.n} + ${c} = ${result.value} = ${factorText}`
          : `${result.n}² + ${result.n} + ${c} = 1`,
        language === "pl"
          ? `Dla n równego ${result.n} wartość wynosi ${result.value}: ${classLabels[result.classification]}`
          : `At n equal to ${result.n}, the value is ${result.value}: ${classLabels[result.classification]}`
      );
    });
    bindCopy();
  };

  const renderProof = () => {
    const prompt = language === "pl"
      ? "Sprawdź dowód krok po kroku. Nie ujawniaj od razu rozwiązania. Najpierw zapytaj, który krok zmienia równanie; potem poproś o wypisanie warunku skracania; dopiero na końcu wskaż pierwszy błąd i nazwij złamany warunek."
      : "Audit the proof step by step. Do not reveal the solution immediately. First ask which step changes the equation; then ask for the condition required for cancellation; only at the end identify the first error and name the violated condition.";
    const labels = language === "pl"
      ? ["a=b≠0 ⇒ a²=ab", "a²=ab ⇒ a²−b²=ab−b²", "Rozkład obu stron na czynniki", "Skrócenie czynnika a−b", "a+b=b ⇒ 2b=b ⇒ 2=1"]
      : ["a=b≠0 ⇒ a²=ab", "a²=ab ⇒ a²−b²=ab−b²", "Factor both sides", "Cancel the factor a−b", "a+b=b ⇒ 2b=b ⇒ 2=1"];
    root.innerHTML = shell(`
      ${labHeader("proof")}
      <main class="experiment-layout">
        <form class="proof-steps" data-proof-form>
          <h2>${t.proof.question}</h2>
          ${labels.map((label, index) => `<label class="proof-option"><input type="radio" name="step" value="${index}" ${index === 0 ? "checked" : ""}><span>${index + 1}. ${label}</span></label>`).join("")}
          <div class="button-group">
            <button class="run-button" type="submit">${t.proof.check}</button>
            <button class="secondary-button" type="button" data-proof-hint>${t.proof.hint}</button>
            <button class="secondary-button" type="button" data-proof-reset>${t.proof.reset}</button>
            <button class="reveal-button" type="button" data-proof-reveal>${t.proof.reveal}</button>
          </div>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          ${liveTerminal(t.proof.waiting)}
          ${formulaBox()}
          ${evidencePanel("proof")}
        </section>
        ${promptPanel(`${prompt}\n\na=b≠0\na²=ab\na²−b²=ab−b²\n(a−b)(a+b)=b(a−b)\na+b=b\n2b=b\n2=1`)}
      </main>`);

    const terminal = document.querySelector("[data-terminal]");
    const form = document.querySelector("[data-proof-form]");
    let hintIndex = 0;
    const hints = language === "pl"
      ? [
          "Wskazówka 1: Nie zaczynaj od wyniku 2=1. Szukaj pierwszego kroku, którego nie można odwrócić.",
          "Wskazówka 2: Przy skracaniu czynnika trzeba sprawdzić, czy ten czynnik jest różny od zera.",
          "Wskazówka 3: Z założenia a=b oblicz wartość a−b."
        ]
      : [
          "Hint 1: Do not start from 2=1. Find the first transition that cannot be reversed.",
          "Hint 2: Before cancelling a factor, check that the factor is nonzero.",
          "Hint 3: Use a=b to calculate the value of a−b."
        ];

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const selected = Number(new FormData(form).get("step"));
      const correct = selected === 3;
      terminal.innerHTML = language === "pl"
        ? correct
          ? [
              line("plan", "[AUDYT] sprawdzam warunki każdego przejścia"),
              line("pass", "[TRAFIONE] krok 4 jest pierwszym błędem"),
              line("diagnosis", "[WARUNEK] skracany czynnik musi być różny od zera"),
              line("result", "[MATEMATYKA NADAL MUSI] podstawić a=b i sprawdzić, że a−b=0")
            ].join("")
          : [
              line("plan", "[AUDYT] sprawdzam wybrany krok"),
              line("fail", `[JESZCZE NIE] krok ${selected + 1} nie jest pierwszym błędem`),
              line("diagnosis", "[TROP] poszukaj pierwszego przejścia wymagającego dodatkowego warunku"),
              line("result", "[DALEJ] wybierz inny krok lub poproś o stopniowaną wskazówkę")
            ].join("")
        : correct
          ? [
              line("plan", "[AUDIT] check the conditions for every transition"),
              line("pass", "[CORRECT] step 4 is the first error"),
              line("diagnosis", "[CONDITION] a cancelled factor must be nonzero"),
              line("result", "[MATHEMATICS STILL NEEDS TO] substitute a=b and verify that a−b=0")
            ].join("")
          : [
              line("plan", "[AUDIT] inspect the selected transition"),
              line("fail", `[NOT YET] step ${selected + 1} is not the first error`),
              line("diagnosis", "[CLUE] find the first transition that requires an extra condition"),
              line("result", "[CONTINUE] select another step or request a graduated hint")
            ].join("");
      setFormula(correct ? "a − b = 0" : "?");
    });

    document.querySelector("[data-proof-hint]").addEventListener("click", () => {
      const hint = hints[Math.min(hintIndex, hints.length - 1)];
      hintIndex += 1;
      terminal.innerHTML = line("diagnosis", hint);
      setFormula("?");
    });
    document.querySelector("[data-proof-reset]").addEventListener("click", () => {
      form.reset();
      hintIndex = 0;
      terminal.innerHTML = line("plan", t.proof.waiting);
      setFormula("—");
      form.querySelector('input[value="0"]').focus();
    });
    document.querySelector("[data-proof-reveal]").addEventListener("click", () => {
      form.querySelector('input[value="3"]').checked = true;
      terminal.innerHTML = language === "pl"
        ? [
            line("pass", "[ROZWIĄZANIE] pierwszy błąd to krok 4"),
            line("diagnosis", "[OBLICZENIE] a=b ⇒ a−b=0"),
            line("fail", "[NIEDOZWOLONE] skrócenie przez a−b jest dzieleniem przez zero"),
            line("result", "[MATEMATYKA NADAL MUSI] kontrolować warunki każdego przekształcenia")
          ].join("")
        : [
            line("pass", "[SOLUTION] the first error is step 4"),
            line("diagnosis", "[CALCULATION] a=b ⇒ a−b=0"),
            line("fail", "[ILLEGAL] cancelling a−b divides by zero"),
            line("result", "[MATHEMATICS STILL NEEDS TO] check the conditions of every transformation")
          ].join("");
      setFormula("a − b = 0");
    });
    bindCopy();
  };

  const renderPrompt = () => {
    const subjectOptions = Object.entries(t.prompt.subjects)
      .map(([value, [label]]) => `<option value="${value}">${label}</option>`)
      .join("");
    const modeOptions = Object.entries(t.prompt.modes)
      .map(([value, label]) => `<option value="${value}">${label}</option>`)
      .join("");
    root.innerHTML = shell(`
      ${labHeader("prompt")}
      <main class="experiment-layout">
        <form class="control-panel" data-prompt-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="subject">${t.prompt.subject}</label><select id="subject" name="subject">${subjectOptions}</select></div>
          <div class="field"><label for="problem">${t.prompt.problem}</label><textarea id="problem" name="problem">${t.prompt.subjects.math[1]}</textarea></div>
          <div class="field"><label for="level">${t.prompt.level}</label><select id="level" name="level"><option>${language === "pl" ? "klasa 7–8" : "grades 7–8"}</option><option>${language === "pl" ? "liceum" : "high school"}</option><option>${language === "pl" ? "poziom rozszerzony" : "advanced"}</option></select></div>
          <div class="field"><label for="mode">${t.prompt.mode}</label><select id="mode" name="mode">${modeOptions}</select></div>
          <label class="check-option"><input type="checkbox" name="tutorGuard" checked><span>${t.prompt.tutorGuard}</span></label>
          <button class="run-button" type="submit">${t.prompt.generate}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          ${liveTerminal(t.prompt.waiting)}
          ${formulaBox()}
          ${evidencePanel("prompt")}
        </section>
        ${promptPanel("")}
      </main>`);

    const form = document.querySelector("[data-prompt-form]");
    const subject = form.querySelector("[name=subject]");
    const problem = form.querySelector("[name=problem]");
    subject.addEventListener("change", () => {
      problem.value = t.prompt.subjects[subject.value][1];
      problem.focus();
    });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const problemText = String(data.get("problem") || "").trim();
      const level = String(data.get("level"));
      const mode = String(data.get("mode"));
      const subjectLabel = t.prompt.subjects[String(data.get("subject"))][0];
      const tutorGuard = data.get("tutorGuard") === "on";
      const modeInstructions = {
        pl: {
          tutor: "Zadawaj jedno pytanie naraz i po każdym pytaniu czekaj na moją odpowiedź.",
          critic: "Nie potwierdzaj automatycznie mojej tezy. Szukaj pierwszego błędu, słabego założenia lub kontrprzykładu.",
          tester: "Zaproponuj mały test, zacznij od przypadków brzegowych i powiedz, czego eksperyment nie dowodzi.",
          reviewer: "Sprawdź rozumowanie krok po kroku. Zatrzymaj się przy pierwszym błędzie i nazwij brakujący warunek."
        },
        en: {
          tutor: "Ask one question at a time and wait for my response after each question.",
          critic: "Do not automatically confirm my claim. Search for the first error, weak assumption, or counterexample.",
          tester: "Propose a small test, begin with edge cases, and state what the experiment does not prove.",
          reviewer: "Check the reasoning step by step. Stop at the first error and name the missing condition."
        }
      }[language][mode];
      const noAnswer = language === "pl"
        ? "Nie podawaj gotowej odpowiedzi ani kompletnego rozwiązania, dopóki wyraźnie o nie nie poproszę. Najpierw diagnozuj moją wiedzę i dawaj jedną wskazówkę naraz."
        : "Do not give the final answer or a complete solution unless I explicitly ask for it. First diagnose my understanding and give one hint at a time.";
      const generated = language === "pl"
        ? `CEL: Chcę zrozumieć problem z dziedziny „${subjectLabel}”: ${problemText}\nKONTEKST: Mój poziom to ${level}. Pokażę własną próbę i chcę dojść do rozwiązania samodzielnie.\nSPOSÓB PRACY: ${modeInstructions}\nOGRANICZENIA: ${tutorGuard ? noAnswer : "Wyraźnie oddziel fakty, hipotezy i niepewność."} Nie używaj danych osobowych. W obliczeniach oddziel wynik eksperymentu od uzasadnienia.\nGOTOWE, GDY: potrafię własnymi słowami wyjaśnić metodę, sprawdzić odpowiedź i samodzielnie rozwiązać podobny przykład.`
        : `GOAL: I want to understand this ${subjectLabel} problem: ${problemText}\nCONTEXT: My level is ${level}. I will show my own attempt and remain responsible for the solution.\nWORKING METHOD: ${modeInstructions}\nCONSTRAINTS: ${tutorGuard ? noAnswer : "Clearly separate facts, hypotheses, and uncertainty."} Do not use personal data. In computational work, separate “computer found” from “mathematics still needs to explain”.\nDONE WHEN: I can explain the method in my own words, verify the response, and solve a similar example independently.`;
      document.querySelector("[data-prompt-output]").value = generated;
      document.querySelector("[data-terminal]").innerHTML = language === "pl"
        ? [
            line("plan", `[SZABLON] ${subjectLabel}`),
            line("pass", `[KONTEKST] poziom: ${level}`),
            line("diagnosis", `[TRYB] ${t.prompt.modes[mode]}`),
            line(tutorGuard ? "pass" : "run", `[KOREPETYTOR, NIE ODPOWIEDŹ] ${tutorGuard ? "włączony" : "wyłączony"}`),
            line("result", "[TY NADAL MUSISZ] sprawdzić fakty i argumenty oraz zastosować metodę w nowym zadaniu")
          ].join("")
        : [
            line("plan", `[TEMPLATE] ${subjectLabel}`),
            line("pass", `[CONTEXT] level: ${level}`),
            line("diagnosis", `[MODE] ${t.prompt.modes[mode]}`),
            line(tutorGuard ? "pass" : "run", `[TUTOR, NOT ANSWER] ${tutorGuard ? "enabled" : "disabled"}`),
            line("result", "[MATHEMATICS STILL NEEDS TO] verify facts, arguments, and whether the method transfers")
          ].join("");
      setFormula(language === "pl" ? "Cel + kontekst + sposób pracy + ograniczenia + kryterium" : "Goal + context + working method + constraints + criterion");
    });
    bindCopy();
    form.requestSubmit();
  };

  const renderers = {
    hub: renderHub,
    rectangles: renderRectangles,
    fermat: renderFermat,
    euler: renderEuler,
    proof: renderProof,
    prompt: renderPrompt
  };

  renderers[lab]?.();
})();
