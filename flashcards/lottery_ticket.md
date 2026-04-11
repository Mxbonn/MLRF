---
paper_title: "The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks"
paper_url: https://arxiv.org/abs/1803.03635
---

> [!question]
> What is **The Lottery Ticket Hypothesis**?

> [!answer]-
> A randomly-initialized, dense neural network contains a subnetwork that is initialized such that - when trained in isolation - it can match the test accuracy of the original network after training for at most the same number of iterations.

> [!explanation]-
> More formally, consider a dense feed-forward neural network $f(x; \theta)$ with initial parameters $\theta = \theta_0 ∼ \mathcal{D}_0$. When optimizing with stochastic gradient descent (SGD) on a training set, $f$ reaches minimum validation loss $l$ at iteration $j$ with test accuracy $a$ . In addition, consider training $f(x;m\bigodot\theta)$ with a mask $m \in {0, 1}^{|\theta|}$ on its parameters such that its initialization is $m \bigodot \theta_0$. When optimizing with SGD on the same training set (with $m$ fixed), $f$ reaches minimum validation loss $l'$ at iteration $j'$ with test accuracy $a'$. The lottery ticket hypothesis predicts that $\exists m $ for which $j' \le j$ (commensurate training time), $a' \ge a$ (commensurate accuracy), and $||m|| \ll |\theta|$ (fewer parameters).

<!-- guid: OMqjUp6Xq8 -->

---

> [!question]
> What does the **Lottery Ticket Hypothesis** say about the initialization of the *winning tickets*?

> [!answer]-
> When the parameters of the *winning tickets* are <u>randomly reinitialized</u> $(f(x;m\bigodot\theta'_0)$, these *winning tickets* **no longer match the performance of the original network**, offering evidence that these smaller networks do not train effectively unless they are appropriately initialized.

> [!explanation]-
> This means that the network structure alone cannot explain the winning ticket's success.
> (However at moderate pruning levels and in conv-nets, the structure alone may be sufficient)

<!-- guid: Nlq3^%1eiC -->

---

> [!question]
> How is the **pruning** done in the **Lottery Ticket Hypothesis paper**?

> [!answer]-
> **Iterative** pruning with resetting the remaining parameters to their initial values (so also retraining from scratch after every pruning step).

<!-- guid: eke9XXq_VX -->

---

> [!question]
> What is the **importance of the winning ticket initialization**?

> [!answer]-
> **When randomly reinitialized, a winning ticket learns more slowly and achieves lower test accuracy**, suggesting that initialization is important to its success.
>
> Experiments have shown that the winning ticket weights move further than other weights. This suggests that **the benefit of the initialization is connected to the optimization algorithm, dataset, and model. **For example, the winning ticket initialization might land in a region of the loss landscape that is particularly amenable to optimization by the chosen optimization algorithm.

> [!explanation]-
> The authors hypothesize that up to a certain level of sparsity - highly overparameterized networks can be pruned, reinitialized, and retrained successfully; however, beyond this point, extremely pruned, less severely overparamterized networks only maintain accuracy with fortuitous initialization.

<!-- guid: u0)t(9J(F9 -->

---

> [!question]
> What were some important limitations of the **Lottery Ticket Hypothesis** paper?

> [!answer]-
> They only considered vision-centric classification tasks on smaller datasets (MNIST, CIFAR10). Iterative pruning is computationally intensive, requiring training a network 15 or more times consecutively for multiple trials. This pruning flow is also the only method to find winning tickets.

<!-- guid: kC)FlP8JZ& -->
