"""One-time migration script: convert existing CSV flashcard files to Markdown format."""

import csv
from pathlib import Path

from md_utils import write_md_file


NOTES_FOLDER = Path(__file__).parents[1] / "flashcards"


def migrate_all():
    csv_files = sorted(NOTES_FOLDER.glob("*.csv"))
    if not csv_files:
        print("No CSV files found.")
        return

    for csv_path in csv_files:
        cards = []
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cards.append({
                    "guid": row.get("guid", ""),
                    "question": row.get("question", ""),
                    "answer": row.get("answer", ""),
                    "paper_title": row.get("paper_title", ""),
                    "paper_url": row.get("paper_url", ""),
                    "explanation": row.get("explanation", ""),
                    "tags": row.get("tags", ""),
                })

        md_path = csv_path.with_suffix(".md")
        write_md_file(md_path, cards)
        print(f"  {csv_path.name} → {md_path.name}  ({len(cards)} cards)")

    print(f"\nMigrated {len(csv_files)} files. Review the .md files, then delete the .csv originals.")


if __name__ == "__main__":
    migrate_all()
