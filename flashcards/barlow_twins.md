---
paper_title: "Barlow Twins: Self-Supervised Learning via Redundancy Reduction"
paper_url: https://arxiv.org/abs/2103.03230
---

> [!question]
> What is the **loss** used in **Barlow Twins**?

> [!answer]-
> $$\mathcal{L}_\text{BT} = \underbrace{\sum_i (1-\mathcal{C}_{ii})^2}_{\text{invariance term}} + \lambda \underbrace{\sum_i\sum_{i\neq j} \mathcal{C}_{ij}^2}_{\text{redundancy reduction term}}$$
>
> where the cross-correlation matrix element is:
> $$\mathcal{C}_{ij} = \frac{\sum_b \mathbf{z}^A_{b,i} \mathbf{z}^B_{b,j}}{\sqrt{\sum_b (\mathbf{z}^A_{b,i})^2}\sqrt{\sum_b (\mathbf{z}^B_{b,j})^2}}$$
>
> Here $\mathbf{z}$ are the embeddings of the networks and $\lambda$ is a positive constant trading off the importance of both terms of the loss.

> [!explanation]-
> Intuitively, the* invariance term* of the objective, by trying to equate the diagonal elements of the cross-correlation matrix to 1, makes the embedding invariant to the distortions applied. 
> The *redundancy reduction term*, by trying to equate the off-diagonal elements of the cross-correlation matrix to 0, decorrelates the different vector components of the embedding. This decorrelation reduces the redundancy between output units, so that the output units contain non-redundant information about the sample.

<!-- guid: GHQ$wXrHO[ -->

---

> [!question]
> Give an overview of the **Barlow Twins** method.

> [!answer]-
> ![[barlow-twins.png]]
> Barlow Twins's objective function measures the cross-correlation matrix between the embeddings of two identical networks fed with distorted versions of a batch of samples, and tries to make this matrix close to the identity. This causes the embedding vectors of distorted versions of a sample to be similar, while minimizing the redundancy between the components of these vectors.

<!-- guid: g-i1W70DQZ -->

---

> [!question]
> Give PyTorch-style **pseudocode** for **Barlow Twins**.

> [!answer]-
> ![[barlow-twins-algo.png]]

<!-- guid: w{sqF8vWDC -->

---

> [!question]
> What is an important advantage of Barlow Twins compared to previous work?

> [!answer]-
> It does not require large number of negative samples and **can thus operate on small batches**.

<!-- guid: c0Nr?rw[R! -->
