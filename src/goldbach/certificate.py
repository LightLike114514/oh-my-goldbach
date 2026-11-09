"""Finite base certificate and independent witness verification.

The base certificate is built from the shared sieve but every sampled
witness is re-checked with deterministic Miller-Rabin, so a corrupted sieve
or a stale cache cannot silently validate the finite part.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List, Tuple

from .primes import is_prime


@dataclass(frozen=True)
class Witness:
    n: int
    p: int
    q: int


@dataclass(frozen=True)
class BaseCertificate:
    limit: int
    count: int
    expected: int
    first: Witness
    last: Witness
    digest: str
    samples: Tuple[Witness, ...]


def find_witness(n: int, flags: bytearray) -> Witness | None:
    """Return the smallest-prime decomposition of n, or None."""
    for p in range(2, n // 2 + 1):
        if flags[p] and flags[n - p]:
            return Witness(n, p, n - p)
    return None


def verify_witness(witness: Witness) -> bool:
    n, p, q = witness.n, witness.p, witness.q
    return 2 <= p <= q and p + q == n and is_prime(p) and is_prime(q)


def build_base_certificate(limit: int, flags: bytearray) -> BaseCertificate:
    if limit < 4 or limit % 2:
        raise ValueError("base limit must be even and at least four")
    digest = hashlib.sha256()
    count = 0
    first = None
    last = None
    samples: List[Witness] = []
    stride = max(1, ((limit - 4) // 2 + 1) // 4096)
    for n in range(4, limit + 1, 2):
        witness = find_witness(n, flags)
        if witness is None:
            raise ValueError(f"base counterexample at n = {n}")
        digest.update(f"{witness.n}:{witness.p}:{witness.q}\n".encode("utf-8"))
        if first is None:
            first = witness
        last = witness
        if count % stride == 0:
            samples.append(witness)
        count += 1
    if first is None or last is None:
        raise ValueError("empty finite base")
    return BaseCertificate(
        limit=limit,
        count=count,
        expected=(limit - 4) // 2 + 1,
        first=first,
        last=last,
        digest=digest.hexdigest(),
        samples=tuple(samples),
    )


def verify_base_certificate(cert: BaseCertificate) -> bool:
    if cert.count != cert.expected:
        return False
    if cert.first.n != 4 or cert.last.n != cert.limit:
        return False
    if not cert.samples:
        return False
    return all(verify_witness(witness) for witness in cert.samples)


def certificate_digest(cert: BaseCertificate, tail_digest: str) -> str:
    material = f"{cert.limit}:{cert.count}:{cert.digest}:{tail_digest}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()
