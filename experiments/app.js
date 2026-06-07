(() => {
  "use strict";

  const language = document.documentElement.lang === "en" ? "en" : "pl";
  const lab = document.body.dataset.lab || "hub";
  const root = document.querySelector("[data-lab-root]");

  const t = {
    pl: {
      home: "Strona główna",
      presentation: "Prezentacja",
      labTitle: "Codex Math Lab",
      labLead: "Eksperymentuj, stawiaj hipotezy, uruchamiaj testy i dopiero potem pytaj o odpowiedź.",
      simulation: "To lokalna symulacja sposobu pracy Codexa. Żadne dane nie opuszczają przeglądarki. Gotowy prompt możesz skopiować do rzeczywistego Codexa.",
      open: "Otwórz eksperyment",
      copyright: "Copyright © 2026 Bartosz Naskręcki. All rights reserved.",
      labs: {
        rectangles: ["01", "Polowanie na prostokąty", "Błąd „o jeden”, małe testy i wzór dla planszy n×n."],
        fermat: ["02", "Łowca pseudopierwszych", "Zmieniaj podstawę testu Fermata i szukaj liczb złożonych, które przechodzą test."],
        euler: ["03", "Laboratorium Eulera", "Sprawdź, jak długo wielomian n²+n+c produkuje liczby pierwsze."],
        proof: ["04", "Audyt fałszywego dowodu", "Wskaż pierwszy niedozwolony krok w płynnym, ale błędnym rozumowaniu."],
        prompt: ["05", "Prompt dojo", "Zmień własny problem w polecenie, które pomaga myśleć zamiast zdradzać wynik."]
      },
      controls: "Ustawienia eksperymentu",
      transcript: "Dziennik pracy",
      promptTitle: "Prompt do dalszej pracy w Codexie",
      run: "Uruchom eksperyment",
      copy: "Kopiuj prompt",
      copied: "Skopiowano",
      boardSize: "Rozmiar planszy n×n",
      rectangleIntro: "Najpierw uruchomimy błędną wersję z n liniami, a potem testy odkryją, że pól jest n, lecz linii n+1.",
      fermatBase: "Podstawa a",
      fermatLimit: "Szukaj do liczby",
      fermatIntro: "Szukamy złożonego n, które spełnia aⁿ ≡ a (mod n). Przejście testu nie dowodzi pierwszości.",
      eulerC: "Stała c w n²+n+c",
      eulerLimit: "Największe badane n",
      eulerIntro: "Program sprawdza kolejne wartości, znajduje pierwszy wynik złożony i pokazuje jego rozkład.",
      proofQuestion: "Które przejście jest pierwszym błędem?",
      proofRun: "Sprawdź wybór",
      problem: "Twój problem lub hipoteza",
      level: "Poziom",
      mode: "Tryb pracy Codexa",
      generate: "Zbuduj prompt",
      modes: {
        tutor: "Korepetytor: jedno pytanie naraz",
        critic: "Krytyk: znajdź błąd lub kontrprzykład",
        tester: "Eksperymentator: zaproponuj i uruchom testy",
        reviewer: "Recenzent dowodu: sprawdź każdy krok"
      }
    },
    en: {
      home: "Home",
      presentation: "Presentation",
      labTitle: "Codex Math Lab",
      labLead: "Experiment, form a hypothesis, run tests, and only then ask for an answer.",
      simulation: "This is a local simulation of a Codex workflow. No data leaves your browser. You can copy the generated prompt into the real Codex.",
      open: "Open experiment",
      copyright: "Copyright © 2026 Bartosz Naskręcki. All rights reserved.",
      labs: {
        rectangles: ["01", "Rectangle hunt", "An off-by-one bug, small tests, and the formula for an n×n board."],
        fermat: ["02", "Pseudoprime hunter", "Change the Fermat-test base and find composite numbers that pass the test."],
        euler: ["03", "Euler laboratory", "Test how long the polynomial n²+n+c keeps producing primes."],
        proof: ["04", "False-proof audit", "Identify the first illegal step in a fluent but invalid argument."],
        prompt: ["05", "Prompt dojo", "Turn your own problem into instructions that support thinking instead of revealing the result."]
      },
      controls: "Experiment settings",
      transcript: "Work log",
      promptTitle: "Prompt for further work in Codex",
      run: "Run experiment",
      copy: "Copy prompt",
      copied: "Copied",
      boardSize: "Board size n×n",
      rectangleIntro: "We first run a buggy version with n lines. Small tests then expose that n cells require n+1 grid lines.",
      fermatBase: "Base a",
      fermatLimit: "Search up to",
      fermatIntro: "We search for a composite n satisfying aⁿ ≡ a (mod n). Passing the test does not prove primality.",
      eulerC: "Constant c in n²+n+c",
      eulerLimit: "Largest tested n",
      eulerIntro: "The program checks consecutive values, finds the first composite result, and displays its factorization.",
      proofQuestion: "Which transition is the first error?",
      proofRun: "Check selection",
      problem: "Your problem or hypothesis",
      level: "Level",
      mode: "Codex working mode",
      generate: "Build prompt",
      modes: {
        tutor: "Tutor: ask one question at a time",
        critic: "Critic: find an error or counterexample",
        tester: "Experimenter: propose and run tests",
        reviewer: "Proof reviewer: check every step"
      }
    }
  }[language];

  const otherLanguage = language === "pl" ? "en" : "pl";
  const pathName = lab === "hub" ? "" : `${lab}.html`;
  const pageTitle = lab === "hub" ? t.labTitle : t.labs[lab]?.[1] || t.labTitle;
  document.title = `${pageTitle} · Bartosz Naskręcki`;

  const shell = (content) => `
    <div class="lab-shell">
      <nav class="lab-nav">
        <div>
          <a href="../../">${t.home}</a>
          <span aria-hidden="true"> · </span>
          <a href="../../${language}/">${t.presentation}</a>
        </div>
        <div class="lab-language">
          <a class="${language === "pl" ? "is-active" : ""}" href="../pl/${pathName}">PL</a>
          <a class="${language === "en" ? "is-active" : ""}" href="../en/${pathName}">EN</a>
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

  const copyButton = () => `<button class="copy-button" type="button" data-copy>${t.copy}</button>`;

  const promptPanel = (prompt) => `
    <section class="prompt-panel">
      <h2>${t.promptTitle}</h2>
      <textarea class="prompt-output" data-prompt-output readonly>${prompt}</textarea>
      ${copyButton()}
    </section>`;

  const bindCopy = () => {
    document.querySelector("[data-copy]")?.addEventListener("click", async (event) => {
      const output = document.querySelector("[data-prompt-output]");
      const text = output.value;
      try {
        await navigator.clipboard.writeText(text);
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
  const factor = (n) => {
    for (let divisor = 2; divisor * divisor <= n; divisor += 1) {
      if (n % divisor === 0) return [divisor, n / divisor];
    }
    return [n, 1];
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
  const line = (kind, text) => `<p class="${kind}">${text}</p>`;

  const renderHub = () => {
    const cards = Object.entries(t.labs).map(([key, [number, title, description]]) => `
      <a class="lab-card" href="${key}.html">
        <span>${number}</span>
        <h2>${title}</h2>
        <p>${description}</p>
        <b>${t.open} →</b>
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
    const initialPrompt = language === "pl"
      ? "Mam planszę n×n. Nie podawaj od razu wzoru. Najpierw zapytaj, ile linii ogranicza n pól, potem poproś mnie o test dla plansz 1×1 i 2×2. Wskaż pierwszy błąd w moim rozumowaniu."
      : "I have an n×n board. Do not give me the formula immediately. First ask how many grid lines bound n cells, then ask me to test 1×1 and 2×2 boards. Point out the first error in my reasoning.";
    root.innerHTML = shell(`
      ${labHeader("rectangles", t.rectangleIntro)}
      <main class="experiment-layout">
        <form class="control-panel" data-rectangle-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="board-size">${t.boardSize}</label><input id="board-size" name="size" type="number" min="1" max="100" value="8"></div>
          <button class="run-button" type="submit">${t.run}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          <div class="terminal" data-terminal>${line("plan", language === "pl" ? "$ czekam na rozmiar planszy" : "$ waiting for a board size")}</div>
          <div class="formula-result" data-formula>—</div>
        </section>
        ${promptPanel(initialPrompt)}
      </main>`);
    document.querySelector("[data-rectangle-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const n = Math.max(1, Math.min(100, Number(new FormData(event.currentTarget).get("size")) || 1));
      const buggy = comb2(n) ** 2;
      const correct = comb2(n + 1) ** 2;
      const terminal = document.querySelector("[data-terminal]");
      terminal.innerHTML = language === "pl"
        ? [
            line("plan", `[PLAN] wybieram 2 linie pionowe i 2 poziome`),
            line("run", `[RUN 1] używam n=${n} linii -> ${buggy}`),
            line("fail", `[TEST] dla 1×1 oczekuję 1, błędny kod daje 0 -> FAIL`),
            line("diagnosis", `[DIAGNOZA] ${n} pól potrzebuje ${n + 1} linii w każdym kierunku`),
            line("pass", `[TEST] poprawiony wynik dla ${n}×${n}: ${correct} -> PASS`)
          ].join("")
        : [
            line("plan", `[PLAN] choose 2 vertical and 2 horizontal lines`),
            line("run", `[RUN 1] use n=${n} lines -> ${buggy}`),
            line("fail", `[TEST] for 1×1 expect 1, buggy code returns 0 -> FAIL`),
            line("diagnosis", `[DIAGNOSIS] ${n} cells require ${n + 1} lines in each direction`),
            line("pass", `[TEST] corrected result for ${n}×${n}: ${correct} -> PASS`)
          ].join("");
      document.querySelector("[data-formula]").textContent = `C(${n + 1},2)² = ${comb2(n + 1)}² = ${correct}`;
    });
    bindCopy();
  };

  const renderFermat = () => {
    const initialPrompt = language === "pl"
      ? "Badam test Fermata dla podstawy a. Napisz mały program szukający pierwszej liczby złożonej n, dla której a^n ≡ a (mod n). Pokaż faktoryzację kontrprzykładu i wyjaśnij, dlaczego eksperyment nie jest dowodem pierwszości."
      : "I am exploring the Fermat test for base a. Write a small program that finds the first composite n satisfying a^n ≡ a (mod n). Factor the counterexample and explain why the experiment is not a proof of primality.";
    root.innerHTML = shell(`
      ${labHeader("fermat", t.fermatIntro)}
      <main class="experiment-layout">
        <form class="control-panel" data-fermat-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="fermat-base">${t.fermatBase}</label><input id="fermat-base" name="base" type="number" min="2" max="30" value="2"></div>
          <div class="field"><label for="fermat-limit">${t.fermatLimit}</label><input id="fermat-limit" name="limit" type="number" min="20" max="10000" value="400"></div>
          <button class="run-button" type="submit">${t.run}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          <div class="terminal" data-terminal>${line("plan", language === "pl" ? "$ wybierz podstawę testu" : "$ choose a test base")}</div>
          <div class="formula-result" data-formula>—</div>
        </section>
        ${promptPanel(initialPrompt)}
      </main>`);
    document.querySelector("[data-fermat-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const base = Math.max(2, Math.min(30, Number(data.get("base")) || 2));
      const limit = Math.max(20, Math.min(10000, Number(data.get("limit")) || 400));
      let found = null;
      for (let n = 4; n <= limit; n += 1) {
        if (!isPrime(n) && gcd(base, n) === 1 && modPow(base, n, n) === BigInt(base % n)) {
          found = n;
          break;
        }
      }
      const terminal = document.querySelector("[data-terminal]");
      const formula = document.querySelector("[data-formula]");
      if (found) {
        const [left, right] = factor(found);
        terminal.innerHTML = language === "pl"
          ? [
              line("plan", `[HIPOTEZA] testuję a=${base}`),
              line("run", `[SZUKAM] liczby złożone n ≤ ${limit}`),
              line("fail", `[KONTRPRZYKŁAD] n=${found}=${left}·${right}`),
              line("pass", `[SPRAWDZENIE] ${base}^${found} mod ${found} = ${base % found}`),
              line("result", `[WNIOSEK] przejście testu nie dowodzi pierwszości`)
            ].join("")
          : [
              line("plan", `[HYPOTHESIS] test base a=${base}`),
              line("run", `[SEARCH] composite n ≤ ${limit}`),
              line("fail", `[COUNTEREXAMPLE] n=${found}=${left}·${right}`),
              line("pass", `[CHECK] ${base}^${found} mod ${found} = ${base % found}`),
              line("result", `[CONCLUSION] passing the test does not prove primality`)
            ].join("");
        formula.textContent = `${found} | (${base}^${found} − ${base}),  ${found} = ${left} · ${right}`;
      } else {
        terminal.innerHTML = line("diagnosis", language === "pl"
          ? `[BRAK WYNIKU] zwiększ limit; brak kontrprzykładu do ${limit} nie jest dowodem`
          : `[NO RESULT] increase the limit; no counterexample up to ${limit} is not a proof`);
        formula.textContent = "—";
      }
    });
    bindCopy();
  };

  const renderEuler = () => {
    const initialPrompt = language === "pl"
      ? "Zbadaj wielomian n²+n+c. Nie zgaduj. Dla kolejnych n sprawdzaj pierwszość wartości, zatrzymaj się na pierwszej liczbie złożonej, pokaż jej rozkład i zaproponuj matematyczne wyjaśnienie."
      : "Explore the polynomial n²+n+c. Do not guess. Test consecutive values for primality, stop at the first composite value, factor it, and propose a mathematical explanation.";
    root.innerHTML = shell(`
      ${labHeader("euler", t.eulerIntro)}
      <main class="experiment-layout">
        <form class="control-panel" data-euler-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="euler-c">${t.eulerC}</label><input id="euler-c" name="c" type="number" min="1" max="500" value="41"></div>
          <div class="field"><label for="euler-limit">${t.eulerLimit}</label><input id="euler-limit" name="limit" type="number" min="1" max="500" value="100"></div>
          <button class="run-button" type="submit">${t.run}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          <div class="terminal" data-terminal>${line("plan", language === "pl" ? "$ ustaw stałą c" : "$ choose constant c")}</div>
          <div class="formula-result" data-formula>—</div>
        </section>
        ${promptPanel(initialPrompt)}
      </main>`);
    document.querySelector("[data-euler-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const c = Math.max(1, Math.min(500, Number(data.get("c")) || 41));
      const limit = Math.max(1, Math.min(500, Number(data.get("limit")) || 100));
      let result = null;
      for (let n = 0; n <= limit; n += 1) {
        const value = n * n + n + c;
        if (!isPrime(value)) {
          result = { n, value, factors: factor(value) };
          break;
        }
      }
      const terminal = document.querySelector("[data-terminal]");
      const formula = document.querySelector("[data-formula]");
      if (result) {
        terminal.innerHTML = language === "pl"
          ? [
              line("plan", `[PLAN] sprawdzam n²+n+${c}`),
              line("run", `[RUN] n=0,1,2,...`),
              line("fail", `[STOP] n=${result.n} daje ${result.value}, liczbę złożoną`),
              line("pass", `[ROZKŁAD] ${result.value}=${result.factors[0]}·${result.factors[1]}`),
              line("result", `[WNIOSEK] wzór działał dla ${result.n} kolejnych wartości n`)
            ].join("")
          : [
              line("plan", `[PLAN] test n²+n+${c}`),
              line("run", `[RUN] n=0,1,2,...`),
              line("fail", `[STOP] n=${result.n} gives composite ${result.value}`),
              line("pass", `[FACTOR] ${result.value}=${result.factors[0]}·${result.factors[1]}`),
              line("result", `[CONCLUSION] the formula produced primes for ${result.n} consecutive n values`)
            ].join("");
        formula.textContent = `${result.n}² + ${result.n} + ${c} = ${result.value} = ${result.factors[0]} · ${result.factors[1]}`;
      } else {
        terminal.innerHTML = line("diagnosis", language === "pl"
          ? `[BRAK KONTRPRZYKŁADU] do n=${limit}; zwiększ zakres`
          : `[NO COUNTEREXAMPLE] up to n=${limit}; increase the range`);
        formula.textContent = "—";
      }
    });
    bindCopy();
  };

  const renderProof = () => {
    const prompt = language === "pl"
      ? "Sprawdź poniższy dowód krok po kroku. Wskaż pierwszy niepoprawny krok, nazwij warunek, który został złamany, i nie oceniaj wyłącznie końcowego wyniku."
      : "Audit the proof below step by step. Identify the first invalid transition, name the violated condition, and do not judge only the final result.";
    const labels = language === "pl"
      ? ["a=b≠0 ⇒ a²=ab", "a²=ab ⇒ a²−b²=ab−b²", "Rozkład obu stron na czynniki", "Skrócenie czynnika a−b", "a+b=b ⇒ 2b=b ⇒ 2=1"]
      : ["a=b≠0 ⇒ a²=ab", "a²=ab ⇒ a²−b²=ab−b²", "Factor both sides", "Cancel the factor a−b", "a+b=b ⇒ 2b=b ⇒ 2=1"];
    root.innerHTML = shell(`
      ${labHeader("proof")}
      <main class="experiment-layout">
        <form class="proof-steps" data-proof-form>
          <h2>${t.proofQuestion}</h2>
          ${labels.map((label, index) => `<label class="proof-option"><input type="radio" name="step" value="${index}" ${index === 0 ? "checked" : ""}><span>${index + 1}. ${label}</span></label>`).join("")}
          <button class="run-button" type="submit">${t.proofRun}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          <div class="terminal" data-terminal>${line("plan", language === "pl" ? "$ wskaż podejrzany krok" : "$ select the suspicious step")}</div>
          <div class="formula-result" data-formula>—</div>
        </section>
        ${promptPanel(`${prompt}\n\na=b≠0\na²=ab\na²−b²=ab−b²\n(a−b)(a+b)=b(a−b)\na+b=b\n2b=b\n2=1`)}
      </main>`);
    document.querySelector("[data-proof-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const selected = Number(new FormData(event.currentTarget).get("step"));
      const correct = selected === 3;
      document.querySelector("[data-terminal]").innerHTML = language === "pl"
        ? [
            line("plan", `[AUDYT] sprawdzam warunki każdego przejścia`),
            line(correct ? "pass" : "fail", correct ? `[TRAFIONE] krok 4 jest pierwszym błędem` : `[JESZCZE NIE] krok ${selected + 1} jest dozwolony`),
            line("diagnosis", `[WARUNEK] a=b, więc a−b=0; nie wolno przez to dzielić`),
            line("result", `[WERDYKT] płynny zapis nie zastępuje kontroli warunków`)
          ].join("")
        : [
            line("plan", `[AUDIT] check the conditions for every transition`),
            line(correct ? "pass" : "fail", correct ? `[CORRECT] step 4 is the first error` : `[NOT YET] step ${selected + 1} is valid`),
            line("diagnosis", `[CONDITION] a=b, so a−b=0; division is forbidden`),
            line("result", `[VERDICT] fluent notation does not replace checking conditions`)
          ].join("");
      document.querySelector("[data-formula]").textContent = "a − b = 0";
    });
    bindCopy();
  };

  const renderPrompt = () => {
    root.innerHTML = shell(`
      ${labHeader("prompt")}
      <main class="experiment-layout">
        <form class="control-panel" data-prompt-form>
          <h2>${t.controls}</h2>
          <div class="field"><label for="problem">${t.problem}</label><textarea id="problem" name="problem">${language === "pl" ? "Czy każda liczba postaci n²+n+41 jest pierwsza?" : "Is every number of the form n²+n+41 prime?"}</textarea></div>
          <div class="field"><label for="level">${t.level}</label><select id="level" name="level"><option>${language === "pl" ? "klasa 7–8" : "grades 7–8"}</option><option>${language === "pl" ? "liceum" : "high school"}</option><option>${language === "pl" ? "poziom rozszerzony" : "advanced"}</option></select></div>
          <div class="field"><label for="mode">${t.mode}</label><select id="mode" name="mode">${Object.entries(t.modes).map(([value, label]) => `<option value="${value}">${label}</option>`).join("")}</select></div>
          <button class="run-button" type="submit">${t.generate}</button>
        </form>
        <section class="result-panel">
          <h2>${t.transcript}</h2>
          <div class="terminal" data-terminal>${line("plan", language === "pl" ? "$ opisz swój problem" : "$ describe your problem")}</div>
          <div class="formula-result" data-formula>Goal + context + constraints + done when</div>
        </section>
        ${promptPanel("")}
      </main>`);
    document.querySelector("[data-prompt-form]").addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const problem = String(data.get("problem") || "").trim();
      const level = String(data.get("level"));
      const mode = String(data.get("mode"));
      const modeInstruction = {
        pl: {
          tutor: "Nie podawaj rozwiązania. Zadawaj mi po jednym pytaniu i czekaj na odpowiedź.",
          critic: "Nie potwierdzaj mojej hipotezy. Szukaj pierwszego błędu lub najmniejszego kontrprzykładu.",
          tester: "Zaproponuj mały eksperyment obliczeniowy, uruchom testy na prostych przypadkach i wyjaśnij, czego test nie dowodzi.",
          reviewer: "Sprawdź każdy krok osobno. Wskaż pierwszy błędny krok i nazwij złamany warunek."
        },
        en: {
          tutor: "Do not reveal the solution. Ask one question at a time and wait for my answer.",
          critic: "Do not confirm my hypothesis. Search for the first error or the smallest counterexample.",
          tester: "Propose a small computational experiment, run simple test cases, and explain what the test does not prove.",
          reviewer: "Check every step separately. Identify the first invalid step and name the violated condition."
        }
      }[language][mode];
      const generated = language === "pl"
        ? `CEL: Chcę zrozumieć problem: ${problem}\nKONTEKST: Mój poziom to ${level}. Pokażę własne próby i chcę zachować odpowiedzialność za rozwiązanie.\nOGRANICZENIA: ${modeInstruction} Oddziel eksperyment od dowodu. Nie używaj danych osobowych.\nGOTOWE, GDY: potrafię wyjaśnić metodę i samodzielnie rozwiązać podobny przykład.`
        : `GOAL: I want to understand this problem: ${problem}\nCONTEXT: My level is ${level}. I will show my own attempts and remain responsible for the solution.\nCONSTRAINTS: ${modeInstruction} Separate experiments from proofs. Do not use personal data.\nDONE WHEN: I can explain the method and solve a similar example on my own.`;
      document.querySelector("[data-prompt-output]").value = generated;
      document.querySelector("[data-terminal]").innerHTML = language === "pl"
        ? [
            line("plan", `[CEL] zapisany`),
            line("pass", `[KONTEKST] poziom: ${level}`),
            line("diagnosis", `[OGRANICZENIA] tryb: ${t.modes[mode]}`),
            line("result", `[KRYTERIUM] uczeń umie przenieść metodę na nowy przykład`)
          ].join("")
        : [
            line("plan", `[GOAL] recorded`),
            line("pass", `[CONTEXT] level: ${level}`),
            line("diagnosis", `[CONSTRAINTS] mode: ${t.modes[mode]}`),
            line("result", `[DONE WHEN] the student can transfer the method to a new example`)
          ].join("");
    });
    bindCopy();
    document.querySelector("[data-prompt-form]").requestSubmit();
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
