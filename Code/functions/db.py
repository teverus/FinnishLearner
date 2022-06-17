import pandas as pd
from pandas import DataFrame

from Code.constants import *
from Code.functions.general import find_item_in_db
from Code.sentences.grammar_constants import *


def get_all_words(target_file: str = ALL_WORDS, sort_by=SCORE) -> DataFrame:
    df = pd.read_excel(target_file).drop_duplicates().fillna({SCORE: 0})
    df.Score = df.Score.astype(int)

    if sort_by:
        df.sort_values(by=sort_by, kind="mergesort", inplace=True, ignore_index=True)

    return df


def update_item_score(main, change: int):
    target_file = {
        ItemType.WORD: ALL_WORDS,
        ItemType.VERB: ALL_VERBS
    }
    target_file = target_file[main.item.item_type]

    df = get_all_words(target_file)

    df.loc[find_item_in_db(main, df).index.item(), SCORE] += change

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


def save_verb_forms(
        verb_forms: list, tense: str, infinitive: str, negativity: str, mood: str
):
    df_orig = pd.read_excel(ALL_VERBS, converters={"Negative": str, "Plural": str})
    df = DataFrame([], columns=VERB_FORMS)

    for index, verb_form in enumerate(verb_forms, 1):
        person = index if index < 4 else index - 3
        plural = "plural" if index > 3 else "singular"
        df.loc[index] = [
            verb_form,
            mood.split()[0].capitalize(),
            tense.split("{}")[0].capitalize(),
            negativity.capitalize(),
            person,
            plural.capitalize(),
            0,
            infinitive,
        ]

    df_final = pd.concat([df_orig, df], ignore_index=True)
    df_final.to_excel(ALL_VERBS, index=False)
