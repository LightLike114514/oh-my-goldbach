"""Text report for a verified finite Goldbach certificate."""

from __future__ import annotations

from .kernel import VerificationResult


def render_report(result: VerificationResult, appendix_note: str) -> str:
    certificate = result.certificate
    check = result.check
    lines = [
        "Goldbach certificate report",
        "-" * 64,
        "assignment: Goldbach's conjecture (证明哥德巴赫猜想)",
        f"scope: every even n in [4, {certificate.limit}]",
        "",
        "producer",
        f"  bounded witness search over primes < {certificate.candidate_bound}",
        f"  rows emitted: {len(certificate.witnesses)}",
        f"  rows without witness: {len(certificate.missing)}",
        "",
        "independent checker",
        f"  rows validated: {check.rows}",
        f"  maximum witness prime: {check.max_witness}",
        f"  certificate digest: {check.digest}",
        f"  mutation tests rejected: {result.self_tests}",
        "",
        f"OPEN: the interval ({certificate.limit}, +infinity) is not covered by this certificate.",
        f"appendix (not used for the verdict): {appendix_note}",
    ]
    return "\n".join(lines)
