---
paper_title: "FaceNet: A Unified Embedding for Face Recognition and Clustering"
paper_url: https://arxiv.org/abs/1503.03832
---

> [!question]
> Give the formula for the **Triplet Loss**.

> [!answer]-
> $$\mathcal{L}_\text{triplet}(\mathbf{x}, \mathbf{x}^+, \mathbf{x}^-) = \sum_{\mathbf{x} \in \mathcal{X}} \max\big( 0, \|f(\mathbf{x}) - f(\mathbf{x}^+)\|^2_2 - \|f(\mathbf{x}) - f(\mathbf{x}^-)\|^2_2 + \alpha \big)$$
> where $\mathbf{x}$ is the an anchor input (e.g. an image of a specific person), $\mathbf{x}^+$ is a positive sample (meaning that it belongs to the same class as $\mathbf{x}$) and $\mathbf{x}^-$ is a negative sample (i.e. from a different class).
> $\alpha$ is a margin that is enforced between positive and negative pairs.

> [!explanation]-
> ![[triplet-loss.png]]
> Illustration: The Triplet Loss minimizes the distance between an *anchor* and a *positive*, both of which have the same identity, and maximizes the distance between the *anchor* and a *negative* of a different identity.

<!-- guid: u2~sQ~EtPb -->

---

> [!question]
> What is an important **limitation** of the **triplet loss** function?

> [!answer]-
> It requires **large batches in the order of a few thousand examples**.
> In order to have meaningful positive and negative paris, a minimal samples of each class need to be present in each batch.

<!-- guid: t=hxxrzgly -->

---

> [!question]
> In **triplet loss**, how are the anchor $\mathbf{x}$, positive $\mathbf{x}^+$ and negative $\mathbf{x}^-$ triplets selected?

> [!answer]-
> Using large batches,** all anchor-positive pairs** are selected.
> **Negatives** are selected such that $\|f(\mathbf{x}) - f(\mathbf{x}^+)\|^2_2 &lt; \|f(\mathbf{x}) - f(\mathbf{x}^-)\|^2_2 $. These negatives are called *semi-hard*.

<!-- guid: *0?.?#HKX -->
