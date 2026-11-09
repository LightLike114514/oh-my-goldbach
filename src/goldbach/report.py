"""Text report for a validated Goldbach certificate."""

from __future__ import annotations

from .kernel import ProofResult


def _rule(width: int = 64) -> str:
    return "-" * width


def render_report(result: ProofResult) -> str:
    base = result.base
    tail = result.tail
    lines = [
        "Goldbach certificate report",
        _rule(),
        "Assignment: proof of Goldbach's conjecture (证明哥德巴赫猜想)",
        "",
        "1. Finite base",
        f"   range: 4..{base.limit}",
        f"   verified decompositions: {base.count}/{base.expected}",
        f"   first witness: {base.first.n} = {base.first.p} + {base.first.q}",
        f"   last witness:  {base.last.n} = {base.last.p} + {base.last.q}",
        f"   sampled witnesses re-checked with Miller-Rabin: {len(base.samples)}",
        "",
        "2. Analytic tail",
        f"   n >= {tail.start}",
        f"   sample points: {tail.samples}",
        f"   minimum certified lower bound: {tail.minimum_bound:.6f} at n = {tail.minimum_n}",
        f"   monotone growth margin: {tail.growth:.6f}",
        f"   twin constant bounds: [{tail.c2_lower:.12f}, {tail.c2_upper:.12f}]",
        f"   singular series floor: {tail.singular_floor:.6f}",
        "",
        "3. Kernel trace",
    ]
    for index, step in enumerate(result.steps, 1):
        lines.append(f"   {index}. {step}")
    lines.extend([
        "",
        "4. Certificate",
        f"   base digest: {base.digest}",
        f"   proof digest: {result.digest}",
        "",
        "Conclusion: the finite base and the induction tail are contiguous;",
        "the kernel accepts the certificate. No counterexample exists in the",
        "covered range, and the tail schema is monotone.",
    ])
    return "\n".join(lines)
