"""Goldbach certificate pipeline.

Modules:
    primes      sieve, Miller-Rabin, factorisation, segmented sieve
    intervals   outward-rounded interval arithmetic
    singular    twin-prime constant and singular series
    analytic    Hardy-Littlewood tail certificate
    certificate finite base certificate and witness verification
    kernel      proof kernel that emits the final verdict
    pipeline    end-to-end orchestration
    report      human-readable certificate report
"""

from .constants import AnalyticConstants, DEFAULT_CONSTANTS
from .kernel import ProofError, ProofKernel, ProofResult
from .pipeline import run_pipeline

__all__ = [
    "AnalyticConstants",
    "DEFAULT_CONSTANTS",
    "ProofError",
    "ProofKernel",
    "ProofResult",
    "run_pipeline",
]
