"""Deterministic Codex-style simulation for rectangles on an m by k board."""

from math import comb


def count_rectangles_buggy(rows: int, columns: int | None = None) -> int:
    """Typical off-by-one bug: use cell counts as line counts."""
    columns = rows if columns is None else columns
    return comb(rows, 2) * comb(columns, 2)


def count_rectangles(rows: int, columns: int | None = None) -> int:
    """Choose two of rows+1 horizontal and two of columns+1 vertical lines."""
    columns = rows if columns is None else columns
    if rows < 1 or columns < 1:
        raise ValueError("Board dimensions must be positive.")
    return comb(rows + 1, 2) * comb(columns + 1, 2)


def count_rectangles_by_enumeration(rows: int, columns: int) -> int:
    """Independent enumeration used to check the closed formula."""
    horizontal = range(rows + 1)
    vertical = range(columns + 1)
    return sum(
        1
        for top in horizontal
        for bottom in horizontal
        for left in vertical
        for right in vertical
        if top < bottom and left < right
    )


def main() -> None:
    rows, columns = 2, 3
    print("[PLAN] A rectangle selects 2 horizontal and 2 vertical grid lines.")
    print(
        f"[RUN 1] buggy({rows}x{columns}) = "
        f"C({rows},2)C({columns},2) = {count_rectangles_buggy(rows, columns)}"
    )
    print("[TEST] 1x1: expected 1, buggy code returns 0 -> FAIL")
    print("[DIAGNOSIS] An m x k board has m+1 horizontal and k+1 vertical lines.")

    expected = {(1, 1): 1, (1, 2): 3, (2, 3): 18, (8, 8): 1296}
    for dimensions, value in expected.items():
        result = count_rectangles(*dimensions)
        enumerated = count_rectangles_by_enumeration(*dimensions)
        status = "PASS" if result == value == enumerated else "FAIL"
        print(f"[TEST] board {dimensions[0]}x{dimensions[1]}: {result} -> {status}")

    result = count_rectangles(rows, columns)
    print(
        f"[FORMULA] C({rows + 1},2)C({columns + 1},2) = "
        f"{comb(rows + 1, 2)} * {comb(columns + 1, 2)} = {result}"
    )
    print(f"[COMPUTER FOUND] {result} rectangles on a {rows}x{columns} board.")
    print(
        "[MATHEMATICS STILL NEEDS TO EXPLAIN] "
        "why line pairs correspond one-to-one with rectangles."
    )


if __name__ == "__main__":
    main()
