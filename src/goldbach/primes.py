"""Prime generation, deterministic primality testing and factorisation.

The module is deliberately self-contained: the certificate pipeline must be
able to rebuild every table from scratch on the evaluation host, without
trusting serialized state produced elsewhere.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Sequence, Tuple

# Deterministic Miller-Rabin bases for every n < 2**64 (Jaeschke/Sorenson).
MILLER_RABIN_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def sieve(limit: int) -> bytearray:
    """Return flags where flags[i] == 1 exactly when i is prime."""
    if limit < 0:
        raise ValueError("sieve limit must be non-negative")
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for factor in range(2, math.isqrt(limit) + 1):
        if flags[factor]:
            start = factor * factor
            flags[start:limit + 1:factor] = b"\x00" * (((limit - start) // factor) + 1)
    return flags


def primes_up_to(limit: int) -> List[int]:
    flags = sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def _miller_rabin(n: int, bases: Sequence[int]) -> bool:
    if n < 2:
        return False
    for small in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == small:
            return True
        if n % small == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in bases:
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_prime(n: int) -> bool:
    """Deterministic primality test valid for every 64-bit unsigned integer."""
    return _miller_rabin(n, MILLER_RABIN_BASES)


def factorize(n: int) -> List[Tuple[int, int]]:
    """Return the prime factorisation of n as (prime, exponent) pairs."""
    if n < 1:
        raise ValueError("factorisation requires a positive integer")
    factors: List[Tuple[int, int]] = []
    remainder = n
    exponent = 0
    while remainder % 2 == 0:
        remainder //= 2
        exponent += 1
    if exponent:
        factors.append((2, exponent))
    candidate = 3
    while candidate * candidate <= remainder:
        exponent = 0
        while remainder % candidate == 0:
            remainder //= candidate
            exponent += 1
        if exponent:
            factors.append((candidate, exponent))
        candidate += 2
    if remainder > 1:
        factors.append((remainder, 1))
    return factors


def prime_factors(n: int) -> List[int]:
    return [prime for prime, _ in factorize(n)]


def segmented_sieve(low: int, high: int, base_primes: Sequence[int]) -> List[int]:
    """Return primes in [low, high] using a precomputed base prime list."""
    if low < 2:
        low = 2
    if high < low:
        return []
    size = high - low + 1
    flags = bytearray(b"\x01") * size
    for prime in base_primes:
        if prime * prime > high:
            break
        start = max(prime * prime, ((low + prime - 1) // prime) * prime)
        for multiple in range(start, high + 1, prime):
            flags[multiple - low] = 0
    return [low + offset for offset in range(size) if flags[offset]]


def prime_count(limit: int) -> int:
    """Count primes <= limit with a sieve (used as a table sanity check)."""
    if limit < 2:
        return 0
    flags = sieve(limit)
    return sum(flags)


def wheel_residues(modulus: int) -> List[int]:
    """Coprime residues of the wheel, used by residue-class certificates."""
    return [value for value in range(modulus) if math.gcd(value, modulus) == 1]


def first_prime_factor(n: int) -> int:
    """Smallest prime factor of n, or n itself when n is prime."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if n % 2 == 0:
        return 2
    candidate = 3
    while candidate * candidate <= n:
        if n % candidate == 0:
            return candidate
        candidate += 2
    return n


def prime_gap_table(limit: int) -> Dict[int, int]:
    """Map each prime below limit to the gap to the next prime."""
    primes = primes_up_to(limit)
    return {prime: primes[index + 1] - prime for index, prime in enumerate(primes[:-1])}
