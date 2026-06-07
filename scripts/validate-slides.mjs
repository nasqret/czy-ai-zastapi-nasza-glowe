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

const validateDeck = async (language) => {
  const htmlPath = resolve(root, language, "index.html");
  const html = await readFile(htmlPath, "utf8");
  const label = language.toUpperCase();
  const slideTags = [...html.matchAll(/<section class="([^"]*\bslide\b[^"]*)" id="([^"]+)" data-title="([^"]+)" data-duration="(\d+)">/g)];
  const talkSlides = slideTags.filter((match) => !match[1].split(/\s+/).includes("appendix"));
  const appendixSlides = slideTags.filter((match) => match[1].split(/\s+/).includes("appendix"));
  const durations = talkSlides.map((match) => Number(match[4]));
  const ids = slideTags.map((match) => match[2]);

  check(talkSlides.length === 22, `${label}: 22 slajdy główne (jest ${talkSlides.length})`);
  check(appendixSlides.length === 2, `${label}: 2 slajdy dodatkowe (jest ${appendixSlides.length})`);
  check(durations.reduce((sum, value) => sum + value, 0) === 2100, `${label}: czas główny wynosi dokładnie 35:00`);
  check(new Set(ids).size === ids.length, `${label}: identyfikatory slajdów są unikalne`);

  const notesCount = (html.match(/<aside class="notes">/g) || []).length;
  check(notesCount === slideTags.length, `${label}: każdy slajd ma notatki (${notesCount}/${slideTags.length})`);

  const imageSources = [...html.matchAll(/<img[^>]+src="([^"]+)"/g)].map((match) => match[1]);
  const scriptSources = [...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map((match) => match[1]);
  const styleSources = [...html.matchAll(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g)].map((match) => match[1]);
  const localAssets = [...imageSources, ...scriptSources, ...styleSources].filter((source) => !source.startsWith("http"));

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
  check(html.includes("data-run-demo"), `${label}: pokaz wielomianu Eulera jest obecny`);
  check(html.includes("data-run-rectangle-demo"), `${label}: symulacja prostokątów jest obecna`);
  check(html.includes("data-run-fermat-demo"), `${label}: zabawa z Fermatem jest obecna`);
  check(html.includes("341 = 11 · 31"), `${label}: kontrprzykład 341 jest obecny`);
  check(html.includes("Bartosz Naskręcki"), `${label}: autor jest podany`);
  check(html.includes("UAM/CCAI"), `${label}: afiliacja jest podana`);
  check(html.includes("Copyright © 2026 Bartosz Naskręcki. All rights reserved."), `${label}: pełny copyright jest obecny`);
  check(html.includes('class="deck-language"'), `${label}: przełącznik języka jest obecny`);
  check(html.includes("√d<sub>k</sub>"), `${label}: wzór atencji używa skali √d_k`);
  check(html.includes("data-speaker-panel"), `${label}: panel notatek jest obecny`);

  if (language === "pl") {
    check(html.includes("Warszawa, 8.06.2026"), "PL: miejsce i data wykładu są poprawne");
  } else {
    check(html.includes("Warsaw, 8 June 2026"), "EN: miejsce i data wykładu są poprawne");
    const polishPhrases = [
      "Szybka sonda",
      "Notatki prowadzącego",
      "Zlecaj pracę",
      "Najpierw pozwól",
      "Kliknij przycisk",
      "Wróć do odpowiedzi",
    ];
    check(polishPhrases.every((phrase) => !html.includes(phrase)), "EN: treść i notatki nie zawierają polskich fragmentów");
  }
};

await validateDeck("pl");
await validateDeck("en");

const landing = await readFile(resolve(root, "index.html"), "utf8");
check(landing.includes('href="pl/"') && landing.includes('href="en/"'), "landing: zawiera obie wersje prezentacji");
check(landing.includes('href="experiments/pl/"') && landing.includes('href="experiments/en/"'), "landing: zawiera oba laboratoria");
check(landing.includes("Copyright © 2026 Bartosz Naskręcki. All rights reserved."), "landing: pełny copyright jest obecny");
check(landing.includes('data-language="pl"') && landing.includes('data-language="en"'), "landing: przełącznik języka jest obecny");

const labs = ["index", "rectangles", "fermat", "euler", "proof", "prompt"];
for (const language of ["pl", "en"]) {
  for (const lab of labs) {
    const path = resolve(root, "experiments", language, `${lab}.html`);
    try {
      const html = await readFile(path, "utf8");
      check(html.includes("data-lab-root"), `${language.toUpperCase()}: istnieje laboratorium ${lab}`);
      check(html.includes('src="../app.js"'), `${language.toUpperCase()}: laboratorium ${lab} ładuje wspólną logikę`);
    } catch {
      failures.push(`${language.toUpperCase()}: brak laboratorium ${lab}`);
    }
  }
}

const css = await readFile(resolve(root, "styles.css"), "utf8");
const js = await readFile(resolve(root, "app.js"), "utf8");
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

if (failures.length) {
  console.error("Walidacja nieudana:");
  failures.forEach((message) => console.error(`  ✗ ${message}`));
  process.exit(1);
}

console.log(`Walidacja udana: ${checks.length} kontroli.`);
