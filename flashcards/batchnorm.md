---
paper_title: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"
paper_url: https://arxiv.org/abs/1502.03167
---

> [!question]
> How does **Batch Normalization** work?

> [!answer]-
> **Batch Normalization** normalizes **each scalar feature independently**, by making it have **zero mean** and a **variance of 1**. The normalized values are then **scaled and shifted**.
> <u>During training</u>, the batchnorm layer works as follows:
>
> ---
>
> **Input:** Values of $x$ over a mini-batch: $\mathcal{B} = {x_{1...m}}$
> **Output:** $y_i = \operatorname{BatchNorm}_{\gamma, \beta}(x_i)$
> $$\mu_{\mathcal{B}} = \frac{1}{m} \sum^m_{i=1}x_i$$
> $$\sigma^2_{\mathcal{B}} = \frac{1}{m} \sum^m_{i=1}(x_i - \mu_{\mathcal{B}})^2$$
> $$\hat{x}_i = \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma^2_{\mathcal{B}} + \epsilon}} $$
> $$y_i = \gamma x_i + \beta$$
>
> ---
>
> With $\epsilon$ a constant added for numeric stability.
> And **$\gamma$ and $\beta$ learned parameters**.
> <u>During inference</u>, the normalization is done using the population rather than mini-batches.
> $$\hat{x}_i = \frac{x_i - \operatorname{E}[x_i]}{\sqrt{\operatorname{Var}[x_i] + \epsilon}} $$

<!-- guid: Mk%J-^b79. -->

---

> [!question]
> What is different for using **Batch Normalization** in **Convolutions** compared to **fully connected layers**?

> [!answer]-
> For convolutional layers, we additionally want the normalization to obey the **convolutional property** – so that different elements of the same feature map, at **different locations, are normalized in the same way**. To achieve this, we **jointly normalize all the activations in a minibatch, over all locations**.
> In other words, in convolutions **we normalize (and scale/shift) per feature map (channel), rather than per individual value**.

<!-- guid: m>D}7b&hT( -->

---

> [!question]
> Why **does Batch Normalization** have **learned scale and shift parameters**?

> [!answer]-
> The learned shift and scale parameters **$\gamma$** and **$\beta$** in 
> $$y_k = \gamma_k \hat{x}_k + \beta_k$$
> **enable the full represation power of the neural network.**

> [!explanation]-
> By setting $\gamma_k = \sqrt{\operatorname{Var}[x_k]}$ and $\beta_k = \operatorname{E}[x_k]$, we **could recover the original values**, if that were the optimal thing to do.

<!-- guid: E2Fv}l-i?e -->
