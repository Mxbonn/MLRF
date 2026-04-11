---
paper_title: "Multiple Choice Learning: Learning to Produce Multiple Structured Outputs"
paper_url: https://papers.nips.cc/paper_files/paper/2012/hash/cfbce4c1d7c425baf21d6b6f2babe6be-Abstract.html
---

> [!question]
> What is a common **technique** used to calculate the **loss for models with multiple outputs** (e.g. Segment Anything)?

> [!answer]-
> **Compute the loss for each of the predicted outputs, but only backpropagate the lowest loss.** 
>
> Let $\hat{Y}_i = \{\hat{y}^1_i, ..., \hat{y}^M_i\}$ be the set of predicted outputs for input $x_i$.
> $$\mathcal{L}(\hat{Y}_i) = \operatorname{min}_{\hat{y}_i \in\hat{Y}_i} \mathcal{l}(y_i, \hat{y}_i)$$

<!-- guid: AC3=>4&L^W -->
