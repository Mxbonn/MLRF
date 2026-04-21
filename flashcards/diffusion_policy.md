---
paper_title: "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"
paper_url: https://arxiv.org/abs/2303.04137
---

> [!question]
> Draw and describe the **Diffusion Policy** architecture, and explain the **observation ($T_o$)**, **prediction ($T_p$)** and **action ($T_a$)** horizons.

> [!answer]-
> ![[dp_policy_input_output.png]]
> At environment time step $t$ the policy:
> 1. Takes the last $T_o$ steps of observation, $\mathbf{O}_t$ (images + robot pose).
> 2. Starts from a pure-noise action sequence $\mathbf{A}_t^K \sim \mathcal{N}(\mathbf{0},\mathbf{I})$ of length $T_p$.
> 3. Runs $K$ **denoising iterations** with noise-prediction network $\boldsymbol{\epsilon}_\theta(\mathbf{O}_t,\mathbf{A}_t^k,k)$, producing $\mathbf{A}_t^0$, the predicted **$T_p$-step action sequence**.
> 4. Executes only the first $T_a$ steps of $\mathbf{A}_t^0$ open-loop, then re-plans (**receding-horizon control**).
>
> **Notation convention:** superscript $k \in \{K,\dots,0\}$ indexes the **diffusion iteration** (since subscript $t$ is already taken by env time). Typical values: $T_o{=}2$, $T_p{=}16$, $T_a{=}8$, $K{=}100$ training / $10$ inference via DDIM.

---

> [!question]
> Write the **conditional denoising update** used at inference in Diffusion Policy and explain every symbol.

