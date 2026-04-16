---
paper_title: "PaLM-E: An Embodied Multimodal Language Model"
paper_url: https://arxiv.org/abs/2303.03378
---

> [!question]
> Give a high-level overview of **PaLM-E**.

> [!answer]-
> ![[palm-e.png]]
> PaLM-E is an **embodied multimodal language model**: a pretrained decoder-only LLM (PaLM) extended so that continuous sensor observations (images, state vectors, 3D scene tokens) are **injected directly into the language embedding space**, letting the same model do VQA, captioning, and embodied planning.
>
> The inputs are **multi-modal sentences** that interleave text with observation embeddings, and the outputs are **autoregressive text completions** — when used for control, those completions are **high-level subgoals** executed by separate low-level policies.
>
> The largest variant (**PaLM-E-562B**) combines PaLM-540B with a **22B ViT**, making it the largest reported vision-language model at the time.

---

> [!question]
> How does **PaLM-E** inject continuous observations into a pretrained LLM?

> [!answer]-
> An encoder $\phi : \mathcal{O} \to \mathcal{X}^q$ maps each observation in observation space $\mathcal{O}$ into a sequence of $q$ vectors in the LLM's **language embedding space** $\mathcal{X}$. These observation embeddings are **interleaved with regular word-token embeddings** to form a multi-modal sentence, which is then fed to the decoder-only LLM exactly like a normal token sequence.
>
> Crucially, the observation embeddings are **placed dynamically within the surrounding text** (e.g. `Q: What happened between <img 1> and <img 2>?`) rather than at fixed positions, so the same model can handle an arbitrary number and ordering of observations per prompt.

[!explanation] contrast with VLMs like PaLI that prepend a fixed image prefix

---

> [!question]
> What are the **inputs** and **outputs** of **PaLM-E**?

> [!answer]-
> **Input:** a multi-modal sentence consisting of text tokens interleaved with one or more **continuous observations** (images, state vectors, or 3D scene representations), each encoded into the LLM's embedding space.
>
> **Output:** text generated **autoregressively** by the decoder-only LLM. Depending on the task this text is:
> - an **answer** (VQA, captioning), or
> - a **high-level plan / subgoal** that a separate low-level policy translates into robot actions.
>
> PaLM-E itself never emits low-level actions — it acts as a **high-level policy that sequences low-level skills** from a vocabulary the model infers from the training data and prompt.

---

> [!question]
> Which **input / scene representations** does **PaLM-E** explore for encoding observations into the language embedding space?

> [!answer]-
> Three encoders, each mapping into $\mathcal{X}$:
>
> 1. **State vectors**: an MLP $\phi_{\text{state}}$ maps a scene-state vector $s \in \mathbb{R}^S$ (object poses, sizes, colors, …) into one embedding.
> 2. **Vision Transformer (ViT)**: $\phi_{\text{ViT}}(I)$ produces per-patch embeddings in dimension $\tilde{k}$. Since $\tilde{k}$ generally differs from the LLM dim $k$, each embedding is projected through a **learned affine transformation** $\psi$: $x_i = \psi(\phi_{\text{ViT}}(I)_i)$.
> 3. **Object Scene Representation Transformer (OSRT)**: a **3D-aware** neural scene representation that learns object-centric slot embeddings via a novel-view synthesis task, producing $m$ embeddings per scene.
>

---

> [!question]
> What is the role of the **learned affine projection $\psi$** in PaLM-E's ViT encoder?

> [!answer]-
> The ViT outputs per-patch embeddings with dimensionality $\tilde{k}$, which is **not necessarily equal** to the LLM's embedding dimension $k$. A learned **affine transformation** $\psi : \mathbb{R}^{\tilde{k}} \to \mathbb{R}^{k}$ projects each patch embedding into the language embedding space so it can be concatenated with word-token embeddings:
> $$x_i = \psi\big(\phi_{\text{ViT}}(I)_i\big).$$


---

> [!question]
> How does **PaLM-E** build **object-centric** visual encodings on top of a ViT?

> [!answer]-
> Given **ground-truth object instance masks** $M_j$, PaLM-E decomposes the ViT representation **per object** by masking the input image before encoding:
> $$x^j_{1:m} = \psi\big(\phi_{\text{ViT}}(M_j \circ I)\big),$$
> producing a separate set of embeddings for each object $j$, which are then interleaved into the prompt.
>
> This **structured encoder** isolates objects into distinct multimodal tokens, making it easier for the LLM to bind words (e.g. referring expressions) to the right visual entity.

---

> [!question]
> Why does **PaLM-E** use **OSRT** as a scene encoder, and what advantage does it have over a plain ViT?

> [!answer]-
> OSRT (Object Scene Representation Transformer) learns **3D-centric, object-slot** neural scene representations **in-domain** via a **novel-view synthesis** objective. No ground-truth masks or segmentation labels are needed.
>
> In PaLM-E's TAMP experiments, OSRT outperforms ViT-based encodings when the number of objects in the scene **exceeds what was seen during training** (i.e. better compositional generalisation), showing the value of **3D-aware, object-factored** representations for embodied reasoning. Plain ViT features flatten the scene into patches and lose this structure.

---

> [!question]
> How is **PaLM-E** actually used in a **robot control loop**?

> [!answer]-
> PaLM-E is a **high-level policy**, not a motor controller:
>
> 1. Given the current image and a long-horizon goal (e.g. *"sort the blocks by colors into corners"*), PaLM-E emits a **language subgoal at ~1 Hz**.
> 2. A separate **low-level policy** (e.g. Lynch et al. 2022, RT-1) consumes that subgoal and outputs **low-level robot actions at ~5 Hz**.
> 3. The subgoal must be drawn from a **vocabulary of low-level skills**; PaLM-E infers the available skills from the training data and prompt — no external filter constrains its output.
>
> Because PaLM-E closes the loop by re-observing the scene and conditioning on its own previous text, it can **replan** and leverage the world knowledge stored in the LLM's weights.

> [!explanation]-
> A typical control prompt looks like: `Human: <instruction> Robot: <step history>. I see <img>.`

---

> [!question]
> How does **PaLM-E**'s multimodal injection differ from earlier VLMs like **PaLI** or **Gato**?

> [!answer]-
> - **vs. PaLI-style VLMs**: PaLI inserts a **fixed image prefix** before the text tokens. PaLM-E instead **dynamically interleaves** observation embeddings anywhere within the text, so a prompt can contain multiple images, state vectors, and object-level tokens in any order.
> - **vs. Gato**: Gato **tokenises everything (including actions) into a discrete vocabulary**, whereas PaLM-E **keeps observations as continuous embeddings** injected into an existing LLM's space and outputs **text-level plans** rather than low-level action tokens.
>
> The upshot: PaLM-E reuses a frozen or lightly-tuned LLM's world knowledge, instead of training a multimodal transformer from scratch.

---

> [!question]
> What are the smallest and largest variants of **PaLM-E**?

> [!answer]-
> - **PaLM-E-62B**: 8B and 562B