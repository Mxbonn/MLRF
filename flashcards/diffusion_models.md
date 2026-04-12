---
paper_title: "Denoising Diffusion Probabilistic Models"
paper_url: https://arxiv.org/abs/2006.11239
---

> [!question]
> Give the **forward diffusion process**.

> [!answer]-
> Given a data point sampled from a real data distribution $\mathbf{x}_0 \sim q(\mathbf{x})$, let us **define a forward diffusion process in which we add small amounts of Gaussian noise to the sample** in $T$ steps, producing a sequence of noisy samples $\mathbf{x}_1, \dots, \mathbf{x}_T$. The step sizes are controlled by a variance schedule $\{\beta_t \in (0, 1)\}_{t=1}^T$
> $$q(\mathbf{x}_t \vert \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t\mathbf{I})$$
> $$q(\mathbf{x}_{1:T} \vert \mathbf{x}_0) = \prod^T_{t=1} q(\mathbf{x}_t \vert \mathbf{x}_{t-1})$$
> As $T \to \infty$, $\mathbf{x}_T$ becomes equivalent to an isotropic Gaussian distribution.
> ![[forward-diffusion.png]]
> *Forward diffusion process. Image modified by [Ho et al. 2020](https://arxiv.org/abs/2006.11239)*

<!-- guid: xxq%EPv[kq -->

---

> [!question]
> **Why is the mean of the forward diffusion model scaled by $\sqrt{1 - \beta_t}$**, where $\beta_t$ is the variance to $\mathbf{x}_t$?
> $$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = N(\mathbf{x}_t;\sqrt{1-\beta_t}\mathbf{x}_{t-1},\beta_t\mathbf{I})$$

> [!answer]-
> **The scaling factor is needed to avoid making the variance of $\mathbf{x}_t$ grow in each step.**
> If we would not scale it, after $T$ steps we will have a value $\mathbf{x}_t \in [-T,T]$.
> To force $\mathrm{Var}(x_1) = 1$ we need to scale by $\sqrt{1 - \beta_t}$.

<!-- guid: v6k1^b/WS8 -->

---

> [!question]
> In the **forward diffusion process, how can we go from $\mathbf{x}_0$ to $\mathbf{x}_T$ in a single step** ?
> Recall that $q(\mathbf{x}_t \vert \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t\mathbf{I}) \quad
> q(\mathbf{x}_{1:T} \vert \mathbf{x}_0) = \prod^T_{t=1} q(\mathbf{x}_t \vert \mathbf{x}_{t-1})$

> [!answer]-
> Using the reparameterization trick that tells us: $$\mathbf{z} \sim \mathcal{N}(\mathbf{z}; \boldsymbol{\mu}, \boldsymbol{\sigma^2}\boldsymbol{I})$$ and $$\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}$$ (where $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \boldsymbol{I})$, Reparameterization trick).
>
> If we define $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{i=1}^t \alpha_i$, then by recursively applying this trick:
>
> $$\mathbf{x}_t = \sqrt{\alpha_t}\mathbf{x}_{t-1} + \sqrt{1 - \alpha_t}\boldsymbol{\epsilon}_{t-1}$$
> $$= \sqrt{\alpha_t \alpha_{t-1}} \mathbf{x}_{t-2} + \sqrt{1 - \alpha_t \alpha_{t-1}} \bar{\boldsymbol{\epsilon}}_{t-2}$$
> $$= \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon}$$
>
> Therefore: $$q(\mathbf{x}_t \vert \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1 - \bar{\alpha}_t)\mathbf{I})$$
>
> *Note: When merging two Gaussians $\mathcal{N}(\mathbf{0}, \sigma_1^2\mathbf{I})$ and $\mathcal{N}(\mathbf{0}, \sigma_2^2\mathbf{I})$, the result is $\mathcal{N}(\mathbf{0}, (\sigma_1^2 + \sigma_2^2)\mathbf{I})$. Thus $\sqrt{(1 - \alpha_t) + \alpha_t (1-\alpha_{t-1})} = \sqrt{1 - \alpha_t\alpha_{t-1}}$.*

<!-- guid: nI>B98FD3] -->

---

> [!question]
> Draw the diffusion process.

> [!answer]-
> ![[DDPM.png]]

> [!explanation]-
> source: [https://lilianweng.github.io/posts/2021-07-11-diffusion-models/](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)

<!-- guid: DK)A;8~,+R -->

---

> [!question]
> Give the **simplified objective funtion** (**loss**) for **diffusion** models.

> [!answer]-
> $$L_\text{simple} = L_t^\text{simple} + C$$
> where $C$ is a constant not depending on $\theta$.
>
> The time-dependent loss is:
> $$L_t^\text{simple} = \mathbb{E}_{t \sim [1, T], \mathbf{x}_0, \boldsymbol{\epsilon}_t} \Big[\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2 \Big]$$
>
> Substituting $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon}_t$:
> $$L_t^\text{simple} = \mathbb{E}_{t \sim [1, T], \mathbf{x}_0, \boldsymbol{\epsilon}_t} \Big[\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon}_t, t)\|^2 \Big]$$

<!-- guid: J_C[@Wze1^ -->

---

> [!question]
> Give the **training algorithm** for Denoising **Diffusion** Probabilistic Models.

> [!answer]-
> repeat until convergence:
>     $\mathbf{x}_0 \sim q(\mathbf{x}_0)$
>     $t \sim \operatorname{Uniform}(\{1, \dots,T\})$
>     $\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$
>     Take gradient descent step on $\nabla_\theta \|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon},t)\|^2$

<!-- guid: B`zj&F[CED -->

---

> [!question]
> Give the **inference algorithm** for Denoising **Diffusion** Probabilistic Models.

> [!answer]-
> $\mathbf{x}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$
> for $t = T, \dots, 1$ do:
>     $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ if $t > 1$, else $\mathbf{z} = \mathbf{0}$
>     $\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}}(\mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)) + \sigma_t \mathbf{z}$
> return $\mathbf{x}_0$

<!-- guid: BB3V,(|H%4 -->
