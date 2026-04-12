---
paper_title: "Token Merging: Your ViT But Faster"
paper_url: https://arxiv.org/abs/2210.09461
---

> [!question]
> Give the algorithm for **Token Merging**.

> [!answer]-
> 1. Partition the tokens into two sets $\mathbb{A}$ and $\mathbb{B}$ by alternating the assignment.
> 2. Calculate the similarity score for all tokens in $\mathbb{A}$ by taking the cosine similarity of the $\mathbf{K}$ vector of a token in $\mathbb{A}$ to all tokens in $\mathbb{B}$. The final similarity score of a token in $\mathbb{A}$ is the highest pairwise score.
> 3. Merge the $k$ pairs with the highest similarity score
> 4. Concatenate the two sets back together

> [!explanation]-
> ![[paste-e674aa12e8c0e8302daa5e55a32754f3c9978627.jpg]]

<!-- guid: 41lNu-X}| -->

---

> [!question]
> Apart from the merging module, which other change needs to be made to the standard Vision Transformer in order to apply **Token Merging**?

> [!answer]-
> The standard attention function need to be changed to **proportional attention**:
> $$\mathbf{A} = \operatorname{softmax}(\frac{\mathbf{QK}^T}{\sqrt{d}} + \log(\mathbf{s}))$$*where $\mathbf{s}$ is a row vector containing the size of each token (number of patches the token represents)*. Tokens are also weighted by $\mathbf{s}$ any time they are aggregated, like when the tokens are merged together.

> [!explanation]-
> This performs the same operation as if you'd have *s* copies of the key

<!-- guid: CLLGe@Z<i9 -->

---

> [!question]
> Where is the **Token Merging** module inserted in the vision transformer?

> [!answer]-
> Between the Multi-headed Self-Attention (MSA) layer and the MLP layer.

<!-- guid: MGVm;!!J{A -->

---

> [!question]
> What schedule does **Token Merging** use to merge tokens?

> [!answer]-
> The default setting merges a **fixed** $k$ tokens per layer. 
> They also report on a linearly decreasing schedule.

<!-- guid: j+k)D&~x:} -->
