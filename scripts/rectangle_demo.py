"""Deterministyczna symulacja pracy Codex nad zadaniem o prostokątach."""

from math import comb


def count_rectangles_buggy(n: int) -> int:
    """Typowy pierwszy błąd: użycie n linii zamiast n+1."""
    lines = range(n)
    return sum(
        1
        for left in lines
        for right in lines
        for top in lines
        for bottom in lines
        if left < right and top < bottom
    )


def count_rectangles(n: int) -> int:
    """Każdy prostokąt wybiera dwie z n+1 linii pionowych i poziomych."""
    lines = range(n + 1)
    return sum(
        1
        for left in lines
        for right in lines
        for top in lines
        for bottom in lines
        if left < right and top < bottom
    )


def main() -> None:
    print("[PLAN] Prostokąt wyznaczają 2 linie pionowe i 2 poziome.")
    print(f"[RUN 1] count_rectangles_buggy(8) = {count_rectangles_buggy(8)}")

    small_result = count_rectangles_buggy(1)
    print(f"[TEST] plansza 1x1: oczekiwano 1, otrzymano {small_result} -> FAIL")
    print("[DIAGNOZA] Plansza nxn ma n+1 linii w każdym kierunku, nie n.")
    print("[POPRAWKA] range(n) -> range(n + 1)")

    expected = {1: 1, 2: 9, 8: 1296}
    for size, value in expected.items():
        result = count_rectangles(size)
        status = "PASS" if result == value else "FAIL"
        print(f"[TEST] plansza {size}x{size}: {result} -> {status}")

    formula = comb(9, 2) ** 2
    print(f"[WZOR] C(9,2)^2 = 36^2 = {formula}")
    print(f"[WYNIK] Szachownica 8x8 zawiera {count_rectangles(8)} prostokątów.")


if __name__ == "__main__":
    main()
