"""Verification pipeline for the finite Goldbach certificate."""

from __future__ import annotations

from dataclasses import dataclass

from .certificate import Certificate, build_certificate
from .checker import CheckError, CheckResult, run_self_tests, verify_certificate
from .constants import CertificateConstants


class VerificationError(RuntimeError):
    """Raised when the produced certificate fails independent verification."""


@dataclass(frozen=True)
class VerificationResult:
    certificate: Certificate
    check: CheckResult
    self_tests: int


def verify(constants: CertificateConstants) -> VerificationResult:
    constants.validate()
    certificate = build_certificate(constants)
    if certificate.missing:
        raise VerificationError(
            f"{len(certificate.missing)} rows have no witness inside "
            f"the search budget {constants.candidate_bound}"
        )
    try:
        check = verify_certificate(certificate, constants)
        self_tests = run_self_tests(constants)
    except CheckError as exc:
        raise VerificationError(str(exc)) from exc
    return VerificationResult(certificate=certificate, check=check, self_tests=self_tests)
