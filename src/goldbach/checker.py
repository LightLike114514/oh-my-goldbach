"""Independent checker for the finite Goldbach certificate.

The checker shares no sieve with the producer: it builds its own prime table
with a list-based implementation, walks every declared row, validates both
addends, and recomputes the digest.  It also runs mutation self-tests so a
checker that silently accepts corrupt data fails loudly.
"""

from __future__ import annotations

import hashlib
from array import array
from dataclasses import dataclass, replace
from typing import Iterator

from .certificate import Certificate, build_certificate
from .constants import CertificateConstants


class CheckError(RuntimeError):
    """Raised when a certificate row, count, or digest does not validate."""


@dataclass(frozen=True)
class CheckResult:
    rows: int
    max_witness: int
    digest: str


def independent_sieve(limit: int) -> list[bool]:
    """List-based sieve, deliberately separate from the producer's bytearray."""
    flags = [True] * (limit + 1)
    flags[0] = False
    flags[1] = False
    value = 2
    while value * value <= limit:
        if flags[value]:
            start = value * value
            flags[start:limit + 1:value] = [False] * (((limit - start) // value) + 1)
        value += 1
    return flags


def verify_certificate(cert: Certificate, constants: CertificateConstants) -> CheckResult:
    if cert.limit != constants.limit:
        raise CheckError("certificate limit does not match the declared scope")
    if cert.candidate_bound != constants.candidate_bound:
        raise CheckError("certificate search budget does not match the declared scope")
    expected = (cert.limit - 4) // 2 + 1
    if len(cert.witnesses) != expected:
        raise CheckError(f"row count mismatch: {len(cert.witnesses)} != {expected}")
    if cert.missing:
        raise CheckError(f"{len(cert.missing)} rows have no witness inside the search budget")

    flags = independent_sieve(cert.limit)
    digest = hashlib.sha256()
    maximum = 0
    for index, raw in enumerate(cert.witnesses):
        n = 4 + 2 * index
        p = int(raw)
        q = n - p
        if p < 2 or p > q or p + q != n or not flags[p] or not flags[q]:
            raise CheckError(f"invalid witness at n = {n}: p = {p}")
        maximum = max(maximum, p)
        digest.update(f"{n}:{p}\n".encode("utf-8"))
    if digest.hexdigest() != cert.digest:
        raise CheckError("certificate digest mismatch")
    return CheckResult(rows=expected, max_witness=maximum, digest=digest.hexdigest())


def _refresh_digest(cert: Certificate) -> Certificate:
    digest = hashlib.sha256()
    for index, raw in enumerate(cert.witnesses):
        n = 4 + 2 * index
        digest.update(f"{n}:{int(raw)}\n".encode("utf-8"))
    return replace(cert, digest=digest.hexdigest())


def _mutations(cert: Certificate) -> Iterator[Certificate]:
    base = cert.witnesses
    invalid = array("I", base)
    invalid[0] = 1
    yield _refresh_digest(replace(cert, witnesses=invalid, missing=()))

    dropped = array("I", base[:-1])
    yield _refresh_digest(replace(cert, witnesses=dropped, missing=()))

    duplicated = array("I", base)
    duplicated.append(duplicated[-1])
    yield _refresh_digest(replace(cert, witnesses=duplicated, missing=()))

    composite = array("I", base)
    middle = len(composite) // 2
    composite[middle] = 9
    yield _refresh_digest(replace(cert, witnesses=composite, missing=()))


def run_self_tests(constants: CertificateConstants) -> int:
    """Verify a small certificate, then require rejection of four mutations."""
    small_constants = replace(constants, limit=constants.self_test_limit)
    small = build_certificate(small_constants)
    verify_certificate(small, small_constants)
    rejected = 0
    for mutated in _mutations(small):
        try:
            verify_certificate(mutated, small_constants)
        except CheckError:
            rejected += 1
            continue
        raise CheckError("checker accepted a mutated certificate")
    return rejected
