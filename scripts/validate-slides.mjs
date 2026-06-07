import { readFile, access } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const failures = [];
const checks = [];

const check = (condition, message) => {
  if (condition) checks.push(message);
  else failures.push(message);
};

const attributes = (tag) => Object.fromEntries(
  [...tag.matchAll(/([\w-]+)="([^"]*)"/g)].map((match) => [match[1], match[2]])
);

const extractSlides = (html) => [...html.matchAll(/<section\b[^>]*\bclass="[^"]*\bslide\b[^"]*"[^>]*>/g)]
  .map((match) => {
    const attrs = attributes(match[0]);
    return {
      attrs,
      classNames: (attrs.class || "").split(/\s+/).filter(Boolean),
      duration: Number(attrs["data-duration"] || 0),
      id: attrs.id,
      track: attrs["data-track"],
    };
  });

const assertStrictEnglish = (html, label, requiredEnglish = []) => {
  const withoutAuthor = html.replaceAll("Naskręcki", "Naskrecki");
  const polishDiacritics = withoutAuthor.match(/[ąćęłńóśźż]/giu) || [];
  check(polishDiacritics.length === 0, `${label}: brak polskich znaków diakrytycznych poza nazwiskiem autora`);

  const polishPhrases = [
    "Szybka sonda",
    "Notatki prowadzącego",
    "Pełne źródła",
    "Ściąga prowadzącego",
    "Możesz pominąć",
    "Wybierz ścieżkę",
    "Zlecaj pracę",
    "Najpierw pozwól",
    "Kliknij przycisk",
    "Wróć do odpowiedzi",
    "Komputer znalazł",
    "Matematyka nadal",
    "Fałszywy dowód",
    "Prostokąty",
    "Wielomian Eulera",
    "Małe twierdzenie Fermata",
  ];
  check(polishPhrases.every((phrase) => !html.includes(phrase)), `${label}: brak znanych polskich fraz`);

  if (requiredEnglish.length) {
    check(requiredEnglish.every((phrase) => html.includes(phrase)), `${label}: wszystkie kluczowe elementy są przetłumaczone`);
  }
};

