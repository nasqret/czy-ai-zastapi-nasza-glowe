from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "test-results" / "site"
BASE_URL = "http://127.0.0.1:4173"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROUTES = [
    "/",
    "/experiments/pl/",
    "/experiments/en/",
    "/experiments/pl/rectangles.html",
    "/experiments/en/fermat.html",
    "/experiments/pl/euler.html",
    "/experiments/en/proof.html",
    "/experiments/pl/prompt.html",
]


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
        page.locator('[data-language="en"]').click()
        if page.locator(".landing-copy h1").inner_text() != "Will AI replace our minds?":
            failures.append("Przełącznik języka landing page nie działa")
        page.screenshot(path=str(OUTPUT / "landing-desktop.png"), full_page=True)

        page.goto(f"{BASE_URL}/experiments/pl/", wait_until="networkidle")
        if page.locator(".lab-card").count() != 5:
            failures.append("Polski hub nie pokazuje pięciu eksperymentów")
        page.goto(f"{BASE_URL}/experiments/en/", wait_until="networkidle")
        if page.locator(".lab-card").count() != 5:
            failures.append("Angielski hub nie pokazuje pięciu eksperymentów")

        page.goto(f"{BASE_URL}/experiments/pl/rectangles.html", wait_until="networkidle")
        page.locator("[data-rectangle-form]").evaluate("(form) => form.requestSubmit()")
        if "1296" not in page.locator("[data-formula]").inner_text():
            failures.append("Laboratorium prostokątów nie oblicza 1296")

        page.goto(f"{BASE_URL}/experiments/en/fermat.html", wait_until="networkidle")
        page.locator("[data-fermat-form]").evaluate("(form) => form.requestSubmit()")
        if "341" not in page.locator("[data-formula]").inner_text():
            failures.append("Laboratorium Fermata nie znajduje 341")

        page.goto(f"{BASE_URL}/experiments/pl/euler.html", wait_until="networkidle")
        page.locator("[data-euler-form]").evaluate("(form) => form.requestSubmit()")
        if "1681" not in page.locator("[data-formula]").inner_text():
            failures.append("Laboratorium Eulera nie znajduje 1681")

        page.goto(f"{BASE_URL}/experiments/en/proof.html", wait_until="networkidle")
        page.locator('input[value="3"]').check()
        page.locator("[data-proof-form]").evaluate("(form) => form.requestSubmit()")
        if "step 4 is the first error" not in page.locator("[data-terminal]").inner_text():
            failures.append("Audyt dowodu nie rozpoznaje pierwszego błędu")

        page.goto(f"{BASE_URL}/experiments/pl/prompt.html", wait_until="networkidle")
        prompt = page.locator("[data-prompt-output]").input_value()
        if "CEL:" not in prompt or "GOTOWE, GDY:" not in prompt:
            failures.append("Prompt dojo nie buduje kompletnego promptu")

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
    print("Test serwisu udany: landing page, laboratoria, interakcje i responsywność.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
