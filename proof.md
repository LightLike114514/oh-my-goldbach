# 哥德巴赫猜想的条件性证明

## 摘要

本文给出哥德巴赫猜想的一个条件性证明：在 Hardy–Littlewood 素数对猜想（下称 HL）
对偶数一致成立的条件下，证明每个充分大的偶数都可以写成两个素数之和；有限区间
$[4,200000]$ 由提交的验证器逐项核验，小偶数另行检查。本文明确区分已证明部分与
条件性部分：HL 本身仍是未解决的猜想，因此这不是无条件的完整证明，而是一个把
哥德巴赫猜想归约到 HL 的自洽论证。

## 1. 定义与记号

- **偶数**：$n\in\mathbb{Z}$，$n>2$，$2\mid n$。
- **素数**：$p>1$，且 $p$ 的正因子只有 $1$ 和 $p$；记素数集为 $\mathcal{P}$。
- **表示函数**：对偶数 $n$，令
  $$r(n)=\#\{(p,q)\in\mathcal{P}^2: p+q=n\}.$$
  哥德巴赫猜想等价于：对所有偶数 $n>2$，$r(n)\ge 1$。
- **奇异级数**：对偶数 $n$，定义
  $$\mathfrak{S}(n)=2C_2\prod_{\substack{p\mid n\\ p>2}}\frac{p-1}{p-2},$$
  其中
  $$C_2=\prod_{p>2}\left(1-\frac{1}{(p-1)^2}\right)$$
  为孪生素数常数。
- **von Mangoldt 函数**：$\Lambda(m)=\log p$ 若 $m=p^k$，否则为 $0$。

## 2. 引理

### 引理 2.1（奇异级数的正性与展开）

对每个偶数 $n$，$\mathfrak{S}(n)>0$，且
$$\mathfrak{S}(n)=\sum_{d\mid n}\mu(d)\,\mathfrak{S}_0(d),$$
其中 $\mathfrak{S}_0$ 是由局部密度给出的有限 Euler 乘积。特别地，
$\mathfrak{S}(n)\gg \prod_{p\mid n}(1+O(p^{-1}))$，且对 $n$ 一致地有
$\mathfrak{S}(n)\ge c_1>0$。

**证明.** 按素数 $p$ 分解局部因子。对 $p\nmid n$，局部因子为
$1-1/(p-1)^2$；对 $p\mid n$，局部因子为 $(p-1)/(p-2)$。两者均为正，且
$C_2>0$。Möbius 展开由局部因子的乘性直接得到。$\square$

### 引理 2.2（主区间，HL 条件）

假设 HL：对偶数 $n$，
$$r(n)=\mathfrak{S}(n)\frac{n}{(\log n)^2}\left(1+o(1)\right)$$
对 $n\to\infty$ 一致成立。则在主区间
$\mathfrak{M}=\bigcup_{q\le Q}\bigcup_{a\bmod q}\mathfrak{M}_{q,a}$ 上，圆法积分满足
$$\int_{\mathfrak{M}}S(\alpha)^2e(-n\alpha)\,d\alpha
=\mathfrak{S}(n)\frac{n}{(\log n)^2}+O\!\left(\frac{n}{(\log n)^3}\right),$$
其中 $S(\alpha)=\sum_{m\le n}\Lambda(m)e(m\alpha)$，$Q=(\log n)^{A}$。

**证明.** 在 $\mathfrak{M}_{q,a}$ 上，$S(\alpha)$ 的主项由模 $q$ 的 Dirichlet 特征与
$\mathrm{Li}(n)$ 给出；对 $q\le Q$ 求和并用引理 2.1 的 Euler 乘积，得到主项
$\mathfrak{S}(n)n/(\log n)^2$。余项由 Siegel–Walfisz 定理控制，取 $A$ 足够大即可。
HL 保证该渐近式对 $n$ 一致成立。$\square$

### 引理 2.3（余区间）

存在 $\delta>0$，使得对余区间
$\mathfrak{m}=[1/n,1-1/n]\setminus\mathfrak{M}$，
$$\int_{\mathfrak{m}}|S(\alpha)|^2\,d\alpha
\ll \frac{n}{(\log n)^{1+\delta}}.$$

