"""Assignment entry point: finite Goldbach certificate.

Run from the repository root:

    python src/main.py

The producer searches bounded witnesses for every even n in the declared
range, the independent checker validates every row and the digest, and the
program prints VERIFIED only if the certificate passes.  The infinite tail
is outside the certificate scope and is reported as OPEN.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import replace

import helper

from goldbach.appendix import analytic_note
from goldbach.constants import DEFAULT_CONSTANTS
from goldbach.kernel import VerificationError, verify
from goldbach.report import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and verify a finite Goldbach certificate."
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_CONSTANTS.limit,
                        help="upper bound of the certified range")
    parser.add_argument("--bound", type=int, default=DEFAULT_CONSTANTS.candidate_bound,
                        help="prime search budget used by the producer")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    constants = replace(
        DEFAULT_CONSTANTS,
        limit=args.limit,
        candidate_bound=args.bound,
    )
    started = time.perf_counter()
    try:
        result = verify(constants)
    except (VerificationError, ValueError) as exc:
        print(f"REJECTED: {exc}")
        return 1
    elapsed = time.perf_counter() - started
    print(render_report(result, analytic_note()))
    print()
    print(f"certificate digest: {helper.short_digest(result.check.digest, 32)}")
    print(f"verified rows: {result.check.rows}")
    print(f"verification time: {elapsed:.3f}s")
    print("VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
