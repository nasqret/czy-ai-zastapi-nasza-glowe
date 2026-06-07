from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "test-results" / "slides"
BASE_URL = "http://127.0.0.1:4173"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PRESENTATIONS = {"pl": "/pl/", "en": "/en/"}

ACTIVATE_SCRIPT = """(id) => {
    const slides = [...document.querySelectorAll('.slide')];
    slides.forEach((slide) => {
      slide.classList.toggle('is-active', slide.id === id);
      if (slide.id === id) {
        slide.querySelectorAll('.fragment').forEach((fragment) => fragment.classList.add('is-visible'));
      }
    });
}"""

OVERFLOW_SCRIPT = """(slide) => {
    const frame = slide.getBoundingClientRect();
    const selectors = [
      'h1', 'h2', 'h3', 'p', 'blockquote', 'pre', 'button',
      '.poll-card', '.training-card', '.reason', '.proof-card',
      '.crime-scene', '.axis-card', '.loop-node', '.learning-step',
      '.recipe-row', '.rules-list li', '.sources-grid a',
      '.backup-cards article', '.formula-card', '.token-machine',
      '.board-panel', '.candidate-card', '.codex-terminal',
      '.codex-run-prompt', '.codex-run-plan', '.code-diff',
      '.chat-message', '.practice-prompt', '.learning-in-practice li',
      '.fermat-lab', '.fermat-conclusion', '.fermat-offline',
      '.fermat-rule-strip', '.fermat-rule-strip span', '.title-meta'
    ];
    return [...slide.querySelectorAll(selectors.join(','))].flatMap((node) => {
      const style = getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      if (style.display === 'none' || style.visibility === 'hidden' || rect.width === 0 || rect.height === 0) return [];
      const outside = rect.left < frame.left - 2 || rect.right > frame.right + 2 ||
        rect.top < frame.top - 2 || rect.bottom > frame.bottom + 2;
      return outside ? [{node: node.tagName.toLowerCase(), rect: [rect.left, rect.top, rect.right, rect.bottom].map(Math.round)}] : [];
    });
}"""

OVERLAP_SCRIPT = """(slide) => {
    const pairs = slide.id === 'dziewiec-dziewiec'
      ? [['.proof-split', '.proof-takeaway']]
      : slide.id === 'dowod-jeden-rowna-sie-dwa'
        ? [['.bad-proof', '.codex-audit'], ['.codex-audit', '.bad-proof-takeaway']]
        : slide.id === 'idee'
          ? [['.slide-header', '.rectangle-idea-layout'], ['.board-panel', '.case-principles'], ['.codex-candidates', '.case-principles']]
        : slide.id === 'codex'
          ? [['.slide-header', '.codex-run-grid'], ['.codex-run-grid', '.codex-result-line']]
        : slide.id === 'jak-sie-uczyc'
          ? [['.slide-header', '.tutor-case']]
        : slide.id === 'fermat-zabawa'
          ? [['.slide-header', '.fermat-lab'], ['.fermat-lab', '.fermat-rule-strip']]
        : [];
    return pairs.flatMap(([firstSelector, secondSelector]) => {
      const first = slide.querySelector(firstSelector);
      const second = slide.querySelector(secondSelector);
      if (!first || !second) return [];
      const a = first.getBoundingClientRect();
      const b = second.getBoundingClientRect();
      return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top
        ? [{first: firstSelector, second: secondSelector}] : [];
    });
}"""


