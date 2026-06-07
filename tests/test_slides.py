from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "test-results" / "slides"
URL = "http://127.0.0.1:4173"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ACTIVATE_SCRIPT = """(id) => {
    const slides = [...document.querySelectorAll('.slide')];
    slides.forEach((slide) => {
      slide.classList.toggle('is-active', slide.id === id);
      if (slide.id === id) {
        slide.querySelectorAll('.fragment').forEach((fragment) => {
          fragment.classList.add('is-visible');
        });
      }
    });
}"""

OVERFLOW_SCRIPT = """(slide) => {
    const slideRect = slide.getBoundingClientRect();
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
      '.fermat-rule-strip', '.fermat-rule-strip span'
    ];
    const problems = [];
    slide.querySelectorAll(selectors.join(',')).forEach((node) => {
      const style = getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      if (style.display === 'none' || style.visibility === 'hidden' || rect.width === 0 || rect.height === 0) return;
      const outside = rect.left < slideRect.left - 2 ||
        rect.right > slideRect.right + 2 ||
        rect.top < slideRect.top - 2 ||
        rect.bottom > slideRect.bottom + 2;
      if (outside) {
        problems.push({
          node: node.tagName.toLowerCase() + (node.className ? '.' + String(node.className).split(' ').join('.') : ''),
          rect: [Math.round(rect.left), Math.round(rect.top), Math.round(rect.right), Math.round(rect.bottom)]
        });
      }
    });
    return problems;
}"""

