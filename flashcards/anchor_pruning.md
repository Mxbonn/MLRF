---
paper_title: "Anchor Pruning for Object Detection"
paper_url: https://arxiv.org/abs/2104.00432
---

> [!question]
> What is **Anchor pruning** in the context of object detection?

> [!answer]-
> Anchor pruning is **a pruning technique for object detection**, which removes redundant anchors in the detection head.

<!-- guid: OEM$imd*-E -->

---

> [!question]
> How does **Anchor Pruning** work?

> [!answer]-
> Anchor Pruning **starts from a fully trained model**.
> Using a search algorithm, the search space of possible anchor configurations is explored efficiently.
>
> The result of the search algorithm is **a set of anchor configurations that are Pareto-efficient**.
>
> After selecting a Pareto-optimal anchor configuration, **the accuracy can be improved by training this configuration again from scratch.**

<!-- guid: BiGsET<1}2 -->

---

> [!question]
> Why does **Anchor pruning** have larger impact on the running time of object detection models than just the FLOPS reduction?

> [!answer]-
> The running time of an object detection model in an embedded context is **often dominated by the running time of the post processing steps**, which is **directly related to the number of bounding boxes** that are produced by the network. This post-processing step is however not included in the FLOPS count.

<!-- guid: H@Q]v(c|Z, -->

---

> [!question]
> What is an **Overanchorized** network?

> [!answer]-
> It is as an object detection model that has more anchors than strictly needed.

> [!explanation]-
> An **Overanchorized** network can be used as base model to start **anchor pruning** from, this avoids having to experiment with many different anchor shape initializations.

<!-- guid: D={>vr/o#% -->

---

> [!question]
> When is an **object detection anchor** redundant?

> [!answer]-
> An anchor is redundant when it produces bounding boxes that are (almost) completely covered by predictions of neighboring anchors.

> [!explanation]-
> The distribution of bounding boxes produced by different anchors shows that for certain anchors, many of the predictions can also be produced by neighboring anchors.
> ![[paste-29cb9f63c29359137bcc9ec0955143062da12061.jpg]]

<!-- guid: d0:e[[Vlat -->

---

> [!question]
> What is an **anchor-based** object detector?

> [!answer]-
> Anchor-based detectors associate some predefined anchors to each feature layer to which the detection head is attached. Usually, the anchors are defined in terms of size and aspect ratio. **The classifier and regressor in the detection head output the class scores and the 4 offsets relative to the predefined anchor shape for each pixel in a feature map.**

> [!explanation]-
> ![](https://nl.mathworks.com/help/vision/ug/ssd_detection.png)
> Anchor boxes are associated with each pixel in every feature map.
>
> The final bounding box predictions are made as classification predictions + offset predictions from the anchor.

<!-- guid: r`cf9VN23L -->

---

> [!question]
> Which technique can reduce the FLOPS of the **object detection <u>head</u>** **by 50% without loss in accuracy**?

> [!answer]-
> **Anchor Pruning**

<!-- guid: s%~Q(Sp/yK -->
