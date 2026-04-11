---
paper_title: "Deep Reinforcement Learning with Double Q-learning"
paper_url: https://arxiv.org/abs/1509.06461v3
---

> [!question]
> What is **Double DQN** and why is it used?

> [!answer]-
> To understand this problem, remember how we calculate the TD Target:
> $$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha [ R_{t+1} + \gamma \operatorname{max}_{a'} Q(S_{t+1}, a') - Q(S_t, A_t)]$$**The max operator uses the same values both to select and to evaluate an actions. This makes is likely to select overestimated values, resuling in overoptimistic value estimates.**
> The solution to prevent this is: when we compute the Q target, we use two networks to decouple the action selection from the target Q-value generation. We:
>
> - Use our **DQN network** to select the best action to take for the next state (the action with the highest Q-value).
> - Use our** Target network** to calculate the target Q-value of taking that action at the next state.
>
> $$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha [ R_{t+1} + \gamma Q(S_{t+1}, \operatorname{argmax}_{a'} Q(S_{t+1}, a';\theta);\theta^-) - Q(S_t, A_t)]$$
>
> Therefore, Double DQN helps us reduce the overestimation of Q-values and, as a consequence, helps us train faster and have more stable learning.

> [!explanation]-
> The idea behind Double-Q learning (before DQN) is introduced in [Double Q-learning
> ](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html)

<!-- guid: PXD:;`3Zz7 -->