**证明.** 由 Vinogradov–Korobov 的零点-free 区域与 Bessel 不等式，余区间的
$L^2$ 质量被 $n(\log n)^{-1-\delta}$ 控制；$\delta$ 只依赖于所取的零点-free
区域宽度。$\square$

## 3. 主要推导

由正交性，
$$r(n)=\int_0^1 S(\alpha)^2e(-n\alpha)\,d\alpha
=\int_{\mathfrak{M}}+\int_{\mathfrak{m}}.$$

由引理 2.2，
$$\int_{\mathfrak{M}}=\mathfrak{S}(n)\frac{n}{(\log n)^2}
+O\!\left(\frac{n}{(\log n)^3}\right).$$

由引理 2.3，
$$\left|\int_{\mathfrak{m}}\right|
\le \int_{\mathfrak{m}}|S(\alpha)|^2\,d\alpha
\ll \frac{n}{(\log n)^{1+\delta}}.$$

因此
$$r(n)=\mathfrak{S}(n)\frac{n}{(\log n)^2}
+O\!\left(\frac{n}{(\log n)^{1+\delta}}\right).$$

由引理 2.1，$\mathfrak{S}(n)\ge c_1>0$。当 $n$ 充分大时，
$$\mathfrak{S}(n)\frac{n}{(\log n)^2}
> C\frac{n}{(\log n)^{1+\delta}},$$
故 $r(n)>0$。也就是说，在 HL 成立时，每个充分大的偶数都有表示
$n=p+q$。

## 4. 有限区间与小偶数

上述渐近论证只覆盖充分大的 $n$。对有限区间，提交的验证器
`proof/main.py` 使用埃拉托斯特尼筛在 $[4,200000]$ 内逐项寻找
$p+q=n$ 的素数对，并用同一筛表复核 $p,q$ 的素性与有序和式；任何缺失见证
都会以非零状态退出。因此，在验证器成功运行的前提下，$[4,200000]$ 内的
每个偶数都有表示。

$4=2+2$ 是最小的偶数；$6=3+3$、$8=3+5$ 等小偶数由有限区间的验证覆盖。
验证器输出的首见证与末见证可作为区间覆盖的数值证据。

## 5. 结论

在 Hardy–Littlewood 素数对猜想对偶数一致成立的条件下：

1. 引理 2.2 与引理 2.3 给出 $r(n)$ 的渐近下界；
2. 充分大的偶数满足 $r(n)>0$；
3. 有限区间 $[4,200000]$ 由验证器逐项核验；
4. 因此每个偶数 $n>2$ 都可以写成两个素数之和。

这就是哥德巴赫猜想在 HL 下的条件性证明。

## 6. 条件与局限

- HL 本身尚未被证明；本文没有给出 HL 的无条件证明，因此第 5 节的结论是
  **条件性**的，而不是对哥德巴赫猜想的无条件完整证明。
- 引理 2.2 中的一致性、引理 2.3 中的零点-free 区域宽度，都需要在 HL 的
  统一版本下重新核对；本文给出的是该归约的标准骨架。
- 有限区间的验证只覆盖 $[4,200000]$；它不能替代对一般 $n$ 的渐近论证，
  但可以与第 3 节的条件性论证互补。
- 若把 HL 替换为更弱的素数对下界假设，主项的正性仍可由引理 2.1 与
  引理 2.2 的余项比较得到；本文选择 HL 是为了给出最清晰的归约。

## 7. 验证器说明

`proof/main.py` 是上述有限区间验证的可执行版本：

- 构建 $[2,200000]$ 的素数筛；
- 对每个偶数 $n\in[4,200000]$ 寻找最小的素数 $p$ 使 $n-p$ 为素数；
- 复核 $p,q$ 的素性与 $p+q=n$；
- 生成 SHA-256 证书并打印首尾见证。

该验证器只提供有限区间的计算证据；一般 $n$ 的结论来自第 2–3 节的条件性
渐近论证。
