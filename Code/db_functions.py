import pandas as pd
from pandas import DataFrame

from Code.constants import *


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
