import { readFile, access } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const htmlPath = resolve(root, "index.html");
const html = await readFile(htmlPath, "utf8");

const failures = [];
const checks = [];

const check = (condition, message) => {
  if (condition) checks.push(message);
  else failures.push(message);
};

const slideTags = [...html.matchAll(/<section class="([^"]*\bslide\b[^"]*)" id="([^"]+)" data-title="([^"]+)" data-duration="(\d+)">/g)];
const talkSlides = slideTags.filter((match) => !match[1].split(/\s+/).includes("appendix"));
const appendixSlides = slideTags.filter((match) => match[1].split(/\s+/).includes("appendix"));
const durations = talkSlides.map((match) => Number(match[4]));
const ids = slideTags.map((match) => match[2]);

check(talkSlides.length === 21, `21 slajdów głównych (jest ${talkSlides.length})`);
check(appendixSlides.length === 2, `2 slajdy dodatkowe (jest ${appendixSlides.length})`);
check(durations.reduce((sum, value) => sum + value, 0) === 2100, "czas główny wynosi dokładnie 35:00");
check(new Set(ids).size === ids.length, "identyfikatory slajdów są unikalne");

const notesCount = (html.match(/<aside class="notes">/g) || []).length;
check(notesCount === slideTags.length, `każdy slajd ma notatki (${notesCount}/${slideTags.length})`);

const imageSources = [...html.matchAll(/<img[^>]+src="([^"]+)"/g)].map((match) => match[1]);
const scriptSources = [...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map((match) => match[1]);
const styleSources = [...html.matchAll(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g)].map((match) => match[1]);
const localAssets = [...imageSources, ...scriptSources, ...styleSources].filter((source) => !source.startsWith("http"));

for (const asset of localAssets) {
  try {
    await access(resolve(root, asset));
    checks.push(`istnieje zasób ${asset}`);
  } catch {
    failures.push(`brak zasobu ${asset}`);
  }
}

const imagesWithoutAlt = [...html.matchAll(/<img\b([^>]*)>/g)]
  .filter((match) => !/\balt="[^"]*"/.test(match[1]));
check(imagesWithoutAlt.length === 0, "każdy obraz ma tekst alternatywny");

check(!/https?:\/\/[^"']+\.(?:js|css)/.test(html), "brak zewnętrznych zależności JS/CSS");
check(html.includes('data-run-demo'), "pokaz wielomianu Eulera jest obecny");
check(html.includes('data-run-rectangle-demo'), "symulacja liczenia prostokątów przez Codex jest obecna");
check(html.includes('data-speaker-panel'), "panel notatek jest obecny");
check(html.includes('prefers-reduced-motion') === false, "HTML nie zawiera przypadkowego CSS inline");

const css = await readFile(resolve(root, "styles.css"), "utf8");
const js = await readFile(resolve(root, "app.js"), "utf8");
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
checks.forEach((message) => console.log(`  ✓ ${message}`));
