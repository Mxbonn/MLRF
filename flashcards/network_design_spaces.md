---
paper_title: "On Network Design Spaces for Visual Recognition"
paper_url: https://arxiv.org/abs/1905.13214
---

> [!question]
> Which **metric **is a better and more robust way to **compare model families** (e.g. ResNets vs VGG family) than the traditional way of point estimates or a curve estimate of a handful of picked models (see Fig 1 (a) and (b))
> ![[paste-6b860bdb1b0691e2f86c94feeeed1367d2cfc801.jpg]]

> [!answer]-
> Comparing **empirical distribution functions (EDFs)** is a better way. 
> Specifically one can compare the **error EDF:
> $$F(e) = \frac{1}{n} \sum^n_{i=1} \mathbb{1}[e_i &lt; e]$$
> **
> $F(e)$ gives the fraction of models with error less than e.
> ![[paste-78908eece335f4117a6e66fe054acea7613bf2f3.jpg]]

<!-- guid: n(bSfU~#u2 -->

---

> [!question]
> What is an issue with the** error EDF** **$$F(e) = \frac{1}{n} \sum^n_{i=1} \mathbb{1}[e_i &lt; e]$$ **when comparing distributions of different network families, and how can it be solved?

> [!answer]-
> **It does not control for confounding factors like network complexity. **Model families which in general produce models of a larger complexity tend to have a better error.
> ![[paste-525ee15f00c2312faf9e0a0e8da41d7ab092b241.jpg]]
>
> This can be solved by working with a <b style="text-decoration-line: underline;">normalized</b> **error EDF:
> $$F(e) = \frac{1}{n} \sum^n_{i=1} w_i\mathbb{1}[e_i &lt; e]$$**
>
> In practice, we set the weights for a model set such that its complexity distribution is uniform. Specifically, we bin the complexity range into $k$ bins, and assign each of the $m_j$ models that fall into a bin $j$ a weight $w_j = \frac{1}{km_j}$ .

> [!explanation]-
> ![[paste-73cde3128d35db5563abaacb483cf0633d574d21.jpg]]

<!-- guid: y^.|iwu>CD -->
