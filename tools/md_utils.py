"""Utilities for converting between Anki HTML and Obsidian Markdown,
and for parsing/writing the per-paper Markdown flashcard format.

Markdown format:
    ---
    paper_title: "Title"
    paper_url: https://...
    ---

    > [!question]
    > Question text (can be multi-line)

    > [!answer]-
    > Answer text (can be multi-line)

    > [!explanation]-
    > Optional explanation

    <!-- guid: Mk%J-^b79. -->

    ---
    (next card)
"""

import re
import csv
from pathlib import Path


# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------

def html_to_md(html: str) -> str:
    """Convert Anki HTML to Obsidian-flavored Markdown."""
    if not html:
        return ""

    s = html

    # Normalize &nbsp; to regular space
    s = s.replace("&nbsp;", " ")

    # Images: external URLs → ![](url), local files → ![[file.jpg]]
    s = re.sub(r'<img\s+src="(https?://[^"]+)"[^>]*>', r'![](\1)', s)
    s = re.sub(r'<img\s+src="([^"]+)"[^>]*>', r'![[\1]]', s)

    # Bold: <b>...</b> → **...**
    s = re.sub(r'<b>(.*?)</b>', r'**\1**', s, flags=re.DOTALL)

    # Italic: <i>...</i> or <em>...</em> → *...*
    s = re.sub(r'<i>(.*?)</i>', r'*\1*', s, flags=re.DOTALL)
    s = re.sub(r'<em>(.*?)</em>', r'*\1*', s, flags=re.DOTALL)

    # Underline: <u>...</u> → keep as HTML (no MD equivalent, Obsidian renders it)
    # (leave as-is)

    # Links: <a href="url">text</a> → [text](url)
    s = re.sub(r'<a\s+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.DOTALL)

    # Ordered lists
    s = re.sub(r'<ol>(.*?)</ol>', lambda m: _convert_list(m.group(1), ordered=True), s, flags=re.DOTALL)

    # Unordered lists
    s = re.sub(r'<ul>(.*?)</ul>', lambda m: _convert_list(m.group(1), ordered=False), s, flags=re.DOTALL)

    # Horizontal rules
    s = re.sub(r'<hr\s*/?>', '\n\n---\n\n', s)

    # Line breaks: <br> or <br/> → newline
    s = re.sub(r'<br\s*/?>', '\n', s)

    # Divs/spans: just remove the tags, keep content
    s = re.sub(r'</?div[^>]*>', '\n', s)
    s = re.sub(r'</?span[^>]*>', '', s)

    # Video tags (rare) - keep as HTML
    # (leave as-is)

    # LaTeX: \( ... \) → $ ... $  and  \[ ... \] → $$ ... $$
    s = re.sub(r'\\\((.*?)\\\)', r'$\1$', s, flags=re.DOTALL)
    s = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', s, flags=re.DOTALL)

    # Clean up multiple blank lines
    s = re.sub(r'\n{3,}', '\n\n', s)

    return s.strip()


def _convert_list(inner_html: str, ordered: bool) -> str:
    items = re.findall(r'<li>(.*?)</li>', inner_html, flags=re.DOTALL)
    lines = []
    for i, item in enumerate(items, 1):
        prefix = f"{i}." if ordered else "-"
        lines.append(f"{prefix} {item.strip()}")
    return "\n" + "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Markdown → HTML
# ---------------------------------------------------------------------------

def md_to_html(md: str) -> str:
    """Convert Obsidian-flavored Markdown back to Anki HTML."""
    if not md:
        return ""

    s = md

    # LaTeX first (before bold/italic processing could interfere):
    # $$ ... $$ → \[ ... \]  (display math)
    s = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', s, flags=re.DOTALL)
    # $ ... $ → \( ... \)  (inline math, but not $$)
    s = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'\\(\1\\)', s, flags=re.DOTALL)

    # Images: ![](url) → <img src="url"> (external), ![[file]] → <img src="file"> (local)
    s = re.sub(r'!\[\]\(([^)]+)\)', r'<img src="\1">', s)
    s = re.sub(r'!\[\[([^\]]+)\]\]', r'<img src="\1">', s)

    # Links: [text](url) → <a href="url">text</a>
    # But not image links (already handled above)
    s = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)

    # Bold: **...** → <b>...</b>
    s = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s, flags=re.DOTALL)

    # Italic: *...* → <i>...</i>  (but not ** which is bold)
    s = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', s, flags=re.DOTALL)

    # Horizontal rules (standalone --- lines)
    s = re.sub(r'\n---\n', '\n<hr>\n', s)

    # Line breaks: newlines → <br>
    # But not double newlines (those are paragraph breaks, still use <br>)
    s = re.sub(r'\n', '<br>', s)

    return s.strip()


