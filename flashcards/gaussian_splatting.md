---
paper_title: "3D Gaussian Splatting for Real-Time Radiance Field Rendering"
paper_url: https://arxiv.org/abs/2308.04079
---

> [!question]
> How are the **3D Gaussians parameterized** in *3D Gaussian Splatting*?

> [!answer]-
> The *anisotropic* 3D gaussians are modeled using a **scale vector $s \in \mathbb{R}^3$ and quaternions $q$**. 
> From this the scaling matrix $S$ and rotatation matrix $R$ can be constructed. 
> The typical parameterization of a guassian through a covariance matrix can then be obtained as:
> $$\Sigma = RSS^TR^T$$

> [!explanation]-
> To avoid overhead they also explicitly derive the gradients of these parameters.

<!-- guid: K|=#0&)WN[ -->

---

> [!question]
> Give a **schematic** **overview** of the **3D Gaussian Splatting** method.

> [!answer]-
> ![[paste-896b00c7b22cce4ab65041aae87caf41aff7facb.jpg]]

<!-- guid: bfQ<b}[lOZ -->

---

> [!question]
> How is **color** parameterized in **3D Gaussian Splatting**?

> [!answer]-
> Using **spherical harmonics**, this allows the color of a gaussian to be different based on the viewing direction.

<!-- guid: pCS5o(Qm}: -->

---

> [!question]
> How are the initial 3D gaussians obtained in 3D gaussian splatting?

> [!answer]-
> They are taken from **SfM** (Structure-from-motion) that is ran prior to 3D Gaussian Splatting. **SfM** also provides the camera parameters for each image.

> [!explanation]-
> The authors show that using randomly initialized gaussians perform much worse.

<!-- guid: t$UDq)SP.# -->

---

> [!question]
> Which **parameters** of the 3D gaussian are **optimized** in **3D Gaussian Splatting**?

> [!answer]-
> The **3D position** of the guassian, the **properties of the anisotropic gaussian** (through scale and rotation), the $\alpha$ for the $\alpha$-blending and the **spherical harmonics** coefficients.

<!-- guid: EQ0]I~QGz` -->
