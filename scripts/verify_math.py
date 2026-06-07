"""Verify every numerical claim used in the main mathematical examples."""

from fermat_demo import first_base_two_pseudoprime, is_prime
from rectangle_demo import count_rectangles


def main() -> None:
    assert sum(range(1, 101)) == 5050

    assert count_rectangles(1) == 1
    assert count_rectangles(2) == 9
    assert count_rectangles(8) == 1296
    assert count_rectangles(10) == 3025

    euler_values = [n * n + n + 41 for n in range(40)]
    assert all(is_prime(value) for value in euler_values)
    assert 40 * 40 + 40 + 41 == 1681 == 41**2

    assert first_base_two_pseudoprime(400) == 341
    assert 341 == 11 * 31
    assert (pow(2, 341, 341) - 2) % 341 == 0
    assert pow(3, 6, 7) == 1
    assert pow(3, 100, 7) == 4

    print("Weryfikacja matematyczna udana: wszystkie przykłady liczbowe są poprawne.")


if __name__ == "__main__":
    main()
