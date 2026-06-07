(() => {
  "use strict";

  const deck = document.querySelector(".deck");
  const allSlides = [...document.querySelectorAll(".slide")];
  const progress = document.querySelector("[data-progress]");
  const counter = document.querySelector("[data-counter]");
  const clock = document.querySelector("[data-clock]");
  const panel = document.querySelector("[data-speaker-panel]");
  const noteTitle = document.querySelector("[data-note-title]");
  const noteBody = document.querySelector("[data-note-body]");
  const slideTime = document.querySelector("[data-slide-time]");
  const totalTime = document.querySelector("[data-total-time]");
  const trackSelect = document.querySelector("[data-track-select]");
  const language = document.documentElement.lang === "en" ? "en" : "pl";
  const copy = {
    pl: {
      appendix: "dodatek",
      missingNotes: "Brak notatek.",
      tracks: { core: "rdzeń", math: "matematyka", full: "pełna" },
      counting: "Obliczam…",
      counterexampleFound: "Kontrprzykład znaleziony",
      rectangleWorking: "Uruchamiam testy…",
      rectangleDone: "Testy zakończone",
      rectangleLines: [
        ["plan", "[PLAN] R(m,k) = C(m+1,2) · C(k+1,2)"],
        ["run", "[RUN 1] błędny kod używa m i k linii"],
        ["fail", "[TEST] 1×1: oczekiwano 1, otrzymano 0 -> FAIL"],
        ["diagnosis", "[DIAGNOZA] m pól wymaga m+1 linii; k pól wymaga k+1 linii"],
        ["patch", "[POPRAWKA] range(size) -> range(size + 1)"],
        ["pass", "[TEST] 1×1: 1 -> PASS"],
        ["pass", "[TEST] 1×2: 3 -> PASS"],
        ["pass", "[TEST] 2×3: 18 -> PASS"],
        ["result", "[WYNIK] 8×8: C(9,2)² = 1296"]
      ],
      fermatWorking: "Szukam pseudopierwszej…",
      fermatDone: "Znaleziono 341",
      fermatLines: [
        ["plan", "[WARUNEK] n złożona, gcd(2,n)=1"],
        ["run", "[TEST] sprawdzam 2^(n-1) mod n = 1"],
        ["diagnosis", "[SZUKAM] kolejne n < 400"],
        ["fail", "[KONTRPRZYKŁAD] 341 = 11 × 31"],
        ["pass", "[SPRAWDZENIE] gcd(2,341)=1; 2^340 mod 341 = 1"],
        ["result", "[WNIOSEK] przejście testu Fermata nie dowodzi pierwszości"]
      ]
    },
    en: {
      appendix: "appendix",
      missingNotes: "No speaker notes.",
      tracks: { core: "core", math: "mathematics", full: "full" },
      counting: "Calculating…",
      counterexampleFound: "Counterexample found",
      rectangleWorking: "Running tests…",
      rectangleDone: "Tests completed",
      rectangleLines: [
        ["plan", "[PLAN] R(m,k) = C(m+1,2) · C(k+1,2)"],
        ["run", "[RUN 1] buggy code uses m and k grid lines"],
        ["fail", "[TEST] 1×1: expected 1, got 0 -> FAIL"],
        ["diagnosis", "[DIAGNOSIS] m cells need m+1 lines; k cells need k+1 lines"],
        ["patch", "[PATCH] range(size) -> range(size + 1)"],
        ["pass", "[TEST] 1×1: 1 -> PASS"],
        ["pass", "[TEST] 1×2: 3 -> PASS"],
        ["pass", "[TEST] 2×3: 18 -> PASS"],
        ["result", "[RESULT] 8×8: C(9,2)² = 1296"]
      ],
      fermatWorking: "Searching for a pseudoprime…",
      fermatDone: "Found 341",
      fermatLines: [
        ["plan", "[CONDITION] composite n, gcd(2,n)=1"],
        ["run", "[TEST] check 2^(n-1) mod n = 1"],
        ["diagnosis", "[SEARCH] consecutive n < 400"],
        ["fail", "[COUNTEREXAMPLE] 341 = 11 × 31"],
        ["pass", "[CHECK] gcd(2,341)=1; 2^340 mod 341 = 1"],
        ["result", "[CONCLUSION] passing the Fermat test does not prove primality"]
      ]
    }
  }[language];

  let track = new URLSearchParams(window.location.search).get("track")
    || window.localStorage.getItem("presentation-track")
    || "core";
  if (!["core", "math", "full"].includes(track)) track = "core";

  let slides = [];
  let talkSlides = [];
  let index = 0;
  let startTime = null;
  let timer = null;
  let overview = false;

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const rest = Math.floor(seconds % 60);
    return `${String(minutes).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
  };

  const belongsToTrack = (slide) => {
    const slideTrack = slide.dataset.track || "core";
    if (slideTrack === "appendix") return true;
    if (track === "full") return true;
    if (track === "math") return slideTrack === "core" || slideTrack === "math";
    return slideTrack === "core";
  };

  const rebuildTrack = (preferredId) => {
    allSlides.forEach((slide) => slide.classList.toggle("is-filtered", !belongsToTrack(slide)));
    slides = allSlides.filter(belongsToTrack);
    talkSlides = slides.filter((slide) => !slide.classList.contains("appendix"));
    const preferred = slides.findIndex((slide) => slide.id === preferredId);
    index = preferred >= 0 ? preferred : Math.min(index, slides.length - 1);
    if (trackSelect) trackSelect.value = track;
    deck.dataset.track = track;
  };

  const currentFragments = () => [...slides[index].querySelectorAll(".fragment")];

  const updateNotes = () => {
    const slide = slides[index];
    const notes = slide.querySelector(".notes");
    noteTitle.textContent = slide.dataset.title || `${index + 1}`;
    noteBody.innerHTML = notes ? notes.innerHTML : copy.missingNotes;
    slideTime.textContent = formatTime(Number(slide.dataset.duration || 0));
    totalTime.textContent = formatTime(talkSlides.reduce((sum, item) => sum + Number(item.dataset.duration || 0), 0));
  };

  const updateUrl = () => {
    const url = new URL(window.location.href);
    url.hash = slides[index].id;
    url.searchParams.set("track", track);
    history.replaceState(null, "", url);
  };

  const render = () => {
    allSlides.forEach((slide) => {
      const active = slide === slides[index];
      slide.classList.toggle("is-active", active);
      if (!active) slide.querySelectorAll(".fragment").forEach((fragment) => fragment.classList.remove("is-visible"));
    });

    const slide = slides[index];
    if (slide.classList.contains("appendix")) {
      const appendixSlides = slides.filter((item) => item.classList.contains("appendix"));
      counter.textContent = `${copy.appendix} ${appendixSlides.indexOf(slide) + 1}`;
      progress.style.width = "100%";
    } else {
      const talkPosition = talkSlides.indexOf(slide) + 1;
      const percentage = talkSlides.length > 1 ? ((talkPosition - 1) / (talkSlides.length - 1)) * 100 : 100;
      progress.style.width = `${percentage}%`;
      counter.textContent = `${talkPosition} / ${talkSlides.length} · ${copy.tracks[track]}`;
    }
    updateNotes();
    updateUrl();
  };

  const revealNext = () => {
    const hidden = currentFragments().find((fragment) => !fragment.classList.contains("is-visible"));
    if (!hidden) return false;
    hidden.classList.add("is-visible");
    return true;
  };

  const hidePrevious = () => {
    const visible = currentFragments().filter((fragment) => fragment.classList.contains("is-visible"));
    const last = visible.at(-1);
    if (!last) return false;
    last.classList.remove("is-visible");
    return true;
  };

  const go = (nextIndex, revealAll = false) => {
    index = Math.max(0, Math.min(slides.length - 1, nextIndex));
    render();
    if (revealAll) currentFragments().forEach((fragment) => fragment.classList.add("is-visible"));
  };

  const next = () => {
    if (!startTime) startClock();
    if (!revealNext()) go(index + 1);
  };

  const previous = () => {
    if (!hidePrevious()) go(index - 1, true);
  };

  const startClock = () => {
    if (startTime) return;
    startTime = Date.now();
    timer = window.setInterval(() => {
      clock.textContent = formatTime((Date.now() - startTime) / 1000);
    }, 1000);
  };

  const toggleNotes = (force) => {
    const open = typeof force === "boolean" ? force : !panel.classList.contains("is-open");
    panel.classList.toggle("is-open", open);
  };

  const toggleOverview = () => {
    overview = !overview;
    deck.classList.toggle("is-overview", overview);
  };

  const toggleFullscreen = async () => {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen?.();
    else await document.exitFullscreen?.();
  };

  const isPrime = (number) => {
    if (number < 2 || !Number.isInteger(number)) return false;
    for (let divisor = 2; divisor * divisor <= number; divisor += 1) {
      if (number % divisor === 0) return false;
    }
    return true;
  };

  const gcd = (left, right) => {
    let a = Math.abs(left);
    let b = Math.abs(right);
    while (b) [a, b] = [b, a % b];
    return a;
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

  const runEulerDemo = (button) => {
    const slide = button.closest(".slide");
    const result = slide.querySelector(".terminal-result");
    button.disabled = true;
    button.textContent = copy.counting;
    result.textContent = "n = 0, 1, 2, 3…";

    let found = null;
    for (let n = 0; n < 200; n += 1) {
      const value = n * n + n + 41;
      if (!isPrime(value)) {
        found = { n, value };
        break;
      }
    }
    window.setTimeout(() => {
      result.textContent = `n = ${found.n} → ${found.value} = 41²`;
      button.textContent = copy.counterexampleFound;
      slide.querySelectorAll(".fragment").forEach((fragment) => fragment.classList.add("is-visible"));
    }, 450);
  };

  const runRectangleDemo = (button) => {
    const slide = button.closest(".slide");
    const transcript = slide.querySelector("[data-rectangle-transcript]");
    const result = slide.querySelector("[data-rectangle-result]");
    button.disabled = true;
    button.textContent = copy.rectangleWorking;
    transcript.innerHTML = "";
    copy.rectangleLines.forEach(([type, text], lineIndex) => {
      window.setTimeout(() => {
        const line = document.createElement("p");
        line.className = `terminal-line--${type}`;
        line.textContent = text;
        transcript.appendChild(line);
        if (lineIndex === copy.rectangleLines.length - 1) {
          button.textContent = copy.rectangleDone;
          result.classList.add("is-visible");
        }
      }, lineIndex * 150);
    });
  };

  const runFermatDemo = (button) => {
    const slide = button.closest(".slide");
    const transcript = slide.querySelector("[data-fermat-transcript]");
    const conclusion = slide.querySelector("[data-fermat-conclusion]");
    const offline = slide.querySelector("[data-fermat-offline]");
    button.disabled = true;
    button.textContent = copy.fermatWorking;

    let found = null;
    for (let n = 4; n < 400; n += 1) {
      if (!isPrime(n) && gcd(2, n) === 1 && modPow(2, n - 1, n) === 1n) {
        found = n;
        break;
      }
    }
    const lines = copy.fermatLines.map(([type, text]) => [type, text.replace("341", String(found))]);
    transcript.innerHTML = "";
    lines.forEach(([type, text], lineIndex) => {
      window.setTimeout(() => {
        const line = document.createElement("p");
        line.className = `terminal-line--${type}`;
        line.textContent = text;
        transcript.appendChild(line);
        if (lineIndex === lines.length - 1) {
          button.textContent = copy.fermatDone;
          conclusion.classList.add("is-visible");
          offline.classList.add("is-visible");
        }
      }, lineIndex * 180);
    });
  };

  document.querySelector("[data-next]")?.addEventListener("click", next);
  document.querySelector("[data-prev]")?.addEventListener("click", previous);
  document.querySelector("[data-notes-toggle]")?.addEventListener("click", () => toggleNotes());
  document.querySelector("[data-notes-close]")?.addEventListener("click", () => toggleNotes(false));
  document.querySelector("[data-overview-toggle]")?.addEventListener("click", toggleOverview);
  document.querySelector("[data-fullscreen-toggle]")?.addEventListener("click", toggleFullscreen);
  document.querySelector("[data-run-demo]")?.addEventListener("click", (event) => runEulerDemo(event.currentTarget));
  document.querySelector("[data-run-rectangle-demo]")?.addEventListener("click", (event) => runRectangleDemo(event.currentTarget));
  document.querySelector("[data-run-fermat-demo]")?.addEventListener("click", (event) => runFermatDemo(event.currentTarget));

  trackSelect?.addEventListener("change", (event) => {
    const currentId = slides[index]?.id;
    track = event.currentTarget.value;
    window.localStorage.setItem("presentation-track", track);
    rebuildTrack(currentId);
    render();
  });

  allSlides.forEach((slide) => {
    slide.addEventListener("click", () => {
      if (!overview || slide.classList.contains("is-filtered")) return;
      const target = slides.indexOf(slide);
      toggleOverview();
      go(target);
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.target.matches("button, a, input, textarea, select, option")) return;
    if (["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"].includes(event.key)) {
      event.preventDefault();
      next();
    } else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(event.key)) {
      event.preventDefault();
      previous();
    } else if (event.key.toLowerCase() === "n") toggleNotes();
    else if (event.key.toLowerCase() === "o") toggleOverview();
    else if (event.key.toLowerCase() === "f") toggleFullscreen();
    else if (event.key === "Home") go(0);
    else if (event.key === "End") go(talkSlides.length - 1, true);
  });

  let touchStartX = 0;
  document.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0].screenX;
  }, { passive: true });
  document.addEventListener("touchend", (event) => {
    const delta = event.changedTouches[0].screenX - touchStartX;
    if (Math.abs(delta) > 60) delta < 0 ? next() : previous();
  }, { passive: true });

  const hashId = window.location.hash.slice(1);
  const hashSlide = allSlides.find((slide) => slide.id === hashId);
  if (hashSlide && !belongsToTrack(hashSlide)) {
    track = hashSlide.dataset.track === "technical" ? "full" : "math";
  }
  rebuildTrack(hashId);
  render();
})();
