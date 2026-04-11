---
paper_title: "DETR: End-to-End Object Detection with Transformers"
paper_url: https://arxiv.org/abs/2005.12872
---

> [!question]
> Draw the architecture of **DETR**.

> [!answer]-
> ![[paste-132b224ca8ac9dcdf056c2b7737a8ffb47c0e9c1.jpg]]![[paste-3a35091f801c1a07f766a113cc4bf98fe9d7225f.jpg]]

<!-- guid: LkzJPdb/!? -->

---

> [!question]
> While **DETR **has a better AP than previous CNN based object detection algorithms, in which aspects is it worse than those models?

> [!answer]-
> DETR performs **worse on small objects**.
> DETR requires **extra-long training**.

<!-- guid: l{=hYS<?DL -->

---

> [!question]
> Why is **DETR **called an **End-to-End** detector?

> [!answer]-
> DETR predicts all objects at once, without an intermediate step such as non-maximal suppression.

> [!explanation]-
> This is done using a **set loss function** which performs **bipartite matching** between predicted and ground-truth objects.

<!-- guid: mGlCpqb_P> -->

---

> [!question]
> How does **DETR** match predictions with ground-truth?

> [!answer]-
> DETR uses **bipartite matching** between predicted and ground truth objects.
>
> Let us denote by $y$ the ground truth set of objects, and $\hat{y} = \{\hat{y}_i\}_{i=1}^{N}$ the set of $N$ predictions.
>
> *Assuming $N$ is larger than the number of objects in the image*,
>
> we consider $y$ also as a set of size $N$ padded with $\emptyset$ (no object).
>
> To find a bipartite matching between these two sets we search for a permutation of $N$ elements $\sigma \in \Sigma_N$ with the lowest cost:
>
> $$\hat{\sigma} = \text{argmin}_{\sigma\in\Sigma_N} \sum_{i}^{N} L_{match}(y_i, \hat{y}_{\sigma(i)}),$$
>
> where $\cal{L}_{match}(y_i, \hat{y}_{\sigma(i)})$ is a pair-wise matching cost between ground truth $y_i$ and a prediction with index $\sigma(i)$. 
> This optimal assignment is computed efficiently with the **Hungarian algorithm**.
>
> The matching cost takes into account both the class prediction and the similarity of predicted and ground truth boxes. Each element $i$ of the ground truth set can be seen as a $y_i = (c_i, b_i)$ where $c_i$ is the target class label (which may be $\emptyset$) and $b_i \in [0, 1]^4$ is a vector that defines ground truth box center coordinates and its height and width relative to the image size. For the prediction with index $\sigma(i)$ we define probability of class $c_i$ as $\hat{p}_{\sigma(i)}(c_i)$ and the predicted box as $\hat{b}_{\sigma(i)}$. With these notations we define
>
> $\cal{L}_{match}(y_i, \hat{y}_{\sigma(i)})$ as $-\mathbb{1}_{\{c_i\neq\emptyset\}}\hat{p}_{\sigma(i)}(c_i) + \mathbb{1}_{\{c_i\neq\emptyset\}} \cal{L}_{box}(b_{i}, \hat{b}_{\sigma(i)})$.

<!-- guid: PJ#-8Ey8Y1 -->

---

> [!question]
> Which **loss function** is used in **DETR**?

> [!answer]-
> The **Hungarian loss**. 
>
> Which is a linear combination of a <u>negative log-likelihood </u>for class prediction and a box loss:
>
> $$\cal{L}_{Hungarian}(y, \hat{y}) = \sum_{i=1}^N \left[-\log \hat{p}_{\hat{\sigma}(i)}(c_{i}) + \mathbb{1}_{\{c_i\neq\emptyset\}} \cal{L}_{box}(b_{i}, \hat{b}_{\hat{\sigma}}(i))\right]$$
>
> where 
> $$\cal{L}_{box}(b_{i}, \hat{b}_{\hat{\sigma}}(i)) = \lambda_{\rm iou}\cal{L}_{iou}(b_{i}, \hat{b}_{\sigma(i)}) + \lambda_{\rm L1}||b_{i}- \hat{b}_{\sigma(i)}||_1 $$
> with $\cal{L}_{iou}$ the <u>generalized IoU loss</u> and $\hat{\sigma}$ the optimal assignment computed with the <u>Hungarian algorithm</u>.

<!-- guid: Ok6w68_sEk -->

---

> [!question]
> How does **DETR **produce N predictions.

> [!answer]-
> The predictions come from the **transformer decoder**.
>
> The decoder follows the standard architecture of the transformer, transforming $N$ embeddings of size $d$ using multi-headed self- and encoder-decoder attention mechanisms. The difference with the original transformer is that our model decodes the $N$ objects in *parallel *at each decoder layer.
>
> Since the decoder is also permutation-invariant, the $N$ input embeddings must be different to produce different results. These input embeddings are *learnt positional encodings* that we refer to as **object queries**, and similarly to the encoder, we add them to the input of each attention layer. 
>
> The $N$ object queries are transformed into an output embedding by the decoder. They are then *independently *decoded into box coordinates and class labels by a feed forward network, resulting $N$ final predictions. Using self- and encoder-decoder attention over these embeddings, the model globally reasons about all objects together using pair-wise relations between them, while being able to use the whole image as context.

<!-- guid: hqkYHP-fZ& -->

---

> [!question]
> How many FLOPS and parameters does the **DETR **model have? And how accurate is it on COCO?

> [!answer]-
> **86G FLOPS** and **41M** parameters with **AP 42.0** on COCO.

<!-- guid: oEa*`6IEbt -->
