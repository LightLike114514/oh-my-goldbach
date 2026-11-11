"""Exploratory analytic appendix.

This module records the Hardy-Littlewood heuristic explored during the
assignment.  It is deliberately excluded from the certificate verdict: a
heuristic lower bound does not prove the infinite tail.
"""

from __future__ import annotations

from .analytic import estimate_tail
from .constants import DEFAULT_ANALYTIC


def analytic_note() -> str:
    cert = estimate_tail(DEFAULT_ANALYTIC)
    return (
        f"heuristic Hardy-Littlewood lower bound min={cert.minimum_bound:.3f} "
        f"at n={cert.minimum_n}; not a proof and not used by the checker."
    )
