"""End-to-end orchestration for the certificate submission."""

from __future__ import annotations

from .constants import CertificateConstants
from .kernel import VerificationResult, verify


def run_pipeline(constants: CertificateConstants) -> VerificationResult:
    return verify(constants)
