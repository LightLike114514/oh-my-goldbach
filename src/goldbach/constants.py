"""Constants for the finite Goldbach certificate and the analytic appendix."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CertificateConstants:
    """Scope and search budget of the machine-checked certificate."""

    limit: int = 4_000_000
    candidate_bound: int = 1024
    self_test_limit: int = 20_000

    def validate(self) -> None:
        if self.limit < 4 or self.limit % 2:
            raise ValueError("limit must be an even integer >= 4")
        if self.candidate_bound < 3:
            raise ValueError("candidate bound must be at least 3")
        if self.self_test_limit < 4 or self.self_test_limit % 2 or self.self_test_limit > self.limit:
            raise ValueError("self-test limit must be an even integer inside the scope")

    def describe(self) -> str:
        return (
            f"limit={self.limit} candidate_bound={self.candidate_bound} "
            f"self_test_limit={self.self_test_limit}"
        )


DEFAULT_CONSTANTS = CertificateConstants()


# The analytic block is an exploratory appendix.  It is not part of the
# certificate verdict and it does not establish the infinite tail.
@dataclass(frozen=True)
class AnalyticConstants:
    base_limit: int = 200_000
    tail_start: int = 10**9
    samples: int = 512
    sieve_limit: int = 1_000_000
    twin_cutoff: int = 200_000
    major_fraction: float = 0.5
    digest_rounds: int = 3

    def validate(self) -> None:
        if self.base_limit < 4 or self.base_limit % 2:
            raise ValueError("base_limit must be an even integer >= 4")
        if self.tail_start <= self.base_limit:
            raise ValueError("tail_start must lie above the finite base")
        if self.samples < 1:
            raise ValueError("samples must be positive")
        if self.sieve_limit < self.base_limit:
            raise ValueError("sieve_limit must cover the finite base")
        if self.twin_cutoff < 3 or self.twin_cutoff > self.sieve_limit:
            raise ValueError("twin_cutoff must lie inside the sieve range")
        if not 0.0 < self.major_fraction <= 1.0:
            raise ValueError("major_fraction must lie in (0, 1]")
        if self.digest_rounds < 1:
            raise ValueError("digest_rounds must be positive")


DEFAULT_ANALYTIC = AnalyticConstants()