# ---------------------------------------------------------------------------
# Parse Markdown flashcard file → list of card dicts
# ---------------------------------------------------------------------------

def parse_md_file(path: Path) -> list[dict]:
    """Parse a Markdown flashcard file into a list of card dicts.

    Returns list of dicts with keys: guid, question, answer, paper_title, paper_url, explanation, tags
    """
    text = path.read_text(encoding="utf-8")

    # Extract YAML frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', text, flags=re.DOTALL)
    if not fm_match:
        raise ValueError(f"No frontmatter found in {path}")

    frontmatter = fm_match.group(1)
    paper_title = _extract_yaml_value(frontmatter, "paper_title")
    paper_url = _extract_yaml_value(frontmatter, "paper_url")

    body = text[fm_match.end():]

    # Split into cards by horizontal rule (--- on its own line)
    card_blocks = re.split(r'\n---\n', body)

    cards = []
    for block in card_blocks:
        block = block.strip()
        if not block:
            continue

        question = _extract_callout(block, "question")
        answer = _extract_callout(block, "answer")
        explanation = _extract_callout(block, "explanation")

        if not question and not answer:
            continue

        guid_match = re.search(r'<!--\s*guid:\s*(\S+)\s*-->', block)
        guid = guid_match.group(1) if guid_match else ""

        cards.append({
            "guid": guid,
            "question": md_to_html(question),
            "answer": md_to_html(answer),
            "paper_title": paper_title,
            "paper_url": paper_url,
            "explanation": md_to_html(explanation),
            "tags": "",
        })

    return cards


def _extract_yaml_value(frontmatter: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', frontmatter, flags=re.MULTILINE)
    return match.group(1) if match else ""


def _extract_callout(block: str, callout_type: str) -> str:
    """Extract content from a > [!type] or > [!type]- callout block."""
    pattern = rf'> \[!{callout_type}\]-?\n((?:>.*\n?)*)'
    match = re.search(pattern, block)
    if not match:
        return ""

    lines = match.group(1).strip().split("\n")
    # Remove the leading "> " from each line
    content_lines = []
    for line in lines:
        if line.startswith("> "):
            content_lines.append(line[2:])
        elif line == ">":
            content_lines.append("")
        else:
            content_lines.append(line)

    return "\n".join(content_lines)


# ---------------------------------------------------------------------------
# Write card dicts → Markdown flashcard file
# ---------------------------------------------------------------------------

def write_md_file(path: Path, cards: list[dict]):
    """Write a list of card dicts to a Markdown flashcard file."""
    if not cards:
        return

    paper_title = cards[0]["paper_title"]
    paper_url = cards[0]["paper_url"]

    lines = []
    lines.append("---")
    lines.append(f'paper_title: "{paper_title}"')
    lines.append(f"paper_url: {paper_url}")
    lines.append("---")
    lines.append("")

    for i, card in enumerate(cards):
        question_md = html_to_md(card["question"])
        answer_md = html_to_md(card["answer"])
        explanation_md = html_to_md(card.get("explanation", ""))
        guid = card.get("guid", "")

        # Question callout
        lines.append("> [!question]")
        for line in question_md.split("\n"):
            lines.append(f"> {line}" if line else ">")
        lines.append("")

        # Answer callout (collapsed)
        lines.append("> [!answer]-")
        for line in answer_md.split("\n"):
            lines.append(f"> {line}" if line else ">")
        lines.append("")

        # Explanation callout (collapsed), only if present
        if explanation_md:
            lines.append("> [!explanation]-")
            for line in explanation_md.split("\n"):
                lines.append(f"> {line}" if line else ">")
            lines.append("")

        # GUID as HTML comment
        if guid:
            lines.append(f"<!-- guid: {guid} -->")
            lines.append("")

        # Card separator (except after last card)
        if i < len(cards) - 1:
            lines.append("---")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Convert MD files → temporary CSVs for brain-brew
# ---------------------------------------------------------------------------

def md_to_temp_csv(md_path: Path, csv_path: Path):
    """Convert a Markdown flashcard file to a CSV that brain-brew can read."""
    cards = parse_md_file(md_path)
    if not cards:
        return

    fieldnames = ["guid", "question", "answer", "paper_title", "paper_url", "explanation", "tags"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cards)
