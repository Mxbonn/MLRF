# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MLRF (Machine Learning Research Flashcards) is a collection of Anki spaced-repetition flashcards tied to ML research papers. The source of truth is Markdown files in `flashcards/`, which are converted to/from Anki decks via Python scripts. The flashcards directory is symlinked into an Obsidian vault for reading/editing.

## Key Commands

```bash
# Install dependencies
uv sync

# Generate Anki deck from MD source files → outputs to build/
uv run python tools/source_to_anki.py

# Generate deck from specific papers only
uv run python tools/source_to_anki.py --include paper1.md paper2.md
uv run python tools/source_to_anki.py --exclude paper1.md

# Import Anki changes back to MD source
uv run python tools/anki_to_source.py <crowdanki_folder>
```

## Architecture

Roundtrip conversion pipeline:

```
MD files (flashcards/*.md)  ←→  CrowdAnki folder (build/)  ←→  Anki app
       source_to_anki.py →                        ← anki_to_source.py
```

- **`flashcards/*.md`**: One Markdown file per paper using Obsidian callout syntax (`> [!question]`, `> [!answer]-`, `> [!explanation]-`). Cards separated by `---`. GUIDs stored as `<!-- guid: ... -->` HTML comments. Frontmatter contains `paper_title` and `paper_url`.
- **`flashcards/metadata/`**: Anki deck config (header.yaml), note model (paper_basic.yaml), card template (Card.html, style.css), and media files (images/GIFs)
- **`tools/source_to_anki.py`**: Converts MD→temp CSV, uses brain-brew to build CrowdAnki-importable deck, syncs generated GUIDs back to MD
- **`tools/anki_to_source.py`**: Exports Anki edits back to MD; filters to `paper_basic` model, ignores `DoNotSync`-tagged cards, syncs media
- **`tools/md_utils.py`**: HTML↔Markdown conversion and MD file parsing/writing

## Adding a New Paper

1. Create a new `.md` file in `flashcards/` following existing format
2. Add any images to `flashcards/metadata/media/`
3. Use `$$...$$` for display math, `$...$` for inline math
4. Use `![[image.jpg]]` for local images, `![](url)` for external images

## Flashcard Guidelines

When creating flashcards for a paper, focus on **technical depth and architecture**, not breadth:

- **Lead with architecture**: Start with how the system works (inputs, outputs, major components), then dive into design choices and trade-offs.
- **Atomicity over combination**: Split combined questions into separate cards if each concept can stand alone (e.g., separate "Which loss is used?" from "How are actions tokenized?"). Standalone cards are more reusable.
- **Vertical depth > horizontal breadth**: Go deep on key components (FiLM, TokenLearner, inference speed constraints) rather than broad comparisons (vs. Gato, ablations, experimental tables). Keep cards ~8–10 total.
- **Skip meta**: Avoid cards about motivation, problem statement, dataset curation details, or experimental setup unless they directly explain a design choice.
- **Use images strategically**: Reference actual media files from `flashcards/metadata/media/` (e.g., `![[model_diagram.png]]`); don't create placeholder references.