def exercise_interactions(page, language: str, failures: list[str]) -> None:
    url = f"{BASE_URL}/{language}/"
    page.goto(f"{url}?interaction-test=1#start", wait_until="networkidle")
    first_fragment = page.locator("#sonda .fragment").first
    page.keyboard.press("ArrowRight")
    if page.locator(".slide.is-active").get_attribute("id") != "sonda":
        failures.append(f"{language}: ArrowRight nie przechodzi do drugiego slajdu")
    page.keyboard.press("ArrowRight")
    if not first_fragment.evaluate("(node) => node.classList.contains('is-visible')"):
        failures.append(f"{language}: ArrowRight nie ujawnia fragmentu")
    page.keyboard.press("ArrowLeft")
    if first_fragment.evaluate("(node) => node.classList.contains('is-visible')"):
        failures.append(f"{language}: ArrowLeft nie ukrywa fragmentu")

    page.keyboard.press("n")
    if not page.locator("[data-speaker-panel]").evaluate("(node) => node.classList.contains('is-open')"):
        failures.append(f"{language}: klawisz N nie otwiera notatek")
    page.keyboard.press("n")
    page.keyboard.press("o")
    if not page.locator(".deck").evaluate("(node) => node.classList.contains('is-overview')"):
        failures.append(f"{language}: klawisz O nie otwiera przeglądu")
    page.locator("#euler").click()
    page.locator("[data-run-demo]").click()
    page.wait_for_timeout(900)
    result = page.locator("#euler .terminal-result").inner_text()
    if "n = 40" not in result or "41²" not in result:
        failures.append(f"{language}: demo Eulera zwróciło {result}")

    page.goto(f"{url}?rectangle-interaction=1#codex", wait_until="networkidle")
    page.locator("#codex .fragment").evaluate_all("(nodes) => nodes.forEach((node) => node.classList.add('is-visible'))")
    page.locator("[data-run-rectangle-demo]").click()
    page.wait_for_timeout(1750)
    output = page.locator("[data-rectangle-transcript]").inner_text()
    if not all(value in output for value in ["784", "FAIL", "1296"]):
        failures.append(f"{language}: niepełna symulacja prostokątów: {output}")

    page.goto(f"{url}?fermat-interaction=1#fermat-zabawa", wait_until="networkidle")
    page.locator("#fermat-zabawa .fragment").evaluate_all("(nodes) => nodes.forEach((node) => node.classList.add('is-visible'))")
    page.locator("[data-run-fermat-demo]").click()
    page.wait_for_timeout(1350)
    output = page.locator("[data-fermat-transcript]").inner_text()
    transfer = page.locator("[data-fermat-offline]").inner_text()
    if "341 = 11 × 31" not in output or "mod 341 = 0" not in output:
        failures.append(f"{language}: symulacja Fermata nie znalazła 341: {output}")
    if not all(value in transfer for value in ["3", "100", "4"]):
        failures.append(f"{language}: brak samodzielnego rachunku Fermata: {transfer}")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    report: list[dict[str, object]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=CHROME, args=["--disable-gpu"])
        for language, path in PRESENTATIONS.items():
            language_output = OUTPUT / language
            language_output.mkdir(parents=True, exist_ok=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            console_errors: list[str] = []
            page_errors: list[str] = []
            page.on("console", lambda message, errors=console_errors: errors.append(message.text) if message.type == "error" else None)
            page.on("pageerror", lambda error, errors=page_errors: errors.append(str(error)))

            response = page.goto(f"{BASE_URL}{path}", wait_until="networkidle")
            if response is None or not response.ok:
                failures.append(f"{language}: nie udało się otworzyć prezentacji")
                page.close()
                continue
            ids = page.locator(".slide").evaluate_all("(nodes) => nodes.map((node) => node.id)")
            if len(ids) != 24:
                failures.append(f"{language}: oczekiwano 24 slajdów, znaleziono {len(ids)}")

            for width, height in [(1440, 900), (1366, 768), (1920, 1080)]:
                page.set_viewport_size({"width": width, "height": height})
                page.goto(f"{BASE_URL}{path}?viewport={width}x{height}", wait_until="networkidle")
                for position, slide_id in enumerate(ids, start=1):
                    page.evaluate(ACTIVATE_SCRIPT, slide_id)
                    if slide_id == "codex":
                        page.locator("[data-run-rectangle-demo]").click()
                        page.wait_for_timeout(1750)
                    if slide_id == "fermat-zabawa":
                        page.locator("[data-run-fermat-demo]").click()
                        page.wait_for_timeout(1350)
                    overflow = page.locator(f"#{slide_id}").evaluate(OVERFLOW_SCRIPT)
                    overlap = page.locator(f"#{slide_id}").evaluate(OVERLAP_SCRIPT)
                    if overflow:
                        failures.append(f"{language}: slajd {position} ({slide_id}) poza kadrem {width}×{height}: {overflow}")
                    if overlap:
                        failures.append(f"{language}: slajd {position} ({slide_id}) ma kolizję {width}×{height}: {overlap}")
                    if width == 1440:
                        screenshot = language_output / f"{position:02d}-{slide_id}.png"
                        page.screenshot(path=str(screenshot), full_page=False)
                        report.append({"language": language, "number": position, "id": slide_id, "overflow": overflow, "overlap": overlap})

            exercise_interactions(page, language, failures)
            if console_errors:
                failures.append(f"{language}: błędy konsoli: {console_errors}")
            if page_errors:
                failures.append(f"{language}: błędy strony: {page_errors}")
            page.close()
        browser.close()

    report_path = ROOT / "test-results" / "report.json"
    report_path.write_text(json.dumps({"slides": report, "failures": failures}, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        print("Test slajdów nieudany:")
        for failure in failures:
            print(f"  ✗ {failure}")
        return 1
    print("Test slajdów udany: 48 slajdów, 3 rozdzielczości, wszystkie interakcje.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
