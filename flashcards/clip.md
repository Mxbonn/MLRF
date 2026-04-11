---
paper_title: "Learning Transferable Visual Models From Natural Language Supervision"
paper_url: https://arxiv.org/abs/2103.00020
---

> [!question]
> Give a summary of the approach used in **CLIP**.

> [!answer]-
> ![[paste-39fa726bd182ceab62978bfde49ed398a1c02ba7.jpg]]
> Given a batch of $N$ (image, text) pairs, CLIP learns a multi-model embedding space by jointly training an image encoder and text encoder to maximize the cosine similarity of the image and text embeddings of the $N$ correct pairs while minimizing the cosine similarity of the $N^2 - N$ incorrect pairs. (It is optimized using a symmetric cross entropy loss over these similarity scores)

<!-- guid: CeybD~r>=% -->

---

> [!question]
> How many (image, text) pairs were collected in the dataset used to train **CLIP**?

> [!answer]-
> 400 million

<!-- guid: Jr:$:]5$=U -->
