"""Verify numerical and classification claims used by the math laboratories."""

from math import gcd

from fermat_demo import (
    first_base_two_pseudoprime,
    first_fermat_pseudoprime,
    is_prime,
    passes_fermat_test,
)
from rectangle_demo import count_rectangles, count_rectangles_by_enumeration


def classify_integer(number: int) -> str:
    if number < 2:
        return "neither"
    return "prime" if is_prime(number) else "composite"


def euler_value(n: int, c: int) -> int:
    return n * n + n + c


def main() -> None:
    assert sum(range(1, 101)) == 5050

    rectangle_cases = {
        (1, 1): 1,
        (1, 2): 3,
        (2, 3): 18,
        (8, 8): 1296,
        (10, 10): 3025,
        (3, 7): 168,
    }
    for dimensions, expected in rectangle_cases.items():
        assert count_rectangles(*dimensions) == expected
        assert count_rectangles_by_enumeration(*dimensions) == expected

    assert classify_integer(0) == "neither"
    assert classify_integer(1) == "neither"
    assert classify_integer(2) == "prime"
    assert classify_integer(4) == "composite"
    assert euler_value(0, 1) == 1
    assert classify_integer(euler_value(0, 1)) == "neither"
    assert all(is_prime(euler_value(n, 41)) for n in range(40))
    assert euler_value(40, 41) == 1681 == 41**2
    for c in [1, 2, 3, 17, 41, 100]:
        assert euler_value(c - 1, c) == c**2

    assert first_base_two_pseudoprime(400) == 341
    assert first_fermat_pseudoprime(400, 2) == 341
    assert 341 == 11 * 31
    assert gcd(2, 341) == 1
    assert pow(2, 340, 341) == 1
    assert passes_fermat_test(341, 2)
    assert not passes_fermat_test(15, 3), "The gcd condition must be enforced."
    for number, base in [(341, 2), (91, 3), (7, 3), (11, 7)]:
        if gcd(base, number) == 1:
            standard = pow(base, number - 1, number) == 1
            equivalent = pow(base, number, number) == base % number
            assert standard == equivalent

    assert pow(3, 6, 7) == 1
    assert pow(3, 100, 7) == 4

    print(
        "Weryfikacja matematyczna udana: prostokąty m×k, klasyfikacja Eulera "
        "i standardowy test Fermata są poprawne."
    )


if __name__ == "__main__":
    main()
