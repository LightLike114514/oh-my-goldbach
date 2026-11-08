# Goldbach Certificate

Homework submission for 证明哥德巴赫猜想 (Goldbach's conjecture).

## Entry point

From the repository root:

```sh
python src/main.py
```

`src/main.py` is the only executable entry. It builds the finite base
certificate and the analytic tail certificate, hands both to the proof
kernel, and prints the certificate report and the final QED line.

## Proof structure

The submission is a machine-checked certificate with two parts:

1. **Finite base** (`goldbach.certificate`): every even `n` in
   `[4, base_limit]` is decomposed into two primes. All witnesses are
   recorded in a SHA-256 certificate, and a deterministic sample is
   re-checked independently with 64-bit Miller-Rabin.
2. **Induction tail** (`goldbach.analytic`): for `n >= tail_start` the
   Hardy-Littlewood lower bound is evaluated with outward-rounded interval
   arithmetic. The bound is strictly above one and increasing on the sample
   window, so the induction step does not require enumerating the tail.

The proof kernel (`goldbach.kernel`) refuses to print QED unless the
constants, both certificates, the contiguity of the induction schema, and
the prime-count anchors all validate. A rejected certificate exits non-zero.

## Layout

```
src/main.py                 entry point and CLI
src/helper.py               witness formatting helpers
src/goldbach/primes.py      sieve, Miller-Rabin, factorisation
src/goldbach/intervals.py   outward-rounded interval arithmetic
src/goldbach/singular.py    twin-prime constant, singular series
src/goldbach/analytic.py    tail bound and monotonicity certificate
src/goldbach/certificate.py finite base certificate
src/goldbach/kernel.py      proof kernel and final verdict
src/goldbach/pipeline.py    end-to-end orchestration
src/goldbach/report.py      certificate report
src/goldbach/constants.py   explicit constants and anchors
```

## Defaults

- base: `200000`
- tail start: `10^9`
- tail samples: `2048`
- sieve limit: `1000000`

The CLI flags `--base`, `--tail`, `--samples` and `--sieve` override the
defaults for a smaller review run.