const validateDeck = async (language) => {
  const htmlPath = resolve(root, language, "index.html");
  const html = await readFile(htmlPath, "utf8");
  const label = language.toUpperCase();
  const slides = extractSlides(html);
  const byTrack = (track) => slides.filter((slide) => slide.track === track);
  const core = byTrack("core");
  const math = byTrack("math");
  const technical = byTrack("technical");
  const appendix = byTrack("appendix");
  const ids = slides.map((slide) => slide.id);

  check(slides.length === 34, `${label}: 34 slajdy w DOM (jest ${slides.length})`);
  check(core.length === 22, `${label}: 22 slajdy core (jest ${core.length})`);
  check(math.length === 6, `${label}: 6 slajdów math (jest ${math.length})`);
  check(technical.length === 4, `${label}: 4 slajdy technical (jest ${technical.length})`);
  check(appendix.length === 2, `${label}: 2 slajdy appendix (jest ${appendix.length})`);
  check(core.reduce((sum, slide) => sum + slide.duration, 0) === 2100, `${label}: rdzeń trwa dokładnie 35:00`);
  check(appendix.every((slide) => slide.duration === 0 && slide.classNames.includes("appendix")), `${label}: dodatki mają czas 0 i klasę appendix`);
  check(core.length + appendix.length === 24, `${label}: profil core pokazuje 24 slajdy z dodatkami`);
  check(core.length + math.length + appendix.length === 30, `${label}: profil math pokazuje 30 slajdów z dodatkami`);
  check(slides.length === 34, `${label}: profil full pokazuje 34 slajdy`);
  check(ids.every(Boolean) && new Set(ids).size === ids.length, `${label}: identyfikatory slajdów są obecne i unikalne`);

  const notesCount = (html.match(/<aside class="notes">/g) || []).length;
  check(notesCount === slides.length, `${label}: każdy slajd ma notatki (${notesCount}/${slides.length})`);

  const imageSources = [...html.matchAll(/<img[^>]+src="([^"]+)"/g)].map((match) => match[1]);
  const scriptSources = [...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map((match) => match[1]);
  const styleSources = [...html.matchAll(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g)].map((match) => match[1]);
  const localAssets = [...imageSources, ...scriptSources, ...styleSources]
    .filter((source) => !source.startsWith("http") && !source.startsWith("data:"));

  for (const asset of localAssets) {
    try {
      await access(resolve(dirname(htmlPath), asset));
      checks.push(`${label}: istnieje zasób ${asset}`);
    } catch {
      failures.push(`${label}: brak zasobu ${asset}`);
    }
  }

  const imagesWithoutAlt = [...html.matchAll(/<img\b([^>]*)>/g)]
    .filter((match) => !/\balt="[^"]*"/.test(match[1]));
  check(imagesWithoutAlt.length === 0, `${label}: każdy obraz ma tekst alternatywny`);
  check(!/https?:\/\/[^"']+\.(?:js|css)/.test(html), `${label}: brak zewnętrznych zależności JS/CSS`);
  check(html.includes('data-track-select'), `${label}: selektor profilu jest obecny`);
  check(html.includes('value="core"') && html.includes('value="math"') && html.includes('value="full"'), `${label}: trzy profile są dostępne`);
  check(html.includes('id="uwaga-wzor"'), `${label}: techniczny slajd wzoru uwagi jest obecny`);
  check(
    html.includes("softmax((QK<sup>T</sup> + M) / √d<sub>k</sub>)V"),
    `${label}: wzór uwagi zawiera maskę M i skalę √d_k`
  );
  check(html.includes('id="prostokaty"') && html.includes("m×k"), `${label}: problem prostokątów m×k jest obecny`);
  check(html.includes("C(m+1,2)") && html.includes("C(k+1,2)"), `${label}: wzór na prostokąty używa obu wymiarów`);
  check(html.includes("data-run-demo"), `${label}: pokaz wielomianu Eulera jest obecny`);
  check(html.includes("data-run-rectangle-demo"), `${label}: symulacja prostokątów jest obecna`);
  check(html.includes("data-run-fermat-demo"), `${label}: zabawa z Fermatem jest obecna`);
  const coprimeCondition = language === "pl" ? "NWD(a,n)=1" : "gcd(a,n)=1";
  check(html.includes(coprimeCondition) && html.includes("a<sup>n−1</sup> ≡ 1 (mod n)"), `${label}: standardowy test Fermata podaje warunek względnej pierwszości`);
  check(html.includes("341 = 11 · 31") || html.includes("341 = 11 × 31"), `${label}: kontrprzykład 341 jest obecny`);
  check(html.includes("Bartosz Naskręcki"), `${label}: autor jest podany`);
  check(html.includes("UAM/CCAI"), `${label}: afiliacja jest podana`);
  check(html.includes("Copyright © 2026 Bartosz Naskręcki. All rights reserved."), `${label}: pełny copyright jest obecny`);
  check(html.includes('class="deck-language"'), `${label}: przełącznik języka jest obecny`);
  check(html.includes("data-speaker-panel"), `${label}: panel notatek jest obecny`);
  check(html.includes('aria-live="polite"'), `${label}: dynamiczne wyniki mają aria-live`);
  check(/<noscript>[\s\S]+<\/noscript>/.test(html), `${label}: istnieje komunikat bez JavaScriptu`);

  if (language === "pl") {
    check(html.includes("Warszawa, 8.06.2026"), "PL: miejsce i data wykładu są poprawne");
  } else {
    check(html.includes("Warsaw, 8 June 2026"), "EN: miejsce i data wykładu są poprawne");
    assertStrictEnglish(html, label, [
      "Will AI replace our minds?",
      "Attention formula",
      "Core 35 min",
      "Core + mathematics",
      "Full sources",
      "Speaker cheat sheet",
      "The computer found:",
      "Mathematics still needs:",
    ]);
  }
};

await validateDeck("pl");
await validateDeck("en");

const landing = await readFile(resolve(root, "index.html"), "utf8");
const directCards = [...landing.matchAll(/<a class="experiment-card"[\s\S]*?<\/a>/g)];
check(landing.includes('href="pl/"') && landing.includes('href="en/"'), "landing: zawiera obie wersje prezentacji");
check(directCards.length === 5, `landing: zawiera pięć bezpośrednich kart laboratoriów (jest ${directCards.length})`);
for (const lab of ["rectangles", "fermat", "euler", "proof", "prompt"]) {
  check(
    landing.includes(`data-href-pl="experiments/pl/${lab}.html"`)
      && landing.includes(`data-href-en="experiments/en/${lab}.html"`),
    `landing: karta ${lab} prowadzi bezpośrednio do obu lokalizacji`
  );
}
check(landing.includes("Copyright © 2026 Bartosz Naskręcki. All rights reserved."), "landing: pełny copyright jest obecny");
check(landing.includes('data-language="pl"') && landing.includes('data-language="en"'), "landing: przełącznik języka jest obecny");

const labNames = ["index", "rectangles", "fermat", "euler", "proof", "prompt"];
for (const language of ["pl", "en"]) {
  for (const lab of labNames) {
    const path = resolve(root, "experiments", language, `${lab}.html`);
    try {
      const html = await readFile(path, "utf8");
      check(html.includes("data-lab-root"), `${language.toUpperCase()}: istnieje laboratorium ${lab}`);
      check(html.includes('src="../app.js"'), `${language.toUpperCase()}: laboratorium ${lab} ładuje wspólną logikę`);
      check(/<noscript>[\s\S]+<\/noscript>/.test(html), `${language.toUpperCase()}: laboratorium ${lab} ma treść noscript`);
      if (language === "en") assertStrictEnglish(html, `EN LAB ${lab}`);
    } catch {
      failures.push(`${language.toUpperCase()}: brak laboratorium ${lab}`);
    }
  }
}

const css = await readFile(resolve(root, "styles.css"), "utf8");
const js = await readFile(resolve(root, "app.js"), "utf8");
const labJs = await readFile(resolve(root, "experiments", "app.js"), "utf8");
for (const asset of ["scripts/fermat_demo.py", "scripts/verify_math.py", "experiments/app.js", "experiments/experiments.css", ".nojekyll", "LICENSE"]) {
  try {
    await access(resolve(root, asset));
    checks.push(`istnieje ${asset}`);
  } catch {
    failures.push(`brak ${asset}`);
  }
}
check(css.includes("@media print"), "istnieje tryb druku");
check(css.includes("prefers-reduced-motion"), "animacje respektują ograniczenie ruchu");
check(js.includes("requestFullscreen"), "pełny ekran jest obsługiwany");
check(js.includes("touchstart") && js.includes("touchend"), "nawigacja dotykowa jest obsługiwana");
check(labJs.includes('aria-live="polite"'), "laboratoria oznaczają dynamiczne wyniki przez aria-live");
check(labJs.includes("gcd(base, n) === 1") && labJs.includes("modPow(base, n - 1, n)"), "laboratorium Fermata implementuje standardowy test z gcd");
check(labJs.includes('classifyInteger') && labJs.includes('neither prime nor composite'), "laboratorium Eulera rozróżnia 1 od liczb złożonych");
check(labJs.includes("data-proof-hint") && labJs.includes("Hint 3:"), "audyt dowodu ma stopniowane wskazówki");
for (const subject of ["math", "history", "biology", "literature", "programming"]) {
  check(labJs.includes(`${subject}:`), `Prompt Dojo zawiera dziedzinę ${subject}`);
}

if (failures.length) {
  console.error("Walidacja nieudana:");
  failures.forEach((message) => console.error(`  ✗ ${message}`));
  process.exit(1);
}

console.log(`Walidacja udana: ${checks.length} kontroli.`);