OVERLAP_SCRIPT = """(slide) => {
    const pairs = slide.id === 'dziewiec-dziewiec'
      ? [['.proof-split', '.proof-takeaway']]
      : slide.id === 'dowod-jeden-rowna-sie-dwa'
        ? [['.bad-proof', '.codex-audit'], ['.codex-audit', '.bad-proof-takeaway']]
        : slide.id === 'idee'
          ? [
              ['.slide-header', '.rectangle-idea-layout'],
              ['.board-panel', '.case-principles'],
              ['.codex-candidates', '.case-principles']
            ]
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
      const overlap = a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
      return overlap ? [{ first: firstSelector, second: secondSelector }] : [];
    });
}"""


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    report: list[dict[str, object]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=CHROME,
            args=["--disable-gpu"],
        )
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        console_errors: list[str] = []
        page_errors: list[str] = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))

        response = page.goto(URL, wait_until="networkidle")
        if response is None or not response.ok:
            failures.append(f"Nie udało się otworzyć {URL}")

        slides = page.locator(".slide")
        slide_count = slides.count()
        if slide_count != 24:
            failures.append(f"Oczekiwano 24 slajdów, znaleziono {slide_count}")

        ids = page.locator(".slide").evaluate_all("(nodes) => nodes.map((node) => node.id)")

        for position, slide_id in enumerate(ids, start=1):
            page.evaluate(ACTIVATE_SCRIPT, slide_id)
            if slide_id == "codex":
                page.locator("[data-run-rectangle-demo]").click()
                page.wait_for_timeout(1750)
            if slide_id == "fermat-zabawa":
                page.locator("[data-run-fermat-demo]").click()
                page.wait_for_timeout(1350)
            page.wait_for_timeout(70)

            overflow = page.locator(f"#{slide_id}").evaluate(OVERFLOW_SCRIPT)
            overlap = page.locator(f"#{slide_id}").evaluate(OVERLAP_SCRIPT)

            if overflow:
                failures.append(f"Slajd {position} ({slide_id}) ma elementy poza kadrem w 1440×900: {overflow}")
            if overlap:
                failures.append(f"Slajd {position} ({slide_id}) ma nakładające się sekcje w 1440×900: {overlap}")

            screenshot = OUTPUT / f"{position:02d}-{slide_id}.png"
            page.screenshot(path=str(screenshot), full_page=False)
            report.append({
                "number": position,
                "id": slide_id,
                "overflow": overflow,
                "overlap": overlap,
                "screenshot": str(screenshot.relative_to(ROOT)),
            })

        for width, height in [(1366, 768), (1920, 1080)]:
            page.set_viewport_size({"width": width, "height": height})
            page.goto(f"{URL}/?viewport={width}x{height}", wait_until="networkidle")
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
                    failures.append(
                        f"Slajd {position} ({slide_id}) ma elementy poza kadrem w {width}×{height}: {overflow}"
                    )
                if overlap:
                    failures.append(
                        f"Slajd {position} ({slide_id}) ma nakładające się sekcje w {width}×{height}: {overlap}"
                    )
                if slide_id in {
                    "dziewiec-dziewiec",
                    "dowod-jeden-rowna-sie-dwa",
                    "idee",
                    "codex",
                    "jak-sie-uczyc",
                    "fermat-zabawa",
                }:
                    page.wait_for_timeout(320)
                    page.screenshot(
                        path=str(OUTPUT / f"{position:02d}-{slide_id}-{width}x{height}.png"),
                        full_page=False,
                    )

        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(f"{URL}/?interaction-test=1#start", wait_until="networkidle")
        first_fragment = page.locator("#sonda .fragment").first
        page.keyboard.press("ArrowRight")
        if page.locator(".slide.is-active").get_attribute("id") != "sonda":
            failures.append("ArrowRight nie przechodzi z tytułu do sondy")
        page.keyboard.press("ArrowRight")
        if not first_fragment.evaluate("(node) => node.classList.contains('is-visible')"):
            failures.append("ArrowRight nie ujawnia pierwszego fragmentu")
        page.keyboard.press("ArrowLeft")
        if first_fragment.evaluate("(node) => node.classList.contains('is-visible')"):
            failures.append("ArrowLeft nie ukrywa poprzedniego fragmentu")

        page.keyboard.press("n")
        if not page.locator("[data-speaker-panel]").evaluate("(node) => node.classList.contains('is-open')"):
            failures.append("Klawisz N nie otwiera notatek")
        page.keyboard.press("n")

        page.keyboard.press("o")
        if not page.locator(".deck").evaluate("(node) => node.classList.contains('is-overview')"):
            failures.append("Klawisz O nie otwiera przeglądu")
        page.locator("#euler").click()
        if page.locator(".slide.is-active").get_attribute("id") != "euler":
            failures.append("Kliknięcie miniatury nie wybiera slajdu")

        page.locator("[data-run-demo]").click()
        page.wait_for_timeout(900)
        result = page.locator("#euler .terminal-result").inner_text()
        if "n = 40" not in result or "41²" not in result:
            failures.append(f"Demo Eulera zwróciło nieoczekiwany wynik: {result}")

        page.goto(f"{URL}/?rectangle-interaction=1#codex", wait_until="networkidle")
        page.locator("#codex .fragment").evaluate_all(
            "(nodes) => nodes.forEach((node) => node.classList.add('is-visible'))"
        )
        page.locator("[data-run-rectangle-demo]").click()
        page.wait_for_timeout(1750)
        rectangle_output = page.locator("[data-rectangle-transcript]").inner_text()
        if "784" not in rectangle_output or "FAIL" not in rectangle_output or "1296" not in rectangle_output:
            failures.append(f"Symulacja Codex ma niepełny przebieg: {rectangle_output}")

        page.goto(f"{URL}/?fermat-interaction=1#fermat-zabawa", wait_until="networkidle")
        page.locator("#fermat-zabawa .fragment").evaluate_all(
            "(nodes) => nodes.forEach((node) => node.classList.add('is-visible'))"
        )
        page.locator("[data-run-fermat-demo]").click()
        page.wait_for_timeout(1350)
        fermat_output = page.locator("[data-fermat-transcript]").inner_text()
        fermat_transfer = page.locator("[data-fermat-offline]").inner_text()
        if "341 = 11 × 31" not in fermat_output or "mod 341 = 0" not in fermat_output:
            failures.append(f"Symulacja Fermata nie znalazła kontrprzykładu: {fermat_output}")
        if "3" not in fermat_transfer or "100" not in fermat_transfer or "4" not in fermat_transfer:
            failures.append(f"Slajd Fermata nie pokazuje samodzielnego transferu: {fermat_transfer}")

        if console_errors:
            failures.append(f"Błędy konsoli: {console_errors}")
        if page_errors:
            failures.append(f"Błędy strony: {page_errors}")

        browser.close()

    report_path = ROOT / "test-results" / "report.json"
    report_path.write_text(json.dumps({"slides": report, "failures": failures}, ensure_ascii=False, indent=2), encoding="utf-8")

    if failures:
        print("Test przeglądarkowy nieudany:")
        for failure in failures:
            print(f"  ✗ {failure}")
        print(f"Raport: {report_path}")
        return 1

    print(
        f"Test przeglądarkowy udany: {len(report)} slajdy, "
        "3 rozdzielczości, brak przepełnień i błędów."
    )
    print(f"Zrzuty: {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
