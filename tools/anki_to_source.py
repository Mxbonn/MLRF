import argparse
from pathlib import Path

import pandas as pd
from brain_brew.build_tasks.crowd_anki.media_group_from_crowd_anki import MediaGroupFromCrowdAnki
from brain_brew.build_tasks.crowd_anki.notes_from_crowd_anki import NotesFromCrowdAnki
from brain_brew.build_tasks.deck_parts.media_group_from_folder import MediaGroupFromFolder
from brain_brew.build_tasks.deck_parts.save_media_group_to_folder import SaveMediaGroupsToFolder
from brain_brew.configuration.file_manager import FileManager
from brain_brew.representation.yaml.media_group import MediaGroup

from md_utils import write_md_file

NOTE_MODEL = 'paper_basic'
FIELD_NAMES = ['question', 'answer', 'paper_title', 'paper_url', 'explanation']
MEDIA_FOLDER = 'flashcards/metadata/media/'
NOTES_FOLDER = 'flashcards'


def anki_to_source(crowdanki_folder):
    project_root = Path(__file__).parents[1]
    FileManager()

    # collect notes
    notes_ca = NotesFromCrowdAnki.from_repr(NotesFromCrowdAnki.Representation(
        source=crowdanki_folder, part_id="deck_notes"
    ))
    notes = notes_ca.execute().part
    notes = notes.get_sorted_notes_copy(sort_by_keys=[], reverse_sort=False, case_insensitive_sort=True)

    # Only process relevant notes
    data = []
    for note in notes:
        if note.note_model == NOTE_MODEL:
            row = {'guid': note.guid}
            row.update(dict(zip(FIELD_NAMES, note.fields)))
            if 'DoNotSync' in note.tags:
                continue
            row["tags"] = ""
            data.append(row)

    df = pd.DataFrame(data)

    # process media
    media_folder = project_root.joinpath(MEDIA_FOLDER)
    media_group_ca = MediaGroupFromCrowdAnki.from_repr(MediaGroupFromFolder.Representation(
        source=crowdanki_folder, part_id="deck_media"
    ))
    media_group_ca.execute()

    save_media_to_folder = SaveMediaGroupsToFolder.from_repr(SaveMediaGroupsToFolder.Representation(
        parts=['deck_media'], folder=str(media_folder), recursive=True, clear_folder=True
    ))

    existing_media_group = MediaGroup.from_directory(save_media_to_folder.folder, save_media_to_folder.recursive)
    all_media_group = MediaGroup.from_many(save_media_to_folder.parts)

    in_both, to_move, to_delete = all_media_group.compare(existing_media_group)

    new_to_move = set()
    for file in to_move:
        if file[-4:] == ".css":
            new_to_move.add(file)
        elif df['question'].str.contains(file).any() or df['answer'].str.contains(file).any()\
                or df['explanation'].str.contains(file).any():
            new_to_move.add(file)
    to_move = new_to_move

    media_folder.mkdir(parents=True, exist_ok=True)
    for filename, media_file in all_media_group.media_files.items():
        if filename in in_both:
            media_file.copy_self_to_target(existing_media_group.media_files[filename].file_path)
        elif filename in to_move:
            media_file.copy_self_to_target(str(media_folder))

    if to_delete:
        for delete_name in to_delete:
            existing_media_group.media_files[delete_name].delete_self()

    # Write to Markdown files instead of CSV
    notes_folder = project_root.joinpath(NOTES_FOLDER)
    mapping = get_existing_papers_mapping()
    i = 1
    for name, group in df.groupby('paper_title'):
        if name in mapping:
            filename = notes_folder / f'{mapping[name]}.md'
        else:
            filename = notes_folder / f'{i}.md'
            i += 1
        cards = group.to_dict('records')
        write_md_file(filename, cards)


def get_existing_papers_mapping():
    project_root = Path(__file__).parents[1]
    notes_folder = project_root.joinpath(NOTES_FOLDER)
    mapping = {}

    from md_utils import parse_md_file
    for md_file in notes_folder.glob('*.md'):
        cards = parse_md_file(md_file)
        if cards:
            mapping[cards[0]['paper_title']] = md_file.stem

    return mapping


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert CrowdAnki export folder to Markdown flashcard files.")
    parser.add_argument('crowdanki_folder', type=str, help="Location of the CrowdAnki export folder.")
    args = parser.parse_args()
    anki_to_source(args.crowdanki_folder)
