---
paper_title: "MobileNetV2: Inverted Residuals and Linear Bottlenecks"
paper_url: https://arxiv.org/abs/1801.04381
---

> [!question]
> Which novel layer module was introduced in MobileNetV2?

> [!answer]-
> The inverted residual with linear bottleneck.

<!-- guid: uszt9su9>2 -->

---

> [!question]
> How does the convolutional module in MobileNetV2 reduce the memory footprint?

> [!answer]-
> By only having large tensors in an intermediate state.

> [!explanation]-
> Large tensors are only used inside the inverted residual with linear bottleneck. Therefore they don't need to be stored in main memory, as would be the case in a module where the large tensors are used in for example a residual connection.

<!-- guid: L5~a;3}$~S -->

---

> [!question]
> When is an inverted residual block (MobileNetV2) conceptually the same as a classical residual block?

> [!answer]-
> When the expansion factor is smaller than 1.

<!-- guid: fBNp*X,<x@ -->

---

> [!question]
> Which activation function is used in MobileNetV2?

> [!answer]-
> RELU6

<!-- guid: qcU}q:QY|l -->

---

> [!question]
> What is the reason **RELU6 **is used in **MobileNetV2**?

> [!answer]-
> Because of its robustness when used with low-precision computation

<!-- guid: h!a-LEP}?X -->

---

> [!question]
> How many multiply-adds and parameters does the default **MobileNetV2 **have? And how much accuracy does it get on ImageNet?

> [!answer]-
> **300M MAdds** and **3.4M parameters**, with an accuracy of **72%** on ImageNet.

<!-- guid: M1D[R8W0CH -->

---

> [!question]
> What is changed from SSD in SSDLite?

> [!answer]-
> All regular convolutions are replaced by separable convolutions.

<!-- guid: f;ATHWa^?? -->

---

> [!question]
> What does the main** building block** of **MobileNetv2 **look like:

> [!answer]-
> The linear bottleneck with inverted residuals block:
> ![[ResidualBlock.png]]
>
> For example:
>
> ![[ExpandProject.png]]

> [!explanation]-
> "The **manifold of interest should lie in a low-dimensional subspace** of the higher-dimensional activation space"

<!-- guid: r5mhU|HL}4 -->
