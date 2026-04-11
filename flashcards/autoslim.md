---
paper_title: "AutoSlim: Towards One-Shot Architecture Search for Channel Numbers&nbsp;"
paper_url: https://arxiv.org/abs/1903.11728
---

> [!question]
> What is the main goal of the **AutoSlim **paper (Follow up work on Slimmable Networks)?

> [!answer]-
> AutoSlim proposes a way to **obtain optimized channel configurations under different resource constraints**.
> In other words: It solves the question of how to select the most accurate nonuniformly slimmed network for a given resource constraint.

> [!explanation]-
> Note: This paper was rejected from ICLR 2020.

<!-- guid: AoVNA[SCWi -->

---

> [!question]
> What is the work flow of the **AutoSlim** approach?

> [!answer]-
> ![[paste-8e7aff54113097dddfe8baece6e2cd351991ac4e.jpg]]
> 1. Start from a standard Network (e.g. Mobilenet).
>
> 2. Train a universal slimmable model for 10-20% of the full training epochs.
>
> 3. Start with the largest model (e.g. $1.0 \times$ or $1.5 \times$) and compare the network accuracy among the possibilities where each layer is slimmed by one channel group. Then greedily slim the layer with minimal accuracy drop. Stop when reaching the constraint.
>
> 4. Train the optimized network from scratch.

<!-- guid: j5u_y8k.`u -->
