---
paper_title: "Slimmable Neural Networks"
paper_url: https://openreview.net/forum?id=H1gMCsAqY7
---

> [!question]
> What are **Slimmable Neural Networks**?

> [!answer]-
> A Slimmable Neural Network is a **single** neural network executable at **different widths** (number of active channels).
> ![[paste-b41b6392ef1254058e87d648f8e04f17b0f3f067.jpg]]

> [!explanation]-
> This permits **instant and adaptive** accuracy-efficiency trade-offs **at runtime**.

<!-- guid: zr_]ryjRHx -->

---

> [!question]
> What is the **training algorithm** to train **Slimmable Neural Networks**?

> [!answer]-
> ![[paste-4619681eabe23c869f41b376f0ae8e235495e51a.jpg]]

> [!explanation]-
> Or in other words: apply each batch over the slimmed networks (which share weights for each layer but have an individual batchnorm layer) and accumulate the loss. Do a weight update at the end.

<!-- guid: Nn6:bX/%pl -->

---

> [!question]
> What was the **main difficulty** to make **Slimmable Neural Networks** work and how was it solved?

> [!answer]-
> For each layer, different channels/switches result in different means and variances of the aggregated feature, which are then rolling averaged to a shared batch normalization layer. The inconsistency leads to **inaccurate batch normalization statistics** in a layer-by-layer propagating manner.
>
> Note that these batch normalization statistics (moving averaged means and variances) are only used during testing, in training the means and variances of the current mini-batch are used.
>
> The solution was the introduction of **Switchable Batch Normalization (S-BN)**, that employs independent batch normalization for different switches in a slimmable network.

> [!explanation]-
> ![[paste-2831e9519fc33eba4fb0bb50166a0c45efdd85ae.jpg]]

<!-- guid: dU@YsQb@b- -->
