---
paper_title: "LoRA: Low-Rank Adaptation of Large Language Models"
paper_url: https://arxiv.org/abs/2106.09685
---

> [!question]
> How does **LoRA** work?

> [!answer]-
> LoRA freezes the pre-trained model weights and **injects trainable rank decomposition matrices** into each layer of the Transformer architecture.
> ![[paste-93f70700ed8f25149460afe0c85505cd00ee1d46.jpg]]

> [!explanation]-
> They use a random Gaussian initialization for $A$ and zero for $B$, so $\Delta W = BA$ is zero at the beginning of training.

<!-- guid: f>Ul@5VJS -->
