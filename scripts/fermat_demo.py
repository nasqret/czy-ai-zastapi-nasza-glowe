"""Deterministic calculations used by the Fermat slide."""


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def passes_base_two_fermat_test(number: int) -> bool:
    return pow(2, number, number) == 2 % number


print("[1] Własna obserwacja")
for prime in [2, 3, 5, 7, 11]:
    remainder = (pow(2, prime, prime) - 2) % prime
    print(f"    p={prime:>2}: (2^p - 2) mod p = {remainder}")

print("\n[2-3] Krytyka hipotezy i test programu")
counterexample = next(
    number
    for number in range(4, 400)
    if not is_prime(number) and passes_base_two_fermat_test(number)
)
print(f"    pierwszy złożony kontrprzykład < 400: {counterexample}")
print(f"    {counterexample} = 11 * 31")
print(
    "    (2^341 - 2) mod 341 = "
    f"{(pow(2, counterexample, counterexample) - 2) % counterexample}"
)

print("\n[4] Do tego testu nie potrzeba żadnych danych osobowych.")
print("\n[5] Małe twierdzenie Fermata i samodzielny transfer")
print("    jeśli p jest pierwsza, to a^p = a (mod p)")
print(f"    3^100 mod 7 = {pow(3, 100, 7)}")
