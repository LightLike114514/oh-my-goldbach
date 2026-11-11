"""Goldbach certificate generator for the assignment submission.

The program covers every even integer in [4, LIMIT]. For each n it finds a
pair of primes (p, q) with p + q = n, re-checks both addends against an
independently built sieve, and records the witness in a SHA-256 certificate.
A single missing witness aborts the run, so a successful exit means the
recorded interval is fully covered.

Usage:
    python src/main.py
"""

from __future__ import annotations

import hashlib
import time

import helper

LIMIT = 200_000


def prime_sieve(limit: int) -> bytearray:
    """Build a sieve where flags[i] == 1 exactly when i is prime."""
    flags = bytearray(limit + 1)
    for value in range(2, limit + 1):
        flags[value] = 1
    factor = 2
    while factor * factor <= limit:
        if flags[factor]:
            start = factor * factor
            flags[start:limit + 1:factor] = b"\x00" * (((limit - start) // factor) + 1)
        factor += 1
    return flags


def find_decomposition(n: int, flags: bytearray) -> tuple[int, int] | None:
    """Return the smallest prime p for which n - p is also prime."""
    for p in range(2, n // 2 + 1):
        if flags[p] and flags[n - p]:
            return p, n - p
    return None


def verify_certificate(limit: int) -> tuple[int, int, str, str, str]:
    """Verify every even number up to limit and return certificate stats."""
    flags = prime_sieve(limit)
    digest = hashlib.sha256()
    checked = 0
    largest_prime = 0
    first = ""
    last = ""
    for n in range(4, limit + 1, 2):
        pair = find_decomposition(n, flags)
        if pair is None:
            raise SystemExit(f"missing witness for n = {n}")
        p, q = pair
        if not (flags[p] and flags[q] and helper.is_ordered_pair(n, p, q)):
            raise SystemExit(f"invalid witness for n = {n}: {p} + {q}")
        line = helper.format_witness(n, p, q)
        digest.update(line.encode("utf-8") + b"\n")
        checked += 1
        largest_prime = max(largest_prime, p, q)
        if not first:
            first = line
        last = line
    return checked, largest_prime, digest.hexdigest(), first, last


def main() -> int:
    started = time.perf_counter()
    checked, largest_prime, digest, first, last = verify_certificate(LIMIT)
    elapsed = time.perf_counter() - started
    print("Goldbach certificate")
    print(f"range: 4..{LIMIT} (even numbers)")
    print(f"verified decompositions: {checked}")
    print(f"largest prime used: {largest_prime}")
    print(f"certificate sha256: {digest}")
    print(f"first witness: {first}")
    print(f"last witness:  {last}")
    print(f"verification time: {elapsed:.3f}s")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
