"""End-to-end certificate pipeline used by the assignment entry point."""

from __future__ import annotations

from .analytic import certify_tail
from .certificate import build_base_certificate
from .constants import AnalyticConstants
from .kernel import ProofKernel, ProofResult
from .primes import sieve


def run_pipeline(constants: AnalyticConstants) -> ProofResult:
    """Build both certificates and hand them to the proof kernel."""
    constants.validate()
    flags = sieve(max(constants.sieve_limit, constants.base_limit))
    base = build_base_certificate(constants.base_limit, flags)
    tail = certify_tail(constants)
    return ProofKernel(constants).check(base, tail)
