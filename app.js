(() => {
  "use strict";

  const deck = document.querySelector(".deck");
  const slides = [...document.querySelectorAll(".slide")];
  const talkSlides = slides.filter((slide) => !slide.classList.contains("appendix"));
  const progress = document.querySelector("[data-progress]");
  const counter = document.querySelector("[data-counter]");
  const clock = document.querySelector("[data-clock]");
  const panel = document.querySelector("[data-speaker-panel]");
  const noteTitle = document.querySelector("[data-note-title]");
  const noteBody = document.querySelector("[data-note-body]");
  const slideTime = document.querySelector("[data-slide-time]");
  const totalTime = document.querySelector("[data-total-time]");
  const language = document.documentElement.lang === "en" ? "en" : "pl";
  const copy = {
    pl: {
      appendix: "dodatek",
      missingNotes: "Brak notatek.",
      counting: "Liczymy…",
      counterexampleFound: "Znaleziono kontrprzykład",
      eulerProgress: "n = 0, 1, 2, 3…",
      rectangleWorking: "Codex pracuje…",
      rectangleDone: "Testy zakończone",
      rectangleLines: [
        ["plan", "[PLAN] Prostokąt wyznaczają 2 linie pionowe i 2 poziome."],
        ["run", "[RUN 1] count_rectangles_buggy(8) = 784"],
        ["fail", "[TEST] plansza 1x1: oczekiwano 1, otrzymano 0 -> FAIL"],
        ["diagnosis", "[DIAGNOZA] Plansza nxn ma n+1 linii, nie n."],
        ["patch", "[POPRAWKA] range(n) -> range(n + 1)"],
        ["pass", "[TEST] plansza 1x1: 1 -> PASS"],
        ["pass", "[TEST] plansza 2x2: 9 -> PASS"],
        ["pass", "[TEST] plansza 8x8: 1296 -> PASS"],
        ["result", "[WYNIK] C(9,2)^2 = 36^2 = 1296"]
      ],
      fermatWorking: "Codex sprawdza…",
      fermatDone: "Kontrprzykład znaleziony",
      fermatLines: [
        ["plan", "[HIPOTEZA] p | (2^p - 2)  ⇔  p jest pierwsza?"],
        ["run", "[TEST] p = 2, 3, 5, 7, 11 -> działa"],
        ["diagnosis", "[SZUKAM] liczby złożone n < 400..."],
        ["fail", "[KONTRPRZYKŁAD] 341 = 11 × 31"],
        ["pass", "[SPRAWDZENIE] (2^341 - 2) mod 341 = 0"],
        ["result", "[WERDYKT] Test dla podstawy 2 nie rozpoznaje pierwszości."]
      ]
    },
    en: {
      appendix: "appendix",
      missingNotes: "No speaker notes.",
      counting: "Calculating…",
      counterexampleFound: "Counterexample found",
      eulerProgress: "n = 0, 1, 2, 3…",
      rectangleWorking: "Codex is working…",
      rectangleDone: "Tests completed",
      rectangleLines: [
        ["plan", "[PLAN] A rectangle is determined by 2 vertical and 2 horizontal lines."],
        ["run", "[RUN 1] count_rectangles_buggy(8) = 784"],
        ["fail", "[TEST] 1x1 board: expected 1, got 0 -> FAIL"],
        ["diagnosis", "[DIAGNOSIS] An nxn board has n+1 lines, not n."],
        ["patch", "[PATCH] range(n) -> range(n + 1)"],
        ["pass", "[TEST] 1x1 board: 1 -> PASS"],
        ["pass", "[TEST] 2x2 board: 9 -> PASS"],
        ["pass", "[TEST] 8x8 board: 1296 -> PASS"],
        ["result", "[RESULT] C(9,2)^2 = 36^2 = 1296"]
      ],
      fermatWorking: "Codex is checking…",
      fermatDone: "Counterexample found",
      fermatLines: [
        ["plan", "[HYPOTHESIS] p | (2^p - 2)  ⇔  p is prime?"],
        ["run", "[TEST] p = 2, 3, 5, 7, 11 -> passes"],
        ["diagnosis", "[SEARCH] composite numbers n < 400..."],
        ["fail", "[COUNTEREXAMPLE] 341 = 11 × 31"],
        ["pass", "[CHECK] (2^341 - 2) mod 341 = 0"],
        ["result", "[VERDICT] The base-2 test does not characterize primes."]
      ]
    }
  }[language];

  let index = 0;
  let startTime = null;
  let timer = null;
  let overview = false;

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const rest = Math.floor(seconds % 60);
    return `${String(minutes).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
  };

  const currentFragments = () => [...slides[index].querySelectorAll(".fragment")];

  const updateNotes = () => {
    const slide = slides[index];
    const notes = slide.querySelector(".notes");
    noteTitle.textContent = slide.dataset.title || `Slajd ${index + 1}`;
    noteBody.innerHTML = notes ? notes.innerHTML : copy.missingNotes;
    slideTime.textContent = formatTime(Number(slide.dataset.duration || 0));
    const planned = talkSlides.reduce((sum, item) => sum + Number(item.dataset.duration || 0), 0);
    totalTime.textContent = formatTime(planned);
  };

  const updateUrl = () => {
    const id = slides[index].id;
    if (id) history.replaceState(null, "", `#${id}`);
  };

  const render = () => {
    slides.forEach((slide, slideIndex) => {
      slide.classList.toggle("is-active", slideIndex === index);
      if (slideIndex !== index) {
        slide.querySelectorAll(".fragment").forEach((fragment) => fragment.classList.remove("is-visible"));
      }
    });

    const talkPosition = Math.min(index + 1, talkSlides.length);
    const percentage = talkSlides.length > 1
      ? ((talkPosition - 1) / (talkSlides.length - 1)) * 100
      : 100;
    progress.style.width = `${percentage}%`;
    counter.textContent = slides[index].classList.contains("appendix")
      ? `${copy.appendix} ${index - talkSlides.length + 1}`
      : `${talkPosition} / ${talkSlides.length}`;
    updateNotes();
    updateUrl();
  };

  const revealNext = () => {
    const hidden = currentFragments().find((fragment) => !fragment.classList.contains("is-visible"));
    if (hidden) {
      hidden.classList.add("is-visible");
      return true;
    }
    return false;
  };

  const hidePrevious = () => {
    const visible = currentFragments().filter((fragment) => fragment.classList.contains("is-visible"));
    const last = visible.at(-1);
    if (last) {
      last.classList.remove("is-visible");
      return true;
    }
    return false;
  };

  const go = (nextIndex, revealAll = false) => {
    index = Math.max(0, Math.min(slides.length - 1, nextIndex));
    render();
    if (revealAll) {
      currentFragments().forEach((fragment) => fragment.classList.add("is-visible"));
    }
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
    if (!document.fullscreenElement) {
      await document.documentElement.requestFullscreen?.();
    } else {
      await document.exitFullscreen?.();
    }
  };

  const runEulerDemo = (button) => {
    const slide = button.closest(".slide");
    const result = slide.querySelector(".terminal-result");
    button.disabled = true;
    button.textContent = copy.counting;
    result.textContent = copy.eulerProgress;

    window.setTimeout(() => {
      result.textContent = "n = 40 → 1681 = 41²";
      button.textContent = copy.counterexampleFound;
      slide.querySelectorAll(".fragment").forEach((fragment) => fragment.classList.add("is-visible"));
    }, 700);
  };

  const runRectangleDemo = (button) => {
    const slide = button.closest(".slide");
    const transcript = slide.querySelector("[data-rectangle-transcript]");
    const result = slide.querySelector("[data-rectangle-result]");
    const lines = copy.rectangleLines;

    button.disabled = true;
    button.textContent = copy.rectangleWorking;
    transcript.innerHTML = "";

    lines.forEach(([type, text], lineIndex) => {
      window.setTimeout(() => {
        const line = document.createElement("p");
        line.className = `terminal-line--${type}`;
        line.textContent = text;
        transcript.appendChild(line);

        if (lineIndex === lines.length - 1) {
          button.textContent = copy.rectangleDone;
          result.classList.add("is-visible");
        }
      }, lineIndex * 180);
    });
  };

  const runFermatDemo = (button) => {
    const slide = button.closest(".slide");
    const transcript = slide.querySelector("[data-fermat-transcript]");
    const conclusion = slide.querySelector("[data-fermat-conclusion]");
    const offline = slide.querySelector("[data-fermat-offline]");
    const lines = copy.fermatLines;

    button.disabled = true;
    button.textContent = copy.fermatWorking;
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
      }, lineIndex * 210);
    });
  };

  document.querySelector("[data-next]").addEventListener("click", next);
  document.querySelector("[data-prev]").addEventListener("click", previous);
  document.querySelector("[data-notes-toggle]").addEventListener("click", () => toggleNotes());
  document.querySelector("[data-notes-close]").addEventListener("click", () => toggleNotes(false));
  document.querySelector("[data-overview-toggle]").addEventListener("click", toggleOverview);
  document.querySelector("[data-fullscreen-toggle]").addEventListener("click", toggleFullscreen);
  document.querySelector("[data-run-demo]").addEventListener("click", (event) => runEulerDemo(event.currentTarget));
  document.querySelector("[data-run-rectangle-demo]").addEventListener("click", (event) => runRectangleDemo(event.currentTarget));
  document.querySelector("[data-run-fermat-demo]").addEventListener("click", (event) => runFermatDemo(event.currentTarget));

  slides.forEach((slide, slideIndex) => {
    slide.addEventListener("click", () => {
      if (overview) {
        toggleOverview();
        go(slideIndex);
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.target.matches("button, a")) return;
    if (["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"].includes(event.key)) {
      event.preventDefault();
      next();
    } else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(event.key)) {
      event.preventDefault();
      previous();
    } else if (event.key.toLowerCase() === "n") {
      toggleNotes();
    } else if (event.key.toLowerCase() === "o") {
      toggleOverview();
    } else if (event.key.toLowerCase() === "f") {
      toggleFullscreen();
    } else if (event.key === "Home") {
      go(0);
    } else if (event.key === "End") {
      go(talkSlides.length - 1, true);
    }
  });

  let touchStartX = 0;
  document.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0].screenX;
  }, { passive: true });
  document.addEventListener("touchend", (event) => {
    const delta = event.changedTouches[0].screenX - touchStartX;
    if (Math.abs(delta) > 60) delta < 0 ? next() : previous();
  }, { passive: true });

  const hashIndex = slides.findIndex((slide) => `#${slide.id}` === window.location.hash);
  if (hashIndex >= 0) index = hashIndex;
  render();
})();
