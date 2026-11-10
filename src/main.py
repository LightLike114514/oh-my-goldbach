"""Assignment entry point: Goldbach certificate pipeline.

Run from the repository root:

    python src/main.py

The program builds the finite base certificate and the analytic tail
certificate, hands both to the proof kernel, and prints the report. The
kernel is the only component allowed to emit the final QED line.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import replace

import helper

from goldbach.constants import DEFAULT_CONSTANTS
from goldbach.kernel import ProofError
from goldbach.pipeline import run_pipeline
from goldbach.report import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and verify a Goldbach certificate."
    )
    parser.add_argument("--base", type=int, default=DEFAULT_CONSTANTS.base_limit,
                        help="upper bound of the exhaustive finite base")
    parser.add_argument("--tail", type=int, default=DEFAULT_CONSTANTS.tail_start,
                        help="start of the analytic tail")
    parser.add_argument("--samples", type=int, default=DEFAULT_CONSTANTS.samples,
                        help="number of tail sample points")
    parser.add_argument("--sieve", type=int, default=DEFAULT_CONSTANTS.sieve_limit,
                        help="sieve limit for the certificate tables")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    constants = replace(
        DEFAULT_CONSTANTS,
        base_limit=args.base,
        tail_start=args.tail,
        samples=args.samples,
        sieve_limit=args.sieve,
    )
    started = time.perf_counter()
    try:
        result = run_pipeline(constants)
    except (ProofError, ValueError) as exc:
        print(f"certificate rejected: {exc}")
        return 1
    elapsed = time.perf_counter() - started
    print(render_report(result))
    print()
    print(f"certificate digest: {helper.short_digest(result.digest, 32)}")
    print(f"first witness: {helper.format_witness(result.base.first.n, result.base.first.p, result.base.first.q)}")
    print(f"kernel checks: {len(result.steps)}")
    print(f"verification time: {elapsed:.3f}s")
    print("QED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
