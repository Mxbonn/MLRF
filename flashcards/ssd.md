---
paper_title: "SSD: Single Shot MultiBox Detector"
paper_url: https://arxiv.org/abs/1512.02325
---

> [!question]
> What is the general **architecture** of the **Single-Short Detector** (SSD)?

> [!answer]-
> ![[SSD-architecture.png]]
> A Single-Shot Detector uses a **backbone network**, to which it adds **additional convolutional feature layers**.
> These layers decrease in size progressively and allow predictions at multiple scales.
> Attached to each feature layer (or optionally an exisiting feaure layer from the base network) is **a convolutional detection layer that produces a fixed set of predictions.**
> These predicted bounding boxes and scores are then processed by a **non-maximum suppression** step to produce the final detections.

<!-- guid: jS!ZE~T@qr -->

---

> [!question]
> How does **SSD** produce predicted bounding boxes?

> [!answer]-
> ![[paste-28e1a0071791e496e97be0d7a222423d4bfcfddb.jpg]]
> In a convolutional fashion, SSD evaluates a small set (e.g. 4) of default boxes of different aspect ratios at each location in several feature maps with different scales (e.g. $8 \times 8$ and $4 \times 4$ in (b) and (c)). For each default box, we predict
> both the shape offsets and the confidences for all object categories ($(c_1, c_2,... , c_p)$).

<!-- guid: NgPR!8uW,= -->

---

> [!question]
> What are the **defining parameters of anchor boxes** in SSD?

> [!answer]-
> Anchor boxes are defined by their **scale $s$** and **aspect ratio $a$**.
> The width and the height of the each default box is then computed as: $w = s\sqrt{a}$, $h = \frac{s}{\sqrt{a}}$.

<!-- guid: dK`dHM}f5m -->

---

> [!question]
> Why are **anchor boxes in SSD** defined using the square root of the aspect ratio?

> [!answer]-
> By taking the square root of the aspect ratio and multiplying it for one side and dividing for the other side, you still get the desired aspect ratio, while also **keeping the area equal to the scale$^{[1]}$**. 
> ![[paste-f951f0ac6e7229baff67587f7d2344d0d1aafbad.jpg]]

> [!explanation]-
> [1]: https://twitter.com/Mxbonn/status/1252933371682066432

<!-- guid: KewPHfsQT) -->

---

> [!question]
> *During training*, **how** does SSD determine which default bounding boxes correspond to a ground truth box?

> [!answer]-
> A default bounding box **matches any ground truth box with jaccard overlap higher than a threshold** (0.5).

> [!explanation]-
> This simplifies the learning problem, allowing the network to predict high scores for multiple overlapping default boxes rather than requiring it to pick only the one with maximum overlap.

<!-- guid: I{cd?N6~8{ -->

---

> [!question]
> *During training*, **how** does **SSD** deal with the large number of default bounding boxes that do not match with a ground truth box?

> [!answer]-
> SSD uses a technique called **hard negative mining**:
> Instead of using all the negative examples, SSD training sorts them using the highest confidence loss for each default box and picks the top ones so that the **ratio between the negatives and positives is at most $3:1$**.

<!-- guid: hZyGVzcTGN -->

---

> [!question]
> What **loss function** is used in **SSD**?

> [!answer]-
> The loss function is the sum of a localization loss and a classification loss.
> $$\mathcal{L} = \frac{1}{N}(\mathcal{L}_\text{cls} + \alpha \mathcal{L}_\text{loc})$$
> where $N$ is the number of matched bounding boxes and $\alpha$ balances the weights between two losses, picked by cross validation.
>
> The **localization loss** is a **smooth L1 loss** between the predicted bounding box correction and the true values.
> The **classification loss** is a **softmax loss** over multiple classes

<!-- guid: K<?IkH[*H? -->

---

> [!question]
> How does **SSD** match predicted bounding boxes with the ground truth?

> [!answer]-
> SSD matches each ground truth box to the default box with the best jaccard overlap and then matches default boxes to any ground truth with jaccard overlap higher than a threshold (0.5).

> [!explanation]-
> This simplifies the learning problem, allowing the network to predict high scores for multiple overlapping default boxes rather than requiring it to pick only the one with maximum overlap.

<!-- guid: iXPg77Qy6h -->
