---
paper_title: "Extracting and Composing Robust Features with Denoising&nbsp;Autoencoders"
paper_url: http://www.cs.toronto.edu/~larocheh/publications/icml-2008-denoising-autoencoders.pdf
---

> [!question]
> What is a **Denoising Autoencoder**?

> [!answer]-
> The **Denoising Autoencoder** is a modification to the basic autoencoder.
> The denoising autoencoder partially corrupts the initial input vector $\mathbf{x}$ in a stochastic manner:
> $$\tilde{\mathbf{x}}^{(i)} \sim \mathcal{M}_\mathcal{D}(\tilde{\mathbf{x}}^{(i)} \vert \mathbf{x}^{(i)})$$
> The model is then trained to recover the original input by minimizing:
> $$L_\text{DAE}(\theta, \phi) = \frac{1}{n} \sum_{i=1}^n (\mathbf{x}^{(i)} - f_\theta(g_\phi(\tilde{\mathbf{x}}^{(i)})))^2$$
> where $\mathcal{M}_\mathcal{D}$ defines the mapping from the true data samples to the noisy or corrupted ones.

> [!explanation]-
> ![[denoising-autoencoder-architecture.png]]
> Source: https://lilianweng.github.io/posts/2018-08-12-vae

<!-- guid: foO=T/>kAD -->
