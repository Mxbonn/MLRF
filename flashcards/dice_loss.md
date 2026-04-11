---
paper_title: "V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation"
paper_url: https://arxiv.org/abs/1606.04797
---

> [!question]
> What is the formula for the **dice loss** used in segmentation tasks?

> [!answer]-
> $$\mathcal{L}_{dice} = 1 - \frac{2 \cdot |A \cap B|}{|A| + |B|}$$Where $A$ and $B$ are the ground truth and predicted mask.

> [!explanation]-
> In PyTorch this can be implemented as:
>
> def dice_loss(input, target):
>
>     smooth = 1.
>
>     iflat = input.view(-1)
>
>     tflat = target.view(-1)
>
>     intersection = (iflat * tflat).sum()
>
>    
>
>     return 1 - ((2. * intersection + smooth) /
>
>               (iflat.sum() + tflat.sum() + smooth))

<!-- guid: p.kLC3W~JH -->
