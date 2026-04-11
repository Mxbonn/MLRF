---
paper_title: "Playing Atari with Deep Reinforcement Learning"
paper_url: https://arxiv.org/abs/1312.5602
---

> [!question]
> Give the pseudocode for **Deep Q-learning with Experience Replay**.

> [!answer]-
> Initialize replay memory $D$ to capacity $N$
>
> Initialize action-value function $Q$ with random weights $\theta$
> for episode = 1, $M$ do
>     Initialize sequence $s_1 = \{x_1\}$ and preprocessed sequence  $\phi_1 = \phi(s_1)$
>     for $t = 1, T$ do
>         With probability $\epsilon$ select a random action $a_t$
>         Otherwise select $a_t = \operatorname{argmax}_a \hat{Q}(\phi(s_t),a;\theta)$
>         Execute action $a_t$ in emulator and observe reward $r_t$ and image $x_{t+1}$
>         Set $s_{t+1} = s_t, a_t, x_{t+1}$ and preprocess $\phi_{t+1}=\phi(s_{t+1})$
>         Store transition $(\phi_t, a_t, r_t, \phi_{t+1})$ in $D$
>         Sample random minibatch of transitions $(\phi_j, a_j, r_j, \phi_{j+1})$ from $D$
>         set $y_j = \begin{cases} r_j &amp; \text{if episode terminates at step } j+1 \\ r_j + \gamma \operatorname{max}_{a'} Q (\phi_{j+1},a'; \theta) &amp; \text{otherwise}\end{cases}$
>         Perform a gradient descent step on $(y_j - Q(\phi_j, a_j;\theta))^2$ with respect to the network parameters $\theta$
>         Every $C$ steps reset $\hat{Q} = Q $
>     End for
> End for

<!-- guid: qC!w~g2u.3 -->

---

> [!question]
> Why do we create **a replay memory in Deep Q-learning**?

> [!answer]-
> Experience replay in Deep Q-Learning has two functions:
> 1. **Make more efficient use of the experiences during training**. Usually, in online RL, the agent interacts in the environment, gets the experiences (state, action, reward, and next state), learns from them (updates the neural network), and discards them. This is not efficient.
>
> Experience replay helps **using the experiences of the training more efficiently**. We use a replay buffer that saves experience samples **that we can reuse during the training**.
> This allows the agent to **learn from the same experiences multiple times**.
>
> 2. **Avoid forgetting previous experiences and reduce the correlation between experiences.**
> Experience replay also has other benefits. By randomly sampling the experiences, we remove correlation in the observation sequences and avoid **action values from oscillating or diverging catastrophically**.

> [!explanation]-
> See also: https://huggingface.co/deep-rl-course/unit3/deep-q-algorithm

<!-- guid: Pld07Hd/xA -->
