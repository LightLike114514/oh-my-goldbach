"""Twin-prime constant and Hardy-Littlewood singular series factors."""

from __future__ import annotations

from fractions import Fraction

from .intervals import Interval
from .primes import factorize, sieve

# Literature interval for the twin-prime constant, used only as a sanity
# anchor by the kernel; the certificate computes its own bounds.
TWIN_CONSTANT_LOWER = 0.6601618158
TWIN_CONSTANT_UPPER = 0.6601618159


def twin_constant_bounds(cutoff: int = 200_000) -> Interval:
    """Heuristic bounds from a partial Euler product plus a tail estimate.

    This exploratory helper uses ordinary floating-point arithmetic; it is
    not an outward-rounded numerical certificate and is not used for the
    certificate verdict.

    The omitted factors satisfy
        prod_{p > cutoff} (1 - 1/(p-1)^2) >= 1 - sum_{m > cutoff} 1/(m-1)^2
                                              >= 1 - 1/(cutoff - 1),
    which is the tail term used below.
    """
    if cutoff < 10:
        raise ValueError("twin-constant cutoff is too small")
    flags = sieve(cutoff)
    partial = 1.0
    for prime in range(3, cutoff + 1):
        if flags[prime]:
            partial *= 1.0 - 1.0 / ((prime - 1) * (prime - 1))
    tail = 1.0 / (cutoff - 1)
    return Interval(partial * (1.0 - tail), partial)


def singular_series(n: int) -> Fraction:
    """Exact Hardy-Littlewood singular series factor for even n."""
    if n < 4 or n % 2:
        raise ValueError("singular series is defined for even n >= 4")
    value = Fraction(1, 1)
    for prime, _ in factorize(n):
        if prime > 2:
            value *= Fraction(prime - 1, prime - 2)
    return value


def singular_series_bounds(n: int) -> Interval:
    return Interval.from_fraction(singular_series(n))


def singular_series_floor(n: int) -> float:
    """Lower bound for the singular series; it is at least one for even n."""
    return singular_series_bounds(n).lower()


def singular_series_table(limit: int) -> dict[int, float]:
    """Cache the series factor for every even n up to limit."""
    table: dict[int, float] = {}
    for n in range(4, limit + 1, 2):
        table[n] = singular_series_floor(n)
    return table


def prime_factor_weights(n: int) -> dict[int, Fraction]:
    """Return the exact weights contributed by each odd prime factor."""
    weights: dict[int, Fraction] = {}
    for prime, _ in factorize(n):
        if prime > 2:
            weights[prime] = Fraction(prime - 1, prime - 2)
    return weights
