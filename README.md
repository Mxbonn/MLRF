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

## Papers

| Title | arXiv | flashcards |
| ----- | ----- | ---------- |
| Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour| [[`arXiv`](https://arxiv.org/abs/1706.02677)] | [`accurate_large_minibatch_sgd.csv`](flashcards/accurate_large_minibatch_sgd.csv)]|
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




