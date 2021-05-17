import os
from pathlib import Path
import argparse

from brain_brew.configuration.file_manager import FileManager
from brain_brew.commands.run_recipe.top_level_builder import TopLevelBuilder


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
    csv_files = notes_folder.glob('*.csv')
    filtered_csv_files = []
    for csv_file in csv_files:
        if args.exclude and csv_file.name in args.exclude:
            continue
        if args.include and csv_file.name not in args.include:
            continue
        else:
            filtered_csv_files.append(csv_file)
    csv_files = [str(file) for file in filtered_csv_files]

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to convert the source format of this repository to a crowdAnki"
                                                 " folder that can be imported into Anki.")
    parser.add_argument('--include', nargs='+', type=str, help="You can convert only part of this repository by using "
                                                               "this argument with a list of the csv files to convert. "
                                                               "E.g. `--include ofa.csv mobilenetv2.csv`")
    parser.add_argument('--exclude', nargs='+', type=str, help="Exclude certain papers in the crowdAnki export folder. "
                                                               "E.g. `--exclude ofa.csv mobilenetv2.csv`")
    args = parser.parse_args()
    source_to_anki(args)
