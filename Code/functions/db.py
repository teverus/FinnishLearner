from typing import Union

from pandas import DataFrame

from Code.constants import *
from Code.functions.general import find_item_in_db
from Code.functions.high_level import get_all_words
from Code.sentences.grammar_constants import *


def update_item_score(main, change: Union[int, list]):
    target_file = {
        ItemType.WORD: ALL_WORDS,
        ItemType.VERB: ALL_VERBS,
        ItemType.COMBINATION: ALL_WORDS,
    }
    target_file = target_file[main.item.item_type]

    df = get_all_words(target_file)

    indices = find_item_in_db(main, df)
    indices = [indices] if not isinstance(indices, list) else indices
    change = [change] if not isinstance(change, list) else change

    for answer, index in enumerate(indices):
        proper_change = change[0] if len(change) == 1 else change[answer]
        df.loc[index, SCORE] += proper_change

    df.sort_values(by=SCORE, kind="mergesort", inplace=True, ignore_index=True)

    df.to_excel(target_file, index=False)


def export_constructions(constructions):
    df = DataFrame([], columns=PARTS_OF_SENTENCE)

    for index, construction in enumerate(constructions):
        entry = []
        for part_of_sentence in PARTS_OF_SENTENCE:
            if part_of_sentence in construction.keys():
                entry.append(construction[part_of_sentence])
            else:
                entry.append("X")
        df.loc[index] = entry

    df.to_excel(ALL_CONSTRUCTIONS, index=False)
