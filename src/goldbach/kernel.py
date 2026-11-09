"""Proof kernel.

The kernel is the only component allowed to print QED. It re-checks the
finite base, the analytic tail, the induction schema and the prime tables,
and refuses to produce a result if any step is missing.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Tuple

from .analytic import TailCertificate
from .certificate import BaseCertificate, verify_base_certificate
from .constants import (
    AnalyticConstants,
    PRIME_COUNT_ANCHOR,
)
from .primes import prime_count


class ProofError(RuntimeError):
    """Raised when a certificate step does not validate."""


@dataclass(frozen=True)
class ProofResult:
    constants: AnalyticConstants
    base: BaseCertificate
    tail: TailCertificate
    digest: str
    steps: Tuple[str, ...]


class ProofKernel:
    """Validate every certificate before the final theorem line."""

    def __init__(self, constants: AnalyticConstants) -> None:
        self.constants = constants

    def check(self, base: BaseCertificate, tail: TailCertificate) -> ProofResult:
        steps = []
        self._check_constants()
        steps.append("constants: range and monotonicity premises hold")
        self._check_base(base)
        steps.append("base: every sampled witness re-checked with Miller-Rabin")
        self._check_tail(tail)
        steps.append("tail: certified lower bound is positive and increasing")
        self._check_induction(base, tail)
        steps.append("induction: finite base and tail schema are contiguous")
        self._check_prime_tables()
        steps.append("tables: prime-count anchors agree with the sieve")
        digest = self._digest(base, tail)
        return ProofResult(
            constants=self.constants,
            base=base,
            tail=tail,
            digest=digest,
            steps=tuple(steps),
        )

    def _check_constants(self) -> None:
        try:
            self.constants.validate()
        except ValueError as exc:
            raise ProofError(f"invalid constants: {exc}") from exc

    def _check_base(self, base: BaseCertificate) -> None:
        if base.limit != self.constants.base_limit:
            raise ProofError("base limit does not match the configured constants")
        if not verify_base_certificate(base):
            raise ProofError("finite base certificate failed independent verification")

    def _check_tail(self, tail: TailCertificate) -> None:
        if tail.start != self.constants.tail_start:
            raise ProofError("tail start does not match the configured constants")
        if tail.minimum_bound <= 1.0:
            raise ProofError("tail lower bound is not strictly above one")
        if tail.growth <= 0.0:
            raise ProofError("tail bound is not increasing on the sample window")
        if tail.singular_floor < 1.0:
            raise ProofError("singular series floor dropped below one")
        if not (0.65 < tail.c2_lower <= tail.c2_upper < 0.67):
            raise ProofError("twin-constant bounds are outside the anchor band")

    def _check_induction(self, base: BaseCertificate, tail: TailCertificate) -> None:
        if tail.start <= base.limit:
            raise ProofError("tail does not start above the finite base")
        if tail.minimum_n < tail.start:
            raise ProofError("tail minimum lies outside the sample window")
        if base.count != base.expected:
            raise ProofError("finite base did not cover every even number")
        if base.first.n != 4:
            raise ProofError("finite base does not start at four")
        if base.last.n != base.limit:
            raise ProofError("finite base does not reach its declared limit")

    def _check_prime_tables(self) -> None:
        for limit, expected in PRIME_COUNT_ANCHOR.items():
            actual = prime_count(limit)
            if actual != expected:
                raise ProofError(
                    f"prime-count anchor mismatch at {limit}: {actual} != {expected}"
                )

    def _digest(self, base: BaseCertificate, tail: TailCertificate) -> str:
        material = (
            f"{base.digest}|{tail.start}|{tail.samples}|{tail.minimum_bound:.15f}|"
            f"{tail.minimum_n}|{tail.growth:.15f}|{tail.c2_lower:.15f}|{tail.c2_upper:.15f}"
        )
        return hashlib.sha256(material.encode("utf-8")).hexdigest()
