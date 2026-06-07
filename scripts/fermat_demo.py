"""Deterministic calculations for the standard Fermat primality test."""

from math import gcd


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def passes_fermat_test(number: int, base: int = 2) -> bool:
    """Return whether gcd(base,n)=1 and base^(n-1) is 1 modulo n."""
    return number > 1 and gcd(base, number) == 1 and pow(base, number - 1, number) == 1


def passes_base_two_fermat_test(number: int) -> bool:
    """Backward-compatible name for the standard base-two test."""
    return passes_fermat_test(number, 2)


def first_fermat_pseudoprime(limit: int, base: int = 2) -> int:
    return next(
        number
        for number in range(4, limit)
        if not is_prime(number) and passes_fermat_test(number, base)
    )


def first_base_two_pseudoprime(limit: int) -> int:
    return first_fermat_pseudoprime(limit, 2)


def main() -> None:
    base = 2
    print("[THEOREM] If p is prime and gcd(a,p)=1, then a^(p-1) = 1 (mod p).")
    for prime in [3, 5, 7, 11]:
        print(
            f"    p={prime:>2}: gcd({base},{prime})={gcd(base, prime)}, "
            f"2^(p-1) mod p = {pow(base, prime - 1, prime)}"
        )

    counterexample = first_fermat_pseudoprime(400, base)
    print("\n[COMPUTER FOUND]")
    print(f"    first composite base-{base} pseudoprime < 400: {counterexample}")
    print(f"    gcd({base},{counterexample}) = {gcd(base, counterexample)}")
    print(f"    {counterexample} = 11 * 31")
    print(
        f"    {base}^({counterexample}-1) mod {counterexample} = "
        f"{pow(base, counterexample - 1, counterexample)}"
    )

    print("\n[EQUIVALENCE WHEN gcd(a,n)=1]")
    print("    a^(n-1) = 1 (mod n)  <=>  a^n = a (mod n)")
    print("    Forward: multiply by a. Reverse: multiply by the inverse of a modulo n.")
    print("\n[MATHEMATICS STILL NEEDS TO EXPLAIN]")
    print("    Passing a Fermat test is necessary for primes, but does not prove primality.")


if __name__ == "__main__":
    main()
