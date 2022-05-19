# MLRF
**M**achine **L**earning **R**esearch **F**lashcards (for [Anki](http://ankisrs.net/))

## Description
MLRF is a collection of flashcards that can be used with [Anki](http://ankisrs.net/).
The flashcards in this repository are associated with scientific research papers in the field of machine learning.

As a machine learning researcher I read a lot of papers to keep up with the state-of-the-art. 
However, for many papers I was only able to recall "Oh I read a paper about that" when a related topic would come up months later, without being able to give much more details.
Intrigued by the article from Michael Nielsen ["Augmenting Long-term Memory"](http://augmentingcognition.com/ltm.html), I started using Anki.

The flashcards in this repository are not a replacement for reading the actual paper, but rather an additional resource to retain the knowledge from these papers.
Initially the papers covered by this repository are mainly selected based on my own interests and topics I do research about.
However, by open sourcing this repository, I invite everyone that has interests in using Anki for Machine Learning papers to collaborate on these flashcards.

## Preview
![image](https://user-images.githubusercontent.com/11473168/118519631-9540c180-b739-11eb-8765-b8a207786bdb.png)

## Papers

| Title | URL | flashcards |
| ----- | ----- | ---------- |
| Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour| [[`arXiv`](https://arxiv.org/abs/1706.02677)] | [[`accurate_large_minibatch_sgd.csv`](flashcards/accurate_large_minibatch_sgd.csv)]|
| Anchor Pruning for Object Detection | [[`arXiv`](https://arxiv.org/abs/2104.00432)] | [[`anchor_pruning.csv`](flashcards/anchor_pruning.csv)]|
| Attention Is All You Need | [[`arXiv`](https://arxiv.org/abs/1706.03762)] | [`attention_is_all_you_need.csv`](flashcards/attention_is_all_you_need.csv)]|
| AutoSlim: Towards One-Shot Architecture Search for Channel Numbers | [[`arXiv`](https://arxiv.org/abs/1903.11728)] | [[`autoslim.csv`](flashcards/autoslim.csv)]|
| Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift | [[`arXiv`](https://arxiv.org/abs/1502.03167)] | [[`batchnorm.csv`](flashcards/batchnorm.csv)]|
| DETR: End-to-End Object Detection with Transformers | [[`arXiv`](https://arxiv.org/abs/1503.02531)] | [[`detr.csv`](flashcards/detr.csv)]|
| Distilling the Knowledge in a Neural Network | [[`arXiv`](https://arxiv.org/abs/1503.02531)] | [[`knowledge_distillation.csv`](flashcards/knowledge_distillation.csv)]|
| Focal Loss for Dense Object Detection | [[`arXiv`](https://arxiv.org/abs/1708.02002)] | [[`retinanet.csv`](flashcards/retinanet.csv)]|
| MobileNetV2: Inverted Residuals and Linear Bottlenecks | [[`arXiv`](https://arxiv.org/abs/1801.04381)] | [[`mobilenetv2.csv`](flashcards/mobilenetv2.csv)]|
| MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications | [[`arXiv`](https://arxiv.org/abs/1704.04861)] | [[`mobilenetv1.csv`](flashcards/mobilenetv1.csv)]|
| Multi-Scale Context Aggregation by Dilated Convolutions | [[`arXiv`](https://arxiv.org/abs/1511.07122)] | [[`multi_scale_context_dilated_convolutions.csv`](flashcards/multi_scale_context_dilated_convolutions.csv)]|
| On Network Design Spaces for Visual Recognitio | [[`arXiv`](https://arxiv.org/abs/1905.13214)] | [[`network_design_spaces.csv`](flashcards/network_design_spaces.csv)]|
| Once-for-All: Train One Network and Specialize it for Efficient Deployment | [[`arXiv`](https://arxiv.org/abs/1908.09791)] | [[`once_for_all.csv`](flashcards/once_for_all.csv)]|
| SSD: Single Shot MultiBox Detector | [[`arXiv`](https://arxiv.org/abs/1512.02325)] | [[`ssd.csv`](flashcards/ssd.csv)]|
| Slimmable Neural Networks | [[`arXiv`](https://arxiv.org/abs/1812.08928)] | [[`slimmable_neural_networks.csv`](flashcards/slimmable_neural_networks.csv)]|
| Squeeze and Excitation Networks| [[`arXiv`](https://arxiv.org/abs/1709.01507)] | [[`squeeze_and_excitation.csv`](flashcards/squeeze_and_excitation.csv)]|
| The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks | [[`arXiv`](https://arxiv.org/abs/1803.03635)] | [[`lottery_ticket.csv`](flashcards/lottery_ticket.csv)]|
| Understanding the Effective Receptive Field in Deep Convolutional Neural Networks | [[`arXiv`](https://arxiv.org/abs/1701.04128)] | [[`understanding_receptive_field.csv`](flashcards/understanding_receptive_field.csv)]|
| Universally Slimmable Networks and Improved Training Techniques | [[`arXiv`](https://arxiv.org/abs/1903.05134)] | [[`universally_slimmable_networks.csv`](flashcards/universally_slimmable_networks.csv)]|
___
## Usage
The flashcards in this repository are made for [Anki](http://ankisrs.net/).
Additionally, you also need to install the Anki add-on [CrowdAnki](https://github.com/Stvad/CrowdAnki).

Once you cloned this repository you can use `tools/source_to_anki.py` to create a deck that can be imported in Anki.
`tools/anki_to_source` can be used to update or add your own cards to this repository.

In order to run these scripts you need to install [brain brew](https://github.com/ohare93/brain-brew/) and pandas `pip install brain-brew pandas`.

### `source_to_anki`
```
usage: python tools/source_to_anki.py [-h] [--include INCLUDE [INCLUDE ...]] [--exclude EXCLUDE [EXCLUDE ...]]

Tool to convert the source format of this repository to a crowdAnki folder that can be imported into Anki.

optional arguments:
  -h, --help            show this help message and exit
  --include INCLUDE [INCLUDE ...]
                        You can convert only part of this repository by using this argument with a list of the csv files to convert. E.g. `--include ofa.csv mobilenetv2.csv`
  --exclude EXCLUDE [EXCLUDE ...]
                        Exclude certain papers in the crowdAnki export folder. E.g. `--exclude ofa.csv mobilenetv2.csv`
```
The resulting export folder will be created in `MLRF/build/`. To add the cards to Anki do the following:
* Open Anki and make sure your devices are all synchronised.
* In the File menu, select CrowdAnki: Import from disk.
* Browse for and select `MLRF/build/`

#### Recommended next steps:
* **Review** all cards in the MLRF deck, delete the cards you're not interested in (see also TODO).
* **Move** the cards to a deck of your own.  (This allows you use your own card scheduling steps)

### `anki_to_source`
```
usage: python tools/anki_to_source.py [-h] crowdanki_folder

Tool to convert crowdAnki export folder to the format of this repository.

positional arguments:
  crowdanki_folder  Location of the crowdAnki export folder.
```
### Important notes:

* This tool only extracts cards that use the `paper_basic` note model from this repository. 
This means that you can export a deck that contains more than just your machine learning research flashcards.
* `paper_basic` cards that are tagged with `DoNotSync` are ignored. 
* Tags are not copied to this repository 




