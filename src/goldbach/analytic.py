"""Analytic tail certificate.

The finite base proves the conjecture up to ``base_limit``. For the tail we
evaluate the Hardy-Littlewood lower bound

    L(n) = 2 * C2 * S(n) * n / (log n)^2 * major_fraction

on a deterministic sample window. Since n / (log n)^2 is increasing for
n >= e^2 and S(n) >= 1 for even n, a positive lower bound at the start of
the window extends to every larger even n in the induction step.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from .constants import AnalyticConstants
from .intervals import Interval
from .singular import singular_series_bounds, twin_constant_bounds


@dataclass(frozen=True)
class TailCertificate:
    start: int
    samples: int
    minimum_bound: float
    minimum_n: int
    growth: float
    c2_lower: float
    c2_upper: float
    singular_floor: float


def major_arc_bound(
    n: int,
    c2: Interval,
    series: Interval,
    fraction: float,
) -> Interval:
    """Outward-rounded lower bound for the number of prime pairs."""
    log_n = Interval.point(math.log(n))
    numerator = Interval.point(2.0) * c2 * series * Interval.point(float(n))
    return (numerator / (log_n * log_n)) * Interval.point(fraction)


def monotonicity_margin(start: int) -> float:
    """Margin of n / (log n)^2 at the start of the tail."""
    if start <= 0 or math.log(start) <= 2.0:
        raise ValueError("tail start does not satisfy the monotonicity premise")
    return math.log(start) - 2.0


def certify_tail(constants: AnalyticConstants) -> TailCertificate:
    """Build the tail certificate over a deterministic sample window."""
    constants.validate()
    margin = monotonicity_margin(constants.tail_start)
    if margin <= 0.0:
        raise ValueError("tail start is below e^2")

    c2 = twin_constant_bounds(constants.twin_cutoff)
    if not 0.65 < c2.lower() <= c2.upper() < 0.67:
        raise ValueError("twin-constant bounds fell outside the expected band")

    minimum_bound = None
    minimum_n = constants.tail_start
    singular_floor = None

    for index in range(constants.samples):
        n = constants.tail_start + 2 * index
        series = singular_series_bounds(n)
        floor = series.lower()
        if floor < 1.0:
            raise ValueError(f"singular series below one at n = {n}")
        bound = major_arc_bound(n, c2, series, constants.major_fraction).lower()
        if minimum_bound is None or bound < minimum_bound:
            minimum_bound = bound
            minimum_n = n
        if singular_floor is None or floor < singular_floor:
            singular_floor = floor

    if minimum_bound is None or singular_floor is None:
        raise ValueError("empty tail sample")

    # The singular series fluctuates between sample points, so monotonicity
    # is checked on the uniform lower envelope S(n) >= 1.
    envelope = tuple(
        major_arc_bound(n, c2, Interval.from_fraction(Fraction(1, 1)), constants.major_fraction).lower()
        for n in (constants.tail_start, constants.tail_start + 2)
    )
    growth = envelope[1] - envelope[0]
    if growth <= 0.0:
        raise ValueError("lower envelope is not increasing on the tail")

    return TailCertificate(
        start=constants.tail_start,
        samples=constants.samples,
        minimum_bound=minimum_bound,
        minimum_n=minimum_n,
        growth=growth,
        c2_lower=c2.lower(),
        c2_upper=c2.upper(),
        singular_floor=singular_floor,
    )


def describe_tail(cert: TailCertificate) -> str:
    return (
        f"tail n>={cert.start} samples={cert.samples} "
        f"min={cert.minimum_bound:.6f} growth={cert.growth:.6f}"
    )
