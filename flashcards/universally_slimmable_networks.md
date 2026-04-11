---
paper_title: "Universally Slimmable Networks and Improved Training Techniques"
paper_url: https://arxiv.org/abs/1903.05134
---

> [!question]
> What is the main **difference **between the original slimmable networks paper and the **universally slimmable networks** paper?

> [!answer]-
> The originally slimmable networks could only be slimmed to predefined widths (e.g. [0.25, 0.5, 0.75, 1.0]), the universally slimmable networks (US-Nets)** extend this to networks of arbitrary width**.

> [!explanation]-
> ![[paste-fbc9e5d9a20d571719f5aac761c3ce8c8ae820a6.jpg]]

<!-- guid: g<%,dt5NO4 -->

---

> [!question]
> One the main issues and reason to work with predefined widths in Slimmable Networks was batch normalization, how is that solved in Universally Slimmable networks?

> [!answer]-
> The batch normalization only caused issues during testing. In universally trainable networks they argue that you can just compute the batch norm statistics of an arbitrary width with a large minibatch before you start using it.

<!-- guid: H%(Et&$@p- -->

---

> [!question]
> What are the main new techniques in Universally Slimmable networks?

> [!answer]-
> **The sandwich rule:**
> Instead of running the model at fixed widths as in Slimmable Networks they randomly sample $n-2$ widths in the range $[0.25, 1.0] \times$ and train the model with these widths along with the smallest and largest width.
>
> **Inplace distillation:**
>
> For the largest model the ground truth is used as labels but for all other models the predicted labels of this largest model is used as training label.

<!-- guid: s4/eG=IKsc -->
