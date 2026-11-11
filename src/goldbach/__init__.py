"""Finite Goldbach certificate pipeline.

Modules:
    primes      sieve, Miller-Rabin, factorisation, segmented sieve
    certificate bounded-witness certificate producer
    checker     independent row-by-row checker and mutation self-tests
    kernel      end-to-end verification result
    pipeline    orchestration used by the entry point
    report      certificate report
    appendix    exploratory analytic heuristic (not part of the verdict)
"""

from .constants import CertificateConstants, DEFAULT_CONSTANTS
from .kernel import VerificationError, VerificationResult, verify
from .pipeline import run_pipeline

__all__ = [
    "CertificateConstants",
    "DEFAULT_CONSTANTS",
    "VerificationError",
    "VerificationResult",
    "run_pipeline",
    "verify",
]
