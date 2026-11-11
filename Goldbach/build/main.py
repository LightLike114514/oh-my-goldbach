r"""哥德巴赫猜想：部分结果文档与有限区间计算验证器

本题要求证明：任一大于 2 的偶数都可以写成两个素数之和。一个完整、自洽、
无条件的证明至今是公开未解问题。本提交诚实给出两部分内容：(a) 目前已知
最强的真实部分结果及其文献；(b) 对有限区间 [4, 200000] 的逐项计算核验
程序（本文件后半部分）。这构成对题目目标的实质尝试（部分完成），
而不是虚构的完整证明。

## 1. 相关定义

- 素数集 P；表示函数 r(n) = #{(p,q) ∈ P^2 : p+q = n}；目标是证 r(n) >= 1
  对一切偶数 n > 2 成立。
- 奇异级数 S(n) = 2*C2 * ∏_{p|n, p>2} (p-1)/(p-2)，
  其中 C2 = ∏_{p>2} (1 - 1/(p-1)^2) ≈ 0.6601618（孪生素数常数）。
- von Mangoldt 加权和 S(α) = Σ_{m≤n} Λ(m) e(mα)，
  加权表示数 R(n) = ∫_0^1 S(α)^2 e(-nα) dα。

## 2. 使用的引理（真实定理与文献）

引理 A（Estermann 1938）. 不满足哥德巴赫猜想的偶数密度为零；
即几乎所有偶数 n 都有 r(n) >= 1。
出处：T. Estermann, "Proof that almost all even positive integers are
sums of two primes", Proc. London Math. Soc. (2) 44 (1938), 307–314.

引理 B（陈景润 1966；完整证明 1973，"1+2"）. 每个充分大的偶数 n 都可
写成 n = p + P2，其中 p 是素数，P2 是至多两个素数之积。
出处：J.-R. Chen, "On the representation of a larger even integer as the
sum of a prime and the product of at most two primes",
Sci. Sinica 16 (1973), 157–176.

引理 C（Helfgott 2013）. 每个大于 5 的奇数都是三个素数之和
（弱哥德巴赫猜想，已证明）。
出处：H. A. Helfgott, "Major arcs for Goldbach's theorem",
Annals of Mathematics Studies 179, Princeton Univ. Press.

引理 D（Oliveira e Silva–Herzog–Pardi 2014）. 哥德巴赫猜想在
4 ≤ n ≤ 4·10^18 的全部偶数上已被系统计算核验。
出处：T. Oliveira e Silva, S. Herzog, S. Pardi, "Empirical verification
of the even Goldbach conjecture and computation of prime gaps up to
4·10^18", Math. Comp. 83 (2014), 2033–2060.

## 3. 详细推导（本提交实际完成的部分）

由引理 D，猜想在 [4, 4·10^18] 上成立。本提交独立复核其中区间
[4, 200000]：先用 Eratosthenes 筛构造 [2, LIMIT] 的素性表（独立于任何
外部输入），再对每个偶数 n ∈ [4, LIMIT] 寻找最小素数 p 使 n-p 也是素数，
复核 p、q 的素性与 p+q=n，把每个见证 n = p + q 逐条写入 SHA-256 证书。
程序输出 RESULT: PASS 当且仅当区间内没有任何偶数缺失见证；任一 n
找不到见证即以非零状态退出。算法复杂度 O(LIMIT · log log LIMIT)。

## 4. 最终结论与局限

- 已完成：[4, 200000] 区间内全部 99999 个偶数的逐项核验（本程序）；
  真实部分结果（引理 A–D）的整理与文献引用。
- 缺失：完整、自洽、无条件的证明（公开未解问题）。引理 B 的 "1+2"
  与猜想本身之间仍差最后一步：P2 的第二个素因子目前无法排除；
  引理 A 是密度结论，不能覆盖全部偶数。本提交如实声明这一局限。

## 5. 运行方式

    python Goldbach/build/main.py
"""

from __future__ import annotations

import hashlib
import time

import helper

LIMIT = 200_000


def prime_sieve(limit: int) -> bytearray:
    """Build a sieve where flags[i] == 1 exactly when i is prime."""
    flags = bytearray(limit + 1)
    for value in range(2, limit + 1):
        flags[value] = 1
    factor = 2
    while factor * factor <= limit:
        if flags[factor]:
            start = factor * factor
            flags[start:limit + 1:factor] = b"\x00" * (((limit - start) // factor) + 1)
        factor += 1
    return flags


def find_decomposition(n: int, flags: bytearray) -> tuple[int, int] | None:
    """Return the smallest prime p for which n - p is also prime."""
    for p in range(2, n // 2 + 1):
        if flags[p] and flags[n - p]:
            return p, n - p
    return None


def verify_certificate(limit: int) -> tuple[int, int, str, str, str]:
    """Verify every even number up to limit and return certificate stats."""
    flags = prime_sieve(limit)
    digest = hashlib.sha256()
    checked = 0
    largest_prime = 0
    first = ""
    last = ""
    for n in range(4, limit + 1, 2):
        pair = find_decomposition(n, flags)
        if pair is None:
            raise SystemExit(f"missing witness for n = {n}")
        p, q = pair
        if not (flags[p] and flags[q] and helper.is_ordered_pair(n, p, q)):
            raise SystemExit(f"invalid witness for n = {n}: {p} + {q}")
        line = helper.format_witness(n, p, q)
        digest.update(line.encode("utf-8") + b"\n")
        checked += 1
        largest_prime = max(largest_prime, p, q)
        if not first:
            first = line
        last = line
    return checked, largest_prime, digest.hexdigest(), first, last


def main() -> int:
    started = time.perf_counter()
    checked, largest_prime, digest, first, last = verify_certificate(LIMIT)
    elapsed = time.perf_counter() - started
    print("Goldbach certificate")
    print(f"range: 4..{LIMIT} (even numbers)")
    print(f"verified decompositions: {checked}")
    print(f"largest prime used: {largest_prime}")
    print(f"certificate sha256: {digest}")
    print(f"first witness: {first}")
    print(f"last witness:  {last}")
    print(f"verification time: {elapsed:.3f}s")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
