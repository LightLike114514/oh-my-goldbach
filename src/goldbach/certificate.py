"""Producer of the finite Goldbach certificate.

For every even n in [4, limit] the producer searches a bounded candidate
list of small primes.  A row is recorded only when both addends are prime;
rows without a witness inside the budget are left as gaps and make the
certificate invalid.  Whether the budget covers every row is a runtime
fact, not a source-level assumption.
"""

from __future__ import annotations

import hashlib
from array import array
from dataclasses import dataclass
from typing import Tuple

from .constants import CertificateConstants
from .primes import sieve


@dataclass(frozen=True)
class Certificate:
    limit: int
    candidate_bound: int
    witnesses: array
    missing: Tuple[int, ...]
    digest: str
    max_witness: int

    @property
    def rows(self) -> int:
        return (self.limit - 4) // 2 + 1


def candidate_primes(bound: int) -> list[int]:
    """All primes below the search budget, in increasing order."""
    if bound < 3:
        raise ValueError("candidate bound must be at least 3")
    flags = sieve(bound - 1)
    return [2] + [value for value in range(3, bound) if flags[value]]


def build_certificate(constants: CertificateConstants) -> Certificate:
    """Search bounded witnesses for every even n in the declared scope."""
    constants.validate()
    flags = sieve(constants.limit)
    candidates = candidate_primes(constants.candidate_bound)
    witnesses = array("I")
    missing: list[int] = []
    digest = hashlib.sha256()
    max_witness = 0

    for n in range(4, constants.limit + 1, 2):
        witness = 0
        for p in candidates:
            if p > n // 2:
                break
            if flags[n - p]:
                witness = p
                break
        if witness == 0:
            missing.append(n)
        else:
            max_witness = max(max_witness, witness)
        witnesses.append(witness)
        digest.update(f"{n}:{witness}\n".encode("utf-8"))

    return Certificate(
        limit=constants.limit,
        candidate_bound=constants.candidate_bound,
        witnesses=witnesses,
        missing=tuple(missing),
        digest=digest.hexdigest(),
        max_witness=max_witness,
    )
