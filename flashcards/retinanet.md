---
paper_title: "Focal Loss for Dense Object Detection"
paper_url: https://arxiv.org/abs/1708.02002
---

> [!question]
> What is according to the **RetinaNet **paper the **main obstacle for one-stage detectors** to achieve state-of-the-art accuracy?

> [!answer]-
> **Class imbalance** during training.

> [!explanation]-
> **Note**: More recent one-stage detectors have not adopted focal loss and have shown that it does not necessarily result in better accuracy.

<!-- guid: BKbQ-a*K5Z -->

---

> [!question]
> How is **class imbalance** an issue for object detectors and how does **SSD **solve this issue compared to **RetinaNet**?

> [!answer]-
> One-stage object detectors evaluate $10^4-10^5$ candidate locations per image but only a few locations contain objects. This imbalance causes two problems: 
> (1) training is inefficient as most locations are easy negatives 
> (2)  the easy negatives can overwhelm training and lead to degenerate models.
> **SSD **solves this by **hard negative mining**.
> **RetinaNet** uses **Focal Loss** that down-weights easy examples.

<!-- guid: rX(!&sGK|# -->

---

> [!question]
> Give the mathematical definition for the **Focal Loss**.

> [!answer]-
> **$$FL(p_t) = -(1 - p_t)^{\gamma} log(p_t)$$
> **with $\gamma \ge 0$ a tunable *focusing* parameter and where 
> $$ p_t = \begin{cases} p &amp; \text{if } y = 1 \\
> 1 - p &amp; \text{if } y = 0 \end{cases} $$
> with $p \in [0,1]$ the model's estimated probability for the class with label $y=1$

> [!explanation]-
> In practice we use an $\alpha$-balanced variant of the focal loss:
> **$$FL(p_t) = -\alpha_t(1 - p_t)^{\gamma} log(p_t)$$
> **![[paste-556541a621df1e615336ac514face4107ed4166b.jpg]]**
> **

<!-- guid: QG?M|;Vez0 -->

---

> [!question]
> How does **focal loss** relate to the **cross entropy loss**?

> [!answer]-
> Focal loss adds a modulating factor $(1 - p_t)$ to the cross entropy loss.
> As $p_t \to 1$, the factor goes to 0 and the loss for well-classified examples is down-weighted. 
> The focusing parameter  $\gamma$ smoothly adjusts the rate at which easy examples are downweighted. **When $\gamma = 0$, focal loss is equivalent to cross entropy loss**, and as $\gamma$ is increased the effect of the modulating factor is likewise increased.

> [!explanation]-
> ![[paste-556541a621df1e615336ac514face4107ed4166b.jpg]]

<!-- guid: mUSQ!?#qIV -->

---

> [!question]
> How is the **focal loss** of an entire image calculated?

> [!answer]-
> The total focal loss of an image is computed as the **sum** of the focal loss over all anchors, **normalized** by the number of anchors assigned to a ground-truth box.

<!-- guid: s-f6CF|~x= -->

---

> [!question]
> Draw the architecture of **RetinaNet**.

> [!answer]-
> ![[paste-cb15da58ea668d1da71d7664f4000f56c141deeb.jpg]]
> RetinaNet is a **one-stage object detector** with **ResNet **as backbone, a feature pyramid network (**FPN**) as neck and head that is **shared **for all feature layers.

> [!explanation]-
> RetinaNet follows the **one-stage** **object detection** architecture, the main innovation of RetinaNet was the **loss function**.

<!-- guid: e$g#+#_Fyo -->
