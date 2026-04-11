---
paper_title: "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications"
paper_url: https://arxiv.org/abs/1704.04861
---

> [!question]
> What is the computational cost of a standard convolution with input $h_i \times w_i \times d_i$, output $h_i \times w_i \times d_j$ and kernel size $k$?

> [!answer]-
> $h_i \times w_i \times d_i \times d_j \times k \times k$

<!-- guid: si7^W!/<> -->

---

> [!question]
> What is the <u>computational cost</u> of a **depthwise separabale convolution** with input $h_i \times w_i \times d_i$, output $h_i \times w_i \times d_j$ and kernel size $k$?

> [!answer]-
> $h_i \cdot w_i \cdot d_i (k^2 + d_j) $

<!-- guid: lQ_1X1b,qX -->

---

> [!question]
> How much** reduction in computation** do you get by replacing standard convolutions with depthwise separable convolutions?

> [!answer]-
> **Computational cost standard convolution**:
>
> $h_i \times w_i \times d_i \times d_j \times k \times k$
>
> **Computational cost depthwise separable convolution**:
> $h_i \cdot w_i \cdot d_i (k^2 + d_j) $
>
> with input $h_i \times w_i \times d_i$, output $h_i \times w_i \times d_j$ and kernel size $k$
>
> **Reduction:**
>
> $= \frac{h_i \cdot w_i \cdot d_i (k^2 + d_j)}{h_i \times w_i \times d_i \times d_j \times k \times k}$
>
> **$= \frac{1}{d_j} + \frac{1}{k^2}$**

> [!explanation]-
> MobileNet uses $3 \times 3$ depthwise separable convolutions which uses between 8 to 9 times less computation than standard convolutions.

<!-- guid: u<LF`Q^|:w -->

---

> [!question]
> With what does **MobileNet replace the standard convolutional layer** with batchnorm and ReLU?
> ![[paste-30e8601affa2d6483ff09e78c38f234cdfcdaaee.jpg]]

> [!answer]-
> With a **Depthwise Separable convolutions** with Depthwise and Pointwise layers followed by batchnorm and ReLU.
> ![[paste-5e4779b76090a08c9ae193dbb7b515d911d52821.jpg]]

<!-- guid: MxBi+I#@1k -->

---

> [!question]
> Which two **additional hyperparameters** are introduced in **MobileNet **to construct scaled versions of the standard architecture?

> [!answer]-
> **<u>Width multiplier:</u>**
> The role of the **width multiplier $\alpha$** is to **thin a network uniformly at each layer**. For a given layer and width multiplier $\alpha$, the number of input channels $d_i$ becomes $\alpha d_i$ and the number of output channels $d_j$ becomes $\alpha d_j$.
>
> Width multiplier has the effect of **reducing computational cost** and the number of parameters quadratically **by roughly $\alpha^2$**.
>
> **<u>Resolution multiplier:</u>**
>
> The resolution multiplier $\rho$ is applied to the input image and the internal representation of every layer is subsequently reduced by the same multiplier. *In practice we implicitly set $\rho$ by setting the input resolution.*
>
> Resolution multiplier has the effect of **reducing computational cost by $\rho^2$**.*
> *

<!-- guid: s3!P5k8M-c -->

---

> [!question]
> How many multiply-adds and parameters does the default **MobileNetV1 **have? And how much accuracy does it get on ImageNet?

> [!answer]-
> **569M MAdds** and **4.2M parameters** with an accuracy of **70.6%** on ImageNet.

<!-- guid: b3}B]ZIL=D -->
