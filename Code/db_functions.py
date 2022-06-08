import pandas as pd
from pandas import DataFrame

from Code.constants import *
from Code.sentences.grammar_constants import *


def get_all_words(target_file: str = ALL_WORDS, sort_by=SCORE) -> DataFrame:
    df = pd.read_excel(target_file).drop_duplicates().fillna({SCORE: 0})
    df.Score = df.Score.astype(int)

    if sort_by:
        df.sort_values(by=sort_by, kind="mergesort", inplace=True, ignore_index=True)

    return df


def update_word_score(main, change: int):
    df = get_all_words()
    word = main.word

    df.loc[(df.Finnish == word.finnish) & (df.English == word.english), SCORE] += change

    df.sort_values(by=SCORE, kind="mergesort", inplace=True, ignore_index=True)

    df.to_excel(ALL_WORDS, index=False)


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


def save_verb_forms(verb_forms: dict, infinitive: str):
    df = DataFrame([], columns=VERB_FORMS)

    for index, (finnish, english) in enumerate(verb_forms.items()):
        df.loc[index] = [finnish, english, 0, infinitive]

    a = 1
