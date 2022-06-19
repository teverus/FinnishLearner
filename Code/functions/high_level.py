import pandas as pd
from pandas import DataFrame

from Code.constants import ALL_WORDS, SCORE, ALL_VERBS, VERB_FORMS


def get_all_words(target_file: str, sort_by=SCORE) -> DataFrame:
    df = pd.read_excel(target_file).drop_duplicates().fillna({SCORE: 0})
    df.Score = df.Score.astype(int)

    if sort_by:
        df.sort_values(by=sort_by, kind="mergesort", inplace=True, ignore_index=True)

    return df


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
