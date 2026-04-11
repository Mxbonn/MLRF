---
paper_title: "Multi-Scale Context Aggregation by Dilated Convolutions"
paper_url: https://arxiv.org/abs/1511.07122
---

> [!question]
> What is the mathematical formula of a **dilated convolution **$\left(k \ast_{l} f\right)_t$?

> [!answer]-
> $\left(k \ast_{l} f\right)_t = \sum_{\tau=-\infty}^{\infty} k_\tau \cdot f_{\tau - lt}$,
> where $l$ is the dilation factor.

> [!explanation]-
> $l = 1$ equals a normal convolution

<!-- guid: q]2OXN!^$) -->

---

> [!question]
> What is a different name for a **dilated** convolution?

> [!answer]-
> **Atrous **convolution.

<!-- guid: rgD@/f8b,7 -->

---

> [!question]
> What is a different name for an **atrous **convolution?

> [!answer]-
> **Dilated **convolution.

<!-- guid: xTKiqg9P<^ -->

---

> [!question]
> If this images demonstrates a normal convolution, visualize how a dilated convolution $l = 2$ would look like.
> ![[0oX5IPr7TlVM2NpEU.gif]]

> [!answer]-
> ![[03cTXIemm0k3Sbask.gif]]

<!-- guid: zAJEla>bD# -->