> [!answer]-
> $$\mathbf{A}_t^{k-1} = \alpha\Big(\mathbf{A}_t^k - \gamma\,\boldsymbol{\epsilon}_\theta(\mathbf{O}_t,\mathbf{A}_t^k,k) + \mathcal{N}\bigl(\mathbf{0},\sigma^2 \mathbf{I}\bigr)\Big)$$
>
> Starting from $\mathbf{A}_t^K \sim \mathcal{N}(\mathbf{0},\mathbf{I})$, this runs for $k = K, K{-}1, \dots, 1$ to produce the clean action sequence $\mathbf{A}_t^0$.
>
> - $\mathbf{A}_t^k$ : action sequence of length $T_p$ at diffusion iteration $k$ (noisy for large $k$, clean at $k{=}0$).
> - $\mathbf{O}_t$ : conditioning observation. It is **only fed in, never denoised**, so the vision encoder runs **once** per control step regardless of $K$.
> - $\boldsymbol{\epsilon}_\theta(\mathbf{O}_t,\mathbf{A}_t^k,k)$ : noise-prediction network; predicts the noise currently contaminating $\mathbf{A}_t^k$.
> - $\gamma$ : step size on the predicted noise (analogous to a learning rate; see gradient-descent card).
> - $\sigma$ : std of the Gaussian noise re-injected to keep the process stochastic (Langevin).
> - $\alpha$ : overall rescale, typically slightly $<1$ to improve stability ([Ho et al. 2020](https://arxiv.org/abs/2006.11239)).
>
> The triple $(\alpha,\gamma,\sigma)$ is a **function of $k$** and constitutes the **noise schedule** (DP uses the *square-cosine* schedule from iDDPM). It plays the role of learning-rate scheduling.

> [!explanation]-
> The standard DDPM update $\mathbf{x}_{t-1}=\tfrac{1}{\sqrt{\alpha_t}}\bigl(\mathbf{x}_t-\tfrac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(\mathbf{x}_t,t)\bigr)+\sigma_t\mathbf{z}$ is the same equation with $\alpha\!=\!1/\sqrt{\alpha_t}$ and $\gamma\!=\!(1-\alpha_t)/\sqrt{1-\bar{\alpha}_t}$ folded into the schedule.

---

> [!question]
> Give the **training loss** for Diffusion Policy, and explain how the noisy input $\mathbf{A}_t^0 + \boldsymbol{\epsilon}^k$ is constructed.

> [!answer]-
> $$\mathcal{L} = \mathrm{MSE}\Big(\boldsymbol{\epsilon}^k,\; \boldsymbol{\epsilon}_\theta(\mathbf{O}_t,\, \mathbf{A}_t^0 + \boldsymbol{\epsilon}^k,\, k)\Big)$$
>
> **Per training step:**
> 1. Sample $(\mathbf{O}_t, \mathbf{A}_t^0)$ from the demonstration dataset.
> 2. Sample a diffusion iteration $k \sim \operatorname{Uniform}\{1,\dots,K\}$.
> 3. Sample noise $\boldsymbol{\epsilon}^k \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ scaled by the schedule for step $k$.
> 4. Form the noisy action $\mathbf{A}_t^0 + \boldsymbol{\epsilon}^k$ and let $\boldsymbol{\epsilon}_\theta$ **predict the noise** that is added.
>
> **Why this works.** This is exactly the DDPM $\boldsymbol{\epsilon}$-matching loss applied to action sequences conditioned on $\mathbf{O}_t$. The paper's compact notation $\mathbf{A}_t^0 + \boldsymbol{\epsilon}^k$ is a shorthand: in the DDPM notation it would be written $\sqrt{\bar{\alpha}_k}\mathbf{A}_t^0 + \sqrt{1-\bar{\alpha}_k}\boldsymbol{\epsilon}$, where the variance of $\boldsymbol{\epsilon}^k$ is set by the schedule at step $k$. It has been shown that minimising this simple MSE also minimises the variational lower bound on $\mathrm{KL}\!\left[\,p_{\text{data}}\,\|\,p_\theta\right]$, so we get proper density modelling with a plain regression loss.
>
> Because $\mathbf{O}_t$ is only conditioning (never noised), gradients flow through it and the **vision encoder is trained end-to-end** with $\boldsymbol{\epsilon}_\theta$.

---

> [!question]
> Why can we interpret one step of the diffusion denoising update as **noisy gradient descent on an energy landscape**, and what does $\boldsymbol{\epsilon}_\theta$ represent in this view?

> [!answer]-
> Strip the bias/scale from the update:
> $$\mathbf{x}^{k-1} \;\approx\; \mathbf{x}^k - \gamma\,\boldsymbol{\epsilon}_\theta(\mathbf{x}^k,k) + \text{noise}$$
> Compare to gradient descent on some scalar energy $E(\mathbf{x})$:
> $$\mathbf{x}' = \mathbf{x} - \gamma\,\nabla E(\mathbf{x})$$
> So **$\boldsymbol{\epsilon}_\theta$ is effectively predicting the gradient field $\nabla E(\mathbf{x})$**, and one denoising iteration is one step of (noisy) gradient descent toward a local minimum of $E$.
>
> Running $K$ such steps with added Gaussian noise is **Stochastic Langevin Dynamics**; it samples from $p(\mathbf{x}) \propto e^{-E(\mathbf{x})}$ rather than greedily descending to a single point. Noise lets trajectories hop between basins, which is exactly what lets the policy express **multiple action modes** instead of collapsing to the mean of the demonstrations.
>
> ![[dp_DP_teaser.png]]
> *(c) Diffusion Policy denoises noise into actions by following a learned gradient field.*

---

> [!question]
> Why is **Diffusion Policy more stable to train than an Implicit Behavioral Cloning (IBC)**? Derive the key observation about the normalisation constant.

> [!answer]-
> **IBC represents the policy as an Energy-Based Model:**
> $$p_\theta(\mathbf{a}\mid\mathbf{o}) = \frac{e^{-E_\theta(\mathbf{o},\mathbf{a})}}{Z(\mathbf{o},\theta)}, \qquad Z(\mathbf{o},\theta)=\int e^{-E_\theta(\mathbf{o},\mathbf{a})}\,d\mathbf{a}$$
> $Z(\mathbf{o},\theta)$, the integral of $e^{-E}$ over the whole action space, is **intractable**. IBC estimates it with an InfoNCE-style loss using $N_{\text{neg}}$ negative action samples $\{\tilde{\mathbf{a}}^j\}$:
> $$\mathcal{L}_{\text{InfoNCE}} = -\log\frac{e^{-E_\theta(\mathbf{o},\mathbf{a})}}{e^{-E_\theta(\mathbf{o},\mathbf{a})}+\sum_{j=1}^{N_{\text{neg}}} e^{-E_\theta(\mathbf{o},\tilde{\mathbf{a}}^j)}}$$
> Poor negatives -> bad $Z$ estimate -> **training instability**. Empirically IBC's train MSE and eval success both oscillate.
>
> ![[dp_ibc_stability_figure.png]]
>
> **Diffusion Policy sidesteps $Z$ entirely** by modelling the **score function** $\nabla_{\mathbf{a}} \log p(\mathbf{a}\mid\mathbf{o})$ instead of $p$:
> $$\nabla_{\mathbf{a}}\log p(\mathbf{a}\mid\mathbf{o}) = -\nabla_{\mathbf{a}} E_\theta(\mathbf{a},\mathbf{o}) - \underbrace{\nabla_{\mathbf{a}} \log Z(\mathbf{o},\theta)}_{=\,0\ \text{since }Z\text{ doesn't depend on }\mathbf{a}} \;\approx\; -\boldsymbol{\epsilon}_\theta(\mathbf{a},\mathbf{o})$$
> The $\log Z$ term **vanishes** under $\nabla_{\mathbf{a}}$, it's a constant w.r.t. $\mathbf{a}$. So neither training (MSE on noise) nor inference (Langevin steps) ever touches $Z$, and training is stable.

---

> [!question]
> How does Diffusion Policy end up expressing **multimodal action distributions**, and where does the multimodality come from?

> [!answer]-
> Multimodality arises from **two stochastic sources** in the Langevin sampler:
>
> 1. **Stochastic initialisation**: each rollout starts from a fresh $\mathbf{A}_t^K \sim \mathcal{N}(\mathbf{0},\mathbf{I})$. Different initial points land in different convergence basins of the (implicit) energy $E$.
> 2. **Injected Gaussian noise per iteration**: the $\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I})$ term in the update lets samples **hop between basins** during the $K$ denoising steps rather than deterministically rolling into the nearest one.
>
> Because $\boldsymbol{\epsilon}_\theta$ learns a **gradient field** over the whole action space (not a single-mode parametric distribution like a Gaussian or GMM), Stochastic Langevin Dynamics can, in principle, sample any normalisable $p(\mathbf{A}_t\mid\mathbf{O}_t)$. Combined with action-sequence prediction, this also gives **temporal consistency**: the whole $T_p$-step chunk is sampled jointly from one mode, so consecutive actions don't alternate between "go left" and "go right".

> [!explanation]-
> ![[dp_multimodal_sim.png]]
> *Pushing the T-block into the target: either left or right around it is valid. Diffusion Policy commits cleanly to one mode per rollout; LSTM-GMM/IBC are biased, BET jitters between modes.*
>
---

> [!question]
> Compare the **CNN-based** and **Transformer-based** Diffusion Policy backbones: how is the observation injected, and when would you use each?

> [!answer]-
> ![[dp_policy_input_output.png]]
>
> **CNN-based (default):** a 1-D temporal U-Net over the action sequence. $\mathbf{O}_t$ and the diffusion step $k$ are injected via **FiLM** (Feature-wise Linear Modulation): per-channel affine $\mathbf{h} \leftarrow \boldsymbol{\gamma}(\mathbf{O}_t,k)\odot\mathbf{h} + \boldsymbol{\beta}(\mathbf{O}_t,k)$ applied at every conv layer. Works out-of-the-box on most tasks with little tuning. **Weakness:** temporal conv has a low-frequency inductive bias, so it over-smooths fast-changing actions (e.g. velocity control).
>
> **Transformer-based (time-series diffusion transformer):** noisy actions $\mathbf{A}_t^k$ are the input tokens of a minGPT-style decoder; a sinusoidal embedding of $k$ is prepended as the first token; an MLP-encoded $\mathbf{O}_t$ is fed via **cross-attention** in each decoder block; causal self-attention within actions. Output tokens predict $\boldsymbol{\epsilon}_\theta(\mathbf{O}_t,\mathbf{A}_t^k,k)$. Better on high-frequency / velocity-control tasks but **more hyperparameter-sensitive**.
>
> **Recommendation:** start with CNN; switch to the transformer only if the task has rapid, sharp action changes.

---

> [!question]
> What are the **key design decisions** that make Diffusion Policy practical on a real robot (action space, execution, inference speed)?

> [!answer]-
> - **Position control > velocity control.** Surprising, because most BC baselines use velocity. Reasons: (i) position actions are **more multimodal**. Diffusion Policy handles this well, baselines (GMM, k-means) don't; (ii) position control suffers less from **compounding error** over long action chunks.
>   ![[dp_pos_vs_vel_figure.png]]
> - **Receding-horizon action chunking.** Predict $T_p$ steps, execute only $T_a$, then replan. Balances temporal consistency (large $T_a$) vs. reactivity (small $T_a$). Ablation shows an interior sweet spot around $T_a{\approx}8$.
>   ![[dp_ablation_figure.png]]
> - **Visual conditioning, not joint modelling.** Model $p(\mathbf{A}_t\mid\mathbf{O}_t)$ instead of $p(\mathbf{A}_t,\mathbf{O}_t)$ (Diffuser-style). → the **vision encoder runs once** per control step regardless of $K$ denoising iterations; and it can be trained **end-to-end** with $\boldsymbol{\epsilon}_\theta$.
> - **End-to-end ResNet-18** with two tweaks: spatial-softmax pooling (preserves spatial info) and GroupNorm instead of BatchNorm (stable with EMA weights, which DDPMs use).
> - **DDIM for fast inference.** DDIM decouples training and inference iteration counts. DP uses **$K{=}100$ training, $10$ inference** → ~0.1 s per forward pass on a 3080, enough for real-time closed-loop control.
> - **Action normalisation to $[-1,1]$.** DDPMs clip predictions to $[-1,1]$ each step, so zero-mean/unit-variance normalisation would make part of action space unreachable.

---

> [!question]
> What is the **control-theory sanity check** for Diffusion Policy on a linear dynamical system with linear feedback demonstrations, and what does it reveal about the general case?

> [!answer]-
> Take an LTI plant with LQR demonstrations:
> $$\mathbf{s}_{t+1} = \mathbf{A}\mathbf{s}_t + \mathbf{B}\mathbf{a}_t + \mathbf{w}_t, \qquad \mathbf{a}_t = -\mathbf{K}\mathbf{s}_t$$
>
> **Single-step prediction ($T_p{=}1$).** The MSE-optimal denoiser for $\mathcal{L}=\mathrm{MSE}\bigl(\boldsymbol{\epsilon}^k,\;\boldsymbol{\epsilon}_\theta(\mathbf{s}_t,\,-\mathbf{K}\mathbf{s}_t+\boldsymbol{\epsilon}^k,\,k)\bigr)$ has closed form
> $$\boldsymbol{\epsilon}_\theta(\mathbf{s},\mathbf{a},k) = \tfrac{1}{\sigma_k}\bigl[\mathbf{a} + \mathbf{K}\mathbf{s}\bigr].$$
> Plug into the DDIM update → Langevin converges to the unique global minimum $\mathbf{a}=-\mathbf{K}\mathbf{s}$. ✓
>
> **Multi-step prediction ($T_p{>}1$).** The optimal denoiser gives $\mathbf{a}_{t+t'} = -\mathbf{K}(\mathbf{A}-\mathbf{B}\mathbf{K})^{t'}\mathbf{s}_t$, i.e. to predict future actions the policy **implicitly learns a (task-relevant) dynamics model** by unrolling the closed-loop system.
>
> **Takeaway.** Even in the simple LTI case, action-sequence prediction forces the network to encode dynamics; in the nonlinear case this becomes harder *and* inherently multimodal — which is exactly the regime where the diffusion formulation pays off.

> [!explanation]-
> **LTI = Linear Time-Invariant.** A dynamical system whose next state is a *linear* function of the current state and input, with matrices that **do not change over time**:
> $$\mathbf{s}_{t+1} = \mathbf{A}\mathbf{s}_t + \mathbf{B}\mathbf{a}_t + \mathbf{w}_t$$
> - $\mathbf{A}$ (state transition) and $\mathbf{B}$ (input matrix) are constant.
> - $\mathbf{w}_t \sim \mathcal{N}(\mathbf{0},\boldsymbol{\Sigma}_w)$ is process noise.
>
> **LQR = Linear Quadratic Regulator.** The **optimal controller** for an LTI system under a **quadratic** running cost
> $$J = \sum_t \bigl(\mathbf{s}_t^\top \mathbf{Q}\mathbf{s}_t + \mathbf{a}_t^\top \mathbf{R}\mathbf{a}_t\bigr)$$
> where $\mathbf{Q}\succeq 0$ penalises state error and $\mathbf{R}\succ 0$ penalises control effort. Minimising $J$ yields a **linear state-feedback** law
> $$\mathbf{a}_t = -\mathbf{K}\mathbf{s}_t$$
> with gain $\mathbf{K}$ obtained by solving the discrete-time **Riccati equation**.
>
> **Why the paper uses this setting.** LTI + LQR is the classic "textbook" controllable case: known linear dynamics + quadratic cost → closed-form optimal linear policy. Because the ground-truth policy is simple and known, the optimal denoiser $\boldsymbol{\epsilon}_\theta$ can be derived analytically, giving a clean sanity check that Diffusion Policy recovers the right controller in the limit.
