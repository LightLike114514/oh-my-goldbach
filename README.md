# Goldbach Certificate

Homework submission for 证明哥德巴赫猜想 (Goldbach's conjecture).

## Scope

The submission certifies the finite statement **T(N)**: every even
`n` in `[4, N]` has a decomposition `n = p + q` into two primes, with
`N = 4,000,000`. The infinite conjecture is not claimed; the report prints
the remaining open interval.

The assignment asks for a proof of the general statement. This submission
contributes the machine-checked finite base of such a proof and an
exploratory analytic appendix for the tail; the appendix is explicitly
conditional and is not used for the verdict.

## Entry point

From the repository root:

```sh
python src/main.py
```

## How the certificate is produced and checked

- **Producer** (`goldbach.certificate`): builds a sieve up to `N` and
  searches a bounded list of primes (`p < 1024`) for every even `n`.
  Rows with no witness inside the budget are recorded as gaps and make the
  certificate invalid.
- **Independent checker** (`goldbach.checker`): builds its own list-based
  sieve, walks every row, re-checks both addends and the digest, and
  rejects four mutated certificates before accepting the real one.
- **Kernel** (`goldbach.kernel`): prints `VERIFIED T(N)` only if every row,
  the digest, and every mutation test pass; otherwise it raises and the
  entry point exits non-zero.

The row count is fixed by the declared scope, but whether every row gets a
valid bounded witness, and what maximum witness the producer finds, are
runtime facts. The report prints both; a reader cannot infer them from the
source alone.

## Layout

```
src/main.py                 entry point and CLI
src/helper.py               formatting helpers
src/goldbach/primes.py      sieve, Miller-Rabin, factorisation
src/goldbach/certificate.py bounded-witness certificate producer
src/goldbach/checker.py     independent checker and mutation self-tests
src/goldbach/kernel.py      verification result
src/goldbach/pipeline.py    orchestration
src/goldbach/report.py      certificate report
src/goldbach/constants.py   scope and search budget
src/goldbach/intervals.py   interval arithmetic (appendix)
src/goldbach/singular.py    singular series (appendix)
src/goldbach/analytic.py    Hardy-Littlewood heuristic (appendix)
src/goldbach/appendix.py    appendix summary, not used for the verdict
```

## Appendix

`goldbach.analytic` records the exploratory Hardy-Littlewood computation.
It is not a proof of the tail, is not used by the checker, and does not
affect the `VERIFIED`/`REJECTED` verdict.

## Defaults

- certified limit: `4,000,000`
- prime search budget: `1024`
- self-test limit: `20,000`

The CLI flags `--limit` and `--bound` override the first two values for a
smaller review run.
