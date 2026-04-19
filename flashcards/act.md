---
paper_title: "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware"
paper_url: https://arxiv.org/abs/2304.13705
---

> [!question]
> Draw and describe the **ACT** (Action Chunking with Transformers) architecture.

> [!answer]-
> ![[act_architecture.png]]
> ACT is a **Conditional VAE (CVAE)** with two transformer-based halves:
> 1. **CVAE encoder** (training only, left): a BERT-like transformer encoder takes a learned **[CLS]** token, the current **joint positions**, and the **target action sequence** $a_{t:t+k}$ from the demonstration. The output at `[CLS]` predicts the mean and variance of the **style variable** $z$ (diagonal Gaussian).
> 2. **CVAE decoder / policy** (right): a transformer encoder–decoder takes **4 RGB images** (processed by per-camera **ResNet** encoders with 2D sinusoidal position embeddings), the **current joint positions**, and **$z$**, and predicts the next **$k$ target joint positions** for both arms.
>
> At test time the CVAE encoder is discarded and $z$ is set to the mean of the prior (**zero**), making the policy deterministic.


> [!explanation]-
> More detailed diagram:
> ![[act_architecture_detailed.png]]


---

> [!question]
> What are the **inputs** and **outputs** of **ACT** at inference time?

> [!answer]-
> **Inputs:**
> - **4 RGB images** at 480×640 from commodity webcams.
> - **Current joint positions** of the two follower robots (**7 + 7 = 14 DoF**).
>
> **Output:**
> - A **$k \times 14$** tensor of **absolute target joint positions** for the next $k$ timesteps (both arms).
>
> Targets are then tracked by the low-level, high-frequency **PID controllers** inside the Dynamixel motors.


---

> [!question]
> What is **action chunking** in ACT, and why does it help?

> [!answer]-
> Instead of predicting a single action per step, the policy models
> $$\pi_\theta(a_{t:t+k} \mid s_t)$$
> i.e. a **sequence of $k$ future actions** from one observation. Every $k$ steps the agent observes, generates $k$ actions, and executes them open-loop.
>
> **Why it helps:** it reduces the **effective horizon** of the task by a factor of $k$, which mitigates the **compounding-error** problem in behavioral cloning (small per-step errors drift the state off the training distribution). Empirically, success climbs from **1% at $k=1$ to 44% at $k=100$** before slightly tapering.


---

> [!question]
> What is **temporal ensembling** in ACT, and how are overlapping chunks combined?

> [!answer]-
> ![[act_chunking.png]]
> To avoid jerky switches between "observe" and "execute" phases, the policy is **queried at every timestep**, producing overlapping chunks that all propose an action for time $t$.
>
> These are combined with a weighted average:
> $$w_i = \exp(-m \cdot i)$$
> where $w_0$ is the weight of the **oldest** proposed action and $m$ controls how fast newer predictions dominate. This smooths trajectories without slowing the control loop and requires **no extra training**.


---

> [!question]
> Why is ACT trained as a **CVAE** rather than a plain regression to actions?

> [!answer]-
> **The problem** — human demonstrations are **multi-modal**: for the same observation $s_t$, a teleoperator may validly choose different action sequences on different takes (e.g. approach a cup from the left *or* from the right). A deterministic regressor trained with MSE/L1 on all these takes averages them and outputs the **mean** of the valid options, which often is not itself valid (averaging "go left" and "go right" → "go straight through the cup"). This is known as **mode averaging / mode collapse**.
>
> **What a CVAE is** — a conditional variational autoencoder models $p(a \mid s)$ as $\int p(a \mid s, z)\, p(z)\, dz$, where $z$ is a **latent "style" variable** drawn from a simple prior (unit Gaussian). Intuition: $z$ picks *which mode* you're in (e.g. "left-approach style") and the decoder $p(a \mid s, z)$ produces the sequence consistent with that style. Because different takes get different $z$'s, the decoder never has to blend them.
>
> Training uses a standard VAE-style ELBO:
> - an **encoder** $q_\phi(z \mid s, a)$ infers which $z$ produced the observed demonstration,
> - a **decoder** $p_\theta(a \mid s, z)$ reconstructs the action sequence,
> - loss = **reconstruction** (L1 on actions) + **KL** pulling $q_\phi$ toward the prior so $z$ stays well-behaved.
>
> **At test time** the encoder is thrown away and $z$ is set to the **prior mean (zero)**, giving one deterministic trajectory — you don't need to pick a style yourself.
>
> **Why it matters here** — ablation: on **scripted (deterministic) data**, removing the CVAE objective barely changes performance because there's only one mode. On **human data**, success drops from **35.3% → 2%**, showing the CVAE objective is essential whenever demonstrations contain genuine human variability.


---

> [!question]
> How is the **style variable $z$** used at **train** vs **test** time in ACT?

> [!answer]-
> **Training:** the CVAE encoder sees the current joint positions and the **target action sequence** (but *not* the images, for speed) and outputs a diagonal-Gaussian $q_\phi(z \mid \text{obs}, a_{t:t+k})$. $z$ is sampled via the **reparameterization trick** and fed to the decoder. Loss = **L1 reconstruction** on actions + **KL** to a unit-Gaussian prior.
>
> **Test:** the encoder is **discarded**. $z$ is set to the **mean of the prior (zero vector)**, so given an observation the policy output is **deterministic**, which is useful for reproducible evaluation.


---

> [!question]
> ACT makes several non-obvious design choices around actions and loss. What are they, and why?

> [!answer]-
> - **Leader joint positions as actions** (not follower): the **force** applied is implicitly encoded in the *difference* between leader and follower joints via the low-level PID controller. Using follower joints would lose this information.
> - **Absolute target joint positions** (not deltas): delta-action parameterization **degrades performance**.
> - **L1 reconstruction loss** (not L2): L1 yields **more precise** modeling of the action sequence — important for fine manipulation.
> - **50 Hz control rate**: dropping to 5 Hz (typical of prior deep-imitation work) harms performance on precise tasks.


---

> [!question]
> What are ACT's **model size**, **training cost**, and **inference latency**?

> [!answer]-
> - **~80M parameters**, trained **from scratch per task**.
> - **~5 hours** of training on a single **11 GB RTX 2080 Ti**.
> - **~0.01 s** per forward pass at inference, which comfortably supports the **50 Hz** control loop (especially combined with action chunking so a single forward pass yields $k$ actions).
> - Data budget: **50 demos per task** (100 for Thread Velcro) ≈ **10–20 min** of demonstration data per task.

