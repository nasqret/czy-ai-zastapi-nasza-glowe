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
PROFILE_COUNTS = {"core": 24, "math": 30, "full": 34}

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
      '.proof-puzzle', '.crime-scene', '.axis-card', '.loop-node',
      '.learning-step', '.rules-list li', '.sources-grid a',
      '.formula-card', '.token-machine', '.attention-matrix',
      '.fluency-card', '.board-panel', '.candidate-card',
      '.codex-terminal', '.codex-run-prompt', '.codex-run-plan',
      '.chat-message', '.practice-prompt', '.checklist-grid article',
      '.transfer-grid article', '.attempt-card', '.school-rules article',
      '.fermat-definitions article', '.fermat-lab', '.resource-slide',
      '.resource-rules span', '.title-meta', '.track-control'
    ];
    return [...slide.querySelectorAll(selectors.join(','))].flatMap((node) => {
      const style = getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      if (style.display === 'none' || style.visibility === 'hidden' || rect.width === 0 || rect.height === 0) return [];
      const outside = rect.left < frame.left - 2 || rect.right > frame.right + 2 ||
        rect.top < frame.top - 2 || rect.bottom > frame.bottom + 2;
      return outside ? [{
        node: node.tagName.toLowerCase(),
        classes: node.className,
        rect: [rect.left, rect.top, rect.right, rect.bottom].map(Math.round)
      }] : [];
    });
}"""

OVERLAP_SCRIPT = """(slide) => {
    const pairs = {
      'uwaga-wzor': [['.slide-header', '.formula-card']],
      'falszywy-dowod': [['.slide-header', '.proof-puzzle']],
      'audyt-dowodu': [['.bad-proof', '.bad-proof-takeaway']],
      'prostokaty': [['.slide-header', '.rectangle-idea-layout']],
      'codex': [['.slide-header', '.codex-run-grid'], ['.codex-run-grid', '.evidence-pair']],
      'euler-eksperyment': [['.slide-header', '.euler-lab'], ['.euler-lab', '.evidence-pair']],
      'korepetytor': [['.slide-header', '.tutor-case']],
      'fermat-341': [['.slide-header', '.fermat-lab'], ['.fermat-lab', '.evidence-pair']]
    }[slide.id] || [];
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


def visible_slide_count(page) -> int:
    return page.locator(".slide:not(.is-filtered)").count()


def exercise_profiles(page, language: str, failures: list[str]) -> None:
    path = PRESENTATIONS[language]
    for track, expected in PROFILE_COUNTS.items():
        page.goto(f"{BASE_URL}{path}?track={track}#start", wait_until="networkidle")
        actual = visible_slide_count(page)
        if actual != expected:
            failures.append(f"{language}: profil {track} pokazuje {actual} slajdów zamiast {expected}")
        talk_count = page.locator(".slide:not(.is-filtered):not(.appendix)").count()
        expected_talk = expected - 2
        if talk_count != expected_talk:
            failures.append(f"{language}: profil {track} ma {talk_count} slajdów wykładu zamiast {expected_talk}")
        if page.locator("[data-track-select]").input_value() != track:
            failures.append(f"{language}: selektor profilu nie wskazuje {track}")

    page.goto(f"{BASE_URL}{path}?track=core#start", wait_until="networkidle")
    page.locator("[data-track-select]").select_option("math")
    page.wait_for_timeout(100)
    if visible_slide_count(page) != 30 or "track=math" not in page.url:
        failures.append(f"{language}: zmiana profilu przez select nie aktywuje 30 slajdów math")
    page.locator("[data-track-select]").select_option("full")
    page.wait_for_timeout(100)
    if visible_slide_count(page) != 34 or "track=full" not in page.url:
        failures.append(f"{language}: zmiana profilu przez select nie aktywuje 34 slajdów full")


def exercise_interactions(page, language: str, failures: list[str]) -> None:
    path = PRESENTATIONS[language]
    url = f"{BASE_URL}{path}"
    page.goto(f"{url}?track=core&interaction-test=1#start", wait_until="networkidle")
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

    page.goto(f"{url}?track=full#uwaga-wzor", wait_until="networkidle")
    formula = page.locator("#uwaga-wzor .formula").inner_text()
    if "QK" not in formula or "+ M" not in formula or "√d" not in formula:
        failures.append(f"{language}: wzór uwagi nie zawiera maski M lub skali √d_k: {formula}")

    page.goto(f"{url}?track=full#euler-eksperyment", wait_until="networkidle")
    page.evaluate(ACTIVATE_SCRIPT, "euler-eksperyment")
    page.locator("#euler-eksperyment [data-run-demo]").evaluate("(button) => button.click()")
    page.wait_for_timeout(600)
    result = page.locator("#euler-eksperyment .terminal-result").inner_text()
    if "n = 40" not in result or "41²" not in result:
        failures.append(f"{language}: demo Eulera zwróciło {result}")

    page.goto(f"{url}?track=full#codex", wait_until="networkidle")
    page.evaluate(ACTIVATE_SCRIPT, "codex")
    page.locator("#codex .fragment").evaluate_all("(nodes) => nodes.forEach((node) => node.classList.add('is-visible'))")
    page.locator("#codex [data-run-rectangle-demo]").evaluate("(button) => button.click()")
    page.wait_for_timeout(1900)
    output = page.locator("[data-rectangle-transcript]").inner_text()
    if not all(value in output for value in ["1×1", "2×3", "1296"]):
        failures.append(f"{language}: niepełna symulacja prostokątów m×k: {output}")

    page.goto(f"{url}?track=full#fermat-341", wait_until="networkidle")
    page.evaluate(ACTIVATE_SCRIPT, "fermat-341")
    page.locator("#fermat-341 .fragment").evaluate_all("(nodes) => nodes.forEach((node) => node.classList.add('is-visible'))")
    page.locator("#fermat-341 [data-run-fermat-demo]").evaluate("(button) => button.click()")
    page.wait_for_timeout(1500)
    output = page.locator("[data-fermat-transcript]").inner_text()
    if not all(value in output for value in ["341 = 11 × 31", "gcd(2,341)=1", "2^340 mod 341 = 1"]):
        failures.append(f"{language}: symulacja standardowego testu Fermata jest niepełna: {output}")


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

            response = page.goto(f"{BASE_URL}{path}?track=full", wait_until="networkidle")
            if response is None or not response.ok:
                failures.append(f"{language}: nie udało się otworzyć prezentacji")
                page.close()
                continue
            ids = page.locator(".slide").evaluate_all("(nodes) => nodes.map((node) => node.id)")
            if len(ids) != 34:
                failures.append(f"{language}: oczekiwano 34 slajdów DOM, znaleziono {len(ids)}")

            tracks = page.locator(".slide").evaluate_all(
                """(nodes) => nodes.reduce((counts, node) => {
                    const track = node.dataset.track;
                    counts[track] = (counts[track] || 0) + 1;
                    return counts;
                }, {})"""
            )
            if tracks != {"core": 22, "technical": 4, "math": 6, "appendix": 2}:
                failures.append(f"{language}: niepoprawny podział data-track: {tracks}")

            for width, height in [(1440, 900), (1366, 768), (1920, 1080)]:
                page.set_viewport_size({"width": width, "height": height})
                page.goto(f"{BASE_URL}{path}?track=full&viewport={width}x{height}", wait_until="networkidle")
                for position, slide_id in enumerate(ids, start=1):
                    page.evaluate(ACTIVATE_SCRIPT, slide_id)
                    overflow = page.locator(f"#{slide_id}").evaluate(OVERFLOW_SCRIPT)
                    overlap = page.locator(f"#{slide_id}").evaluate(OVERLAP_SCRIPT)
                    if overflow:
                        failures.append(f"{language}: slajd {position} ({slide_id}) poza kadrem {width}×{height}: {overflow}")
                    if overlap:
                        failures.append(f"{language}: slajd {position} ({slide_id}) ma kolizję {width}×{height}: {overlap}")
                    if width == 1440:
                        screenshot = language_output / f"{position:02d}-{slide_id}.png"
                        page.screenshot(path=str(screenshot), full_page=False)
                        report.append({
                            "language": language,
                            "number": position,
                            "id": slide_id,
                            "overflow": overflow,
                            "overlap": overlap,
                        })

            exercise_profiles(page, language, failures)
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
    print("Test slajdów udany: 68 renderów slajdów, 3 rozdzielczości, 3 profile i wszystkie interakcje.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
