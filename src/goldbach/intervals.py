"""Outward-rounded floating point intervals for certified inequalities.

Every operation widens the result by one ulp on each side, so a positive
lower bound computed with this module is a rigorous statement about the
represented floating point expression rather than an approximation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

DOWN = -math.inf
UP = math.inf


def _down(value: float) -> float:
    return math.nextafter(value, DOWN)


def _up(value: float) -> float:
    return math.nextafter(value, UP)


@dataclass(frozen=True)
class Interval:
    """A closed interval [lo, hi] with outward rounding."""

    lo: float
    hi: float

    def __post_init__(self) -> None:
        if not (self.lo <= self.hi):
            raise ValueError(f"invalid interval: [{self.lo}, {self.hi}]")

    @classmethod
    def point(cls, value: float) -> "Interval":
        return cls(_down(value), _up(value))

    @classmethod
    def from_fraction(cls, value: Fraction) -> "Interval":
        approx = float(value)
        return cls(_down(approx), _up(approx))

    @classmethod
    def positive(cls, lo: float, hi: float) -> "Interval":
        if lo <= 0.0:
            raise ValueError("positive interval must have a positive lower bound")
        return cls(_down(lo), _up(hi))

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(_down(self.lo + other.lo), _up(self.hi + other.hi))

    def __sub__(self, other: "Interval") -> "Interval":
        return Interval(_down(self.lo - other.hi), _up(self.hi - other.lo))

    def __mul__(self, other: "Interval") -> "Interval":
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(_down(min(products)), _up(max(products)))

    def __truediv__(self, other: "Interval") -> "Interval":
        if other.lo <= 0.0 <= other.hi:
            raise ZeroDivisionError("interval divisor contains zero")
        reciprocal = Interval(_down(1.0 / other.hi), _up(1.0 / other.lo))
        return self * reciprocal

    def log(self) -> "Interval":
        if self.lo <= 0.0:
            raise ValueError("logarithm requires a positive interval")
        return Interval(_down(math.log(self.lo)), _up(math.log(self.hi)))

    def sqrt(self) -> "Interval":
        if self.lo < 0.0:
            raise ValueError("square root requires a non-negative interval")
        low = 0.0 if self.lo == 0.0 else _down(math.sqrt(self.lo))
        return Interval(low, _up(math.sqrt(self.hi)))

    def lower(self) -> float:
        return self.lo

    def upper(self) -> float:
        return self.hi

    def width(self) -> float:
        return self.hi - self.lo

    def contains(self, value: float) -> bool:
        return self.lo <= value <= self.hi

    def __repr__(self) -> str:
        return f"Interval({self.lo:.17g}, {self.hi:.17g})"


ZERO = Interval(0.0, 0.0)
ONE = Interval.from_fraction(Fraction(1, 1))
TWO = Interval.from_fraction(Fraction(2, 1))
