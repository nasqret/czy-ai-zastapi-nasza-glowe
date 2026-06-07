from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "test-results" / "site"
BASE_URL = "http://127.0.0.1:4173"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LABS = ["rectangles", "fermat", "euler", "proof", "prompt"]
ROUTES = [
    "/",
    "/experiments/pl/",
    "/experiments/en/",
    *[f"/experiments/{language}/{lab}.html" for language in ("pl", "en") for lab in LABS],
]


def assert_strict_english(text: str, context: str, failures: list[str]) -> None:
    normalized = text.replace("Naskręcki", "Naskrecki")
    if re.search(r"[ąćęłńóśźż]", normalized, flags=re.IGNORECASE):
        failures.append(f"{context}: widoczna treść EN zawiera polskie znaki")
    polish_phrases = [
        "Wróć", "Otwórz", "Uruchom", "Wynik", "Wskazówka", "Pierwszy błąd",
        "Komputer znalazł", "Matematyka nadal", "liczba pierwsza", "złożona",
    ]
    leaked = [phrase for phrase in polish_phrases if phrase.lower() in text.lower()]
    if leaked:
        failures.append(f"{context}: widoczna treść EN zawiera polskie frazy {leaked}")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=CHROME, args=["--disable-gpu"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        console_errors: list[str] = []
        page_errors: list[str] = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))

        page.goto(BASE_URL, wait_until="networkidle")
        if page.locator('a[href="pl/"]').count() < 1 or page.locator('a[href="en/"]').count() < 1:
            failures.append("Landing page nie zawiera obu prezentacji")
        if "Copyright © 2026 Bartosz Naskręcki" not in page.locator(".site-footer").inner_text():
            failures.append("Landing page nie zawiera pełnego copyrightu")
        cards = page.locator(".experiment-card")
        if cards.count() != 5:
            failures.append(f"Landing page pokazuje {cards.count()} bezpośrednich kart laboratoriów zamiast 5")
        for lab in LABS:
            if page.locator(f'.experiment-card[data-href-pl="experiments/pl/{lab}.html"]').count() != 1:
                failures.append(f"Landing page nie ma bezpośredniej polskiej karty {lab}")
            if page.locator(f'.experiment-card[data-href-en="experiments/en/{lab}.html"]').count() != 1:
                failures.append(f"Landing page nie ma bezpośredniej angielskiej karty {lab}")

        page.locator('[data-language="en"]').click()
        if page.locator(".landing-copy h1").inner_text() != "Will AI replace our minds?":
            failures.append("Przełącznik języka landing page nie działa")
        for lab in LABS:
            href = page.locator(f'.experiment-card[data-href-en$="/{lab}.html"]').get_attribute("href")
            if href != f"experiments/en/{lab}.html":
                failures.append(f"Po przełączeniu EN karta {lab} prowadzi do {href}")
        page.screenshot(path=str(OUTPUT / "landing-desktop.png"), full_page=True)

        for language in ("pl", "en"):
            page.goto(f"{BASE_URL}/experiments/{language}/", wait_until="networkidle")
            if page.locator(".lab-card").count() != 5:
                failures.append(f"Hub {language} nie pokazuje pięciu eksperymentów")
            if language == "en":
                assert_strict_english(page.locator("body").inner_text(), "Hub EN", failures)

        page.goto(f"{BASE_URL}/experiments/pl/rectangles.html", wait_until="networkidle")
        page.locator("#board-rows").fill("3")
        page.locator("#board-columns").fill("5")
        page.locator("[data-rectangle-form]").evaluate("(form) => form.requestSubmit()")
        rectangle_formula = page.locator("[data-formula]").inner_text()
        rectangle_log = page.locator("[data-terminal]").inner_text()
        if "C(4,2) · C(6,2)" not in rectangle_formula or "90" not in rectangle_formula:
            failures.append(f"Laboratorium prostokątów nie realizuje wzoru m×k dla 3×5: {rectangle_formula}")
        if not all(value in rectangle_log for value in ["1×1", "1×2", "2×3", "90"]):
            failures.append(f"Laboratorium prostokątów nie pokazuje małych testów i wyniku: {rectangle_log}")

        page.goto(f"{BASE_URL}/experiments/en/fermat.html", wait_until="networkidle")
        page.locator("[data-fermat-form]").evaluate("(form) => form.requestSubmit()")
        fermat_formula = page.locator("[data-formula]").inner_text()
        fermat_log = page.locator("[data-terminal]").inner_text()
        fermat_note = page.locator(".equivalence-note").inner_text()
        fermat_note_html = page.locator(".equivalence-note").inner_html()
        if "341" not in fermat_formula or "11 · 31" not in fermat_formula:
            failures.append(f"Laboratorium Fermata nie znajduje i nie rozkłada 341: {fermat_formula}")
        if "gcd(2,341)=1" not in fermat_log or "2^(341−1) mod 341 = 1" not in fermat_log:
            failures.append(f"Laboratorium Fermata nie pokazuje standardowego testu z gcd: {fermat_log}")
        if (
            "gcd(a,n)=1" not in fermat_note
            or "a<sup>n−1</sup> ≡ 1" not in fermat_note_html
            or "a<sup>n</sup> ≡ a" not in fermat_note_html
        ):
            failures.append(f"Laboratorium Fermata nie wyjaśnia standardowej postaci testu: {fermat_note}")
        assert_strict_english(page.locator("body").inner_text(), "Fermat EN", failures)

        page.goto(f"{BASE_URL}/experiments/pl/euler.html", wait_until="networkidle")
        page.locator("[data-euler-form]").evaluate("(form) => form.requestSubmit()")
        euler_formula = page.locator("[data-formula]").inner_text()
        euler_log = page.locator("[data-terminal]").inner_text()
        if "40² + 40 + 41" not in euler_formula or "1681" not in euler_formula or "n=40" not in euler_log:
            failures.append(f"Laboratorium Eulera nie znajduje przypadku n=40: {euler_formula} / {euler_log}")

        page.locator("#euler-c").fill("1")
        page.locator("#euler-limit").fill("5")
        page.locator("[data-euler-form]").evaluate("(form) => form.requestSubmit()")
        c_one_log = page.locator("[data-terminal]").inner_text()
        c_one_formula = page.locator("[data-formula]").inner_text()
        if "ani pierwsza, ani złożona" not in c_one_log or "0² + 0 + 1 = 1" not in c_one_formula:
            failures.append(f"Laboratorium Eulera błędnie klasyfikuje c=1: {c_one_log} / {c_one_formula}")

        page.goto(f"{BASE_URL}/experiments/en/proof.html", wait_until="networkidle")
        hint_button = page.locator("[data-proof-hint]")
        hint_button.click()
        hint_one = page.locator("[data-terminal]").inner_text()
        hint_button.click()
        hint_two = page.locator("[data-terminal]").inner_text()
        hint_button.click()
        hint_three = page.locator("[data-terminal]").inner_text()
        if not ("Hint 1:" in hint_one and "Hint 2:" in hint_two and "Hint 3:" in hint_three):
            failures.append(f"Audyt dowodu nie podaje trzech stopniowanych wskazówek: {hint_one} | {hint_two} | {hint_three}")
        page.locator("[data-proof-reset]").click()
        if "select a suspicious step or request a hint" not in page.locator("[data-terminal]").inner_text().lower():
            failures.append("Reset audytu dowodu nie przywraca stanu oczekiwania")
        page.locator('input[value="3"]').check()
        page.locator("[data-proof-form]").evaluate("(form) => form.requestSubmit()")
        if "step 4 is the first error" not in page.locator("[data-terminal]").inner_text():
            failures.append("Audyt dowodu nie rozpoznaje pierwszego błędu")
        assert_strict_english(page.locator("body").inner_text(), "Proof EN", failures)

        page.goto(f"{BASE_URL}/experiments/pl/prompt.html", wait_until="networkidle")
        subject = page.locator("#subject")
        values = subject.locator("option").evaluate_all("(options) => options.map((option) => option.value)")
        expected_subjects = ["math", "history", "biology", "literature", "programming"]
        if values != expected_subjects:
            failures.append(f"Prompt Dojo ma dziedziny {values} zamiast {expected_subjects}")
        for value in expected_subjects:
            subject.select_option(value)
            page.locator("[data-prompt-form]").evaluate("(form) => form.requestSubmit()")
            prompt = page.locator("[data-prompt-output]").input_value()
            if "CEL:" not in prompt or "GOTOWE, GDY:" not in prompt:
                failures.append(f"Prompt Dojo nie buduje kompletnego promptu dla dziedziny {value}")
        if page.locator('[aria-live="polite"]').count() < 3:
            failures.append("Prompt Dojo nie oznacza dynamicznych wyników przez aria-live")

        for language in ("pl", "en"):
            for lab in LABS:
                page.goto(f"{BASE_URL}/experiments/{language}/{lab}.html", wait_until="networkidle")
                if page.locator("noscript").count() != 1:
                    failures.append(f"{language}/{lab}: brak elementu noscript")
                if page.locator('[aria-live="polite"]').count() < 2:
                    failures.append(f"{language}/{lab}: za mało regionów aria-live")
                if language == "en":
                    assert_strict_english(page.locator("body").inner_text(), f"{lab} EN", failures)

        no_js_context = browser.new_context(java_script_enabled=False)
        no_js_page = no_js_context.new_page()
        no_js_page.goto(f"{BASE_URL}/experiments/en/fermat.html", wait_until="domcontentloaded")
        if not no_js_page.locator(".noscript-message").is_visible():
            failures.append("Treść noscript laboratorium Fermata nie jest widoczna bez JavaScriptu")
        if "gcd(a,n)=1" not in no_js_page.locator(".noscript-message").inner_text():
            failures.append("Treść noscript Fermata nie zachowuje warunku gcd")
        no_js_context.close()

        for width, height in [(1440, 900), (390, 844)]:
            page.set_viewport_size({"width": width, "height": height})
            for route in ROUTES:
                page.goto(f"{BASE_URL}{route}", wait_until="networkidle")
                if page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2"):
                    failures.append(f"Poziome przepełnienie na {route} w {width}×{height}")
            page.goto(BASE_URL, wait_until="networkidle")
            page.screenshot(path=str(OUTPUT / f"landing-{width}x{height}.png"), full_page=True)

        if console_errors:
            failures.append(f"Błędy konsoli: {console_errors}")
        if page_errors:
            failures.append(f"Błędy strony: {page_errors}")
        browser.close()

    if failures:
        print("Test serwisu nieudany:")
        for failure in failures:
            print(f"  ✗ {failure}")
        return 1
    print("Test serwisu udany: landing page, pięć laboratoriów, matematyka, lokalizacja i dostępność.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
