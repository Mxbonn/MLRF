---
paper_title: "Templates for 3D Object Pose Estimation Revisited: Generalization to New Objects and Robustness to Occlusions"
paper_url: https://arxiv.org/abs/2203.17234
---

> [!question]
> How does the paper **Templates for 3D Object Pose Estimation Revisited: Generalization to New Objects and Robustness to Occlusions** match a real image to the most similar template?

> [!answer]-
> Query image $\mathbf{q}$ (which is already a cropped image with only one object) is passed through a **local feature extraction network** resulting in local features $\mathbf{\bar{q}^{(l)}}$, where $l$ indicates the index of the 2D feature grid. This network is trained in a contrastive manner to maximize the similarity of a real image and the closest rendered template. 
> The most similar template is the one with the **highest similarity score**:
> $$\operatorname{sim}^*(\bar{\mathbf{q}}, \bar{\mathbf{t}}) = \frac{1}{|\mathcal{M}|} \sum_l \mathcal{M}^{(l)} \mathcal{O}^{(l)} \mathcal{S} \left( \bar{\mathbf{q}}^{(l)}, \bar{\mathbf{t}}^{(l)} \right),$$where $\mathcal{M}$ is a 2D binary visibility mask for template $\mathbf{t}$, $\mathcal{S}$ is a local similarity metric such as the cosine similarity, $\mathcal{O}^{(l)} = \mathbb{1}_{\mathcal{S}(\bar{\mathbf{q}}^{(l)}, \bar{\mathbf{t}}^{(l)}) &gt; \delta}$, with $\delta$ a threshold applied to the similarity to *turn off* the occluded local features.

<!-- guid: OV#HlRSegT -->

---

> [!question]
> **Which loss function** is used to the train the **local feature network** in **Templates for 3D Object Pose Estimation Revisited: Generalization to New Objects and Robustness to Occlusions**?

> [!answer]-
> The [**InfoNCE**](https://arxiv.org/abs/1807.03748) loss function:
> $$\mathcal{L} = - \sum_{i=1}^N \log \frac{\exp \left( \operatorname{sim}(\bar{\mathbf{q}}_i, \bar{\mathbf{t}}_i) / \tau \right)}{\sum_{k=1}^N \mathbb{1}_{[k \ne i]} \exp \left( \operatorname{sim}(\bar{\mathbf{q}}_i, \bar{\mathbf{t}}_k) / \tau \right)}$$
>  Previous papers used the **Triplet loss** function but this performs worse.

> [!explanation]-
> This loss is also known as the **NT-Xent loss **in in the SimCLR paper.

<!-- guid: b.;~HE38#3 -->

---

> [!question]
> **How** is the **local feature network trained** in *Templates for 3D Object Pose Estimation Revisited: Generalization to New Objects and Robustness to Occlusions*?

> [!answer]-
> ![[paste-e1bcc9e9b6d9933279578fdffe7e336b2b0cde5e.jpg]]
> In each training iteration, $N$ positive pairs, where a pair is a real image and a synthetic render of the same object with at most 5° difference in viewpoint angle. All the pairs composed by a real image and a synthetic render of a different object or a dissimilar pose are defined as negative pairs. 
> A **convolutional neural network** that outputs a **2D local feature representation** is trained using the **contrastive learning** loss InfoNCE.

<!-- guid: J_AA1+uM`K -->
