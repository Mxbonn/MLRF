import os
import tempfile
import shutil
from pathlib import Path
import argparse

from brain_brew.configuration.file_manager import FileManager
from brain_brew.commands.run_recipe.top_level_builder import TopLevelBuilder

from md_utils import md_to_temp_csv


NOTE_MODEL = 'paper_basic'
NOTE_MODEL_FILE = 'flashcards/metadata/paper_basic.yaml'
MEDIA_FOLDER = 'flashcards/metadata/media/'
NOTES_FOLDER = 'flashcards'
DECK_HEADERS_FILE = 'flashcards/metadata/header.yaml'
BUILD_FOLDER = 'build/'


def source_to_anki(args):
    project_root = Path(__file__).parents[1]
    os.chdir(str(project_root))
    FileManager()

    notes_folder = project_root.joinpath(NOTES_FOLDER)
    md_files = sorted(notes_folder.glob('*.md'))

    filtered_files = []
    for md_file in md_files:
        if args.exclude and md_file.name in args.exclude:
            continue
        if args.include and md_file.name not in args.include:
            continue
        filtered_files.append(md_file)

    # Convert MD files to temporary CSVs for brain-brew
    tmp_dir = Path(tempfile.mkdtemp())
    csv_files = []
    try:
        for md_file in filtered_files:
            csv_path = tmp_dir / md_file.with_suffix('.csv').name
            md_to_temp_csv(md_file, csv_path)
            csv_files.append(str(csv_path))

        data = [
            {'generate_guids_in_csvs': {'source': csv_files, 'columns': ['guid']}},
            {'build_parts': [
                {'note_models_from_yaml_part': {
                    'part_id': NOTE_MODEL,
                    'file': NOTE_MODEL_FILE
                }},
                {'headers_from_yaml_part': {
                    'part_id': 'deck_headers',
                    'file': DECK_HEADERS_FILE,
                }},
                {'notes_from_csvs': {
                    'part_id': 'deck_notes',
                    'file_mappings': [{'file': file, 'note_model': NOTE_MODEL} for file in csv_files],
                    'note_model_mappings': [{'note_models': [NOTE_MODEL]}]
                }},
                {'media_group_from_folder': {
                    'part_id': 'deck_media',
                    'source': MEDIA_FOLDER,
                    'recursive': True,
                }}]},
            {'generate_crowd_anki': {
                'folder': BUILD_FOLDER,
                'notes': {'part_id': 'deck_notes'},
                'note_models': {'parts': [NOTE_MODEL]},
                'headers': 'deck_headers',
                'media': {'parts': ['deck_media']}
            }}
        ]
        recipe = TopLevelBuilder.from_list(data)
        recipe.execute()

        # Write back any newly generated GUIDs to the MD files
        _sync_guids_back(filtered_files, csv_files)

    finally:
        shutil.rmtree(tmp_dir)


def _sync_guids_back(md_files: list[Path], csv_files: list[str]):
    """After brain-brew generates GUIDs, write them back to the MD source files."""
    import csv as csv_mod
    from md_utils import parse_md_file, write_md_file

    for md_file, csv_file in zip(md_files, csv_files):
        # Read the GUIDs from the (potentially updated) CSV
        with open(csv_file, encoding="utf-8") as f:
            reader = csv_mod.DictReader(f)
            csv_guids = [row["guid"] for row in reader]

        # Read the current MD cards
        cards = parse_md_file(md_file)

        # Check if any GUIDs were added/changed
        changed = False
        for card, guid in zip(cards, csv_guids):
            if card["guid"] != guid:
                card["guid"] = guid
                changed = True

        if changed:
            write_md_file(md_file, cards)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown flashcard source files to a CrowdAnki deck.")
    parser.add_argument('--include', nargs='+', type=str,
                        help="Only convert specific files. E.g. `--include batchnorm.md clip.md`")
    parser.add_argument('--exclude', nargs='+', type=str,
                        help="Exclude specific files. E.g. `--exclude batchnorm.md clip.md`")
    args = parser.parse_args()
    source_to_anki(args)
