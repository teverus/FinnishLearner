import random
import re
from typing import Union, List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

from Code.constants import (
    COUNT,
    SCORE,
    SCORE_TO_TIER,
    Statistics,
    Tier,
    ItemType,
    ENGLISH,
    FINNISH,
    PERSONAL_PRONOUNS,
    ALL_TIERS,
    SCREEN_WIDTH,
    Word,
    ALL_WORDS,
    POSITIVE,
    NEGATIVE,
    Tense,
    Mood,
    ALL_VERBS,
)
from Code.functions.high_level import get_all_words, save_verb_forms
from Code.functions.ui import print_a_message, do_nothing


def get_stats(df: DataFrame, simple=False) -> dict:
    stats = get_stats_dict(simple)

    if not simple:
        groups = df.groupby(SCORE).size().reset_index(name=COUNT)

        for _, group in groups.iterrows():
            score = group[SCORE]
            count = group[COUNT]
            score = 0 if score <= 0 else score
            score = 15 if score >= 15 else score
            major = SCORE_TO_TIER[score][0]
            minor = SCORE_TO_TIER[score][1]

            stats[Statistics.TIERS][major][minor][Tier.TOTAL] += count
            stats[Statistics.TIERS][major][minor][Tier.LEFT] += count

    return stats


def get_stats_dict(simple) -> dict:
    if simple:
        return {Statistics.CORRECT: 0, Statistics.INCORRECT: 0}
    else:
        return {
            Statistics.CORRECT: 0,
            Statistics.INCORRECT: 0,
            Statistics.TIERS: {
                Tier.BEGINNER: {
                    Tier.LOWER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.MIDDLE: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.UPPER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                },
                Tier.PRE_INTERMEDIATE: {
                    Tier.LOWER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.MIDDLE: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.UPPER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                },
                Tier.INTERMEDIATE: {
                    Tier.LOWER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.MIDDLE: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.UPPER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                },
                Tier.UPPER_INTERMEDIATE: {
                    Tier.LOWER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.MIDDLE: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.UPPER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                },
                Tier.ADVANCED: {
                    Tier.LOWER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.MIDDLE: {Tier.TOTAL: 0, Tier.LEFT: 0},
                    Tier.UPPER: {Tier.TOTAL: 0, Tier.LEFT: 0},
                },
            },
            Statistics.CURRENT_TIER: [Tier.BEGINNER, Tier.LOWER],
        }


def get_random_item(main):
    word = choose_an_item(main)

    while word is False:
        advance_current_tier(main)
        word = choose_an_item(main)


def choose_an_item(main):
    df = main.snapshot

    if main.item.item_type == ItemType.COMBINATION:
        for key, value in main.item.pattern.items():
            element = value["type"]
            df_ = df.loc[df.PartOfSpeech == element].groupby(SCORE).groups.keys()
            lowest_score = sorted(list(df_))[0]

            options = df.loc[(df.PartOfSpeech == element) & (df.Score == lowest_score)]

            random_number = random.randint(0, len(options) - 1)
            random_item = options.iloc[random_number]

            main.item.english = f"{main.item.english} {random_item.English}"
            main.item.finnish = f"{main.item.finnish} {random_item.Finnish}"

            main.item.pattern[key].update(
                {ENGLISH: random_item.English, FINNISH: random_item.Finnish}
            )

        main.item.english = main.item.english.strip()
        main.item.finnish = main.item.finnish.strip()

        return True

    current_tier = main.stats[Statistics.CURRENT_TIER]
    max_score = [_ for _, value in SCORE_TO_TIER.items() if value == current_tier][0]

    if max_score == 0:
        items_on_this_tier = df.loc[df.Score <= max_score]
    elif max_score == 15:
        items_on_this_tier = df.loc[df.Score >= max_score]
    else:
        items_on_this_tier = df.loc[df.Score == max_score]

    if len(items_on_this_tier) == 0:
        return False

    elif len(items_on_this_tier.groupby(SCORE)) != 1:
        available_groups = list(items_on_this_tier.groupby(SCORE).groups.keys())
        for group in available_groups:
            items_on_this_tier = df.loc[df.Score == group]
            break

    random_number = random.randint(0, len(items_on_this_tier) - 1)
    random_item = items_on_this_tier.iloc[random_number]

    if main.item.item_type == ItemType.WORD:
        main.item.finnish = random_item.Finnish
        main.item.english = random_item.English

    elif main.item.item_type == ItemType.VERB:
        main.item.finnish = random_item["Verb form"]
        ri = random_item
        pronoun = PERSONAL_PRONOUNS[f"{ri.Person} {ri.Plural}"]
        main.item.english = (
            f"[{ri.English}] ({ri.Negative}|{ri.Mood}|{ri.Tense})\n Finnish: {pronoun}"
        )


def advance_current_tier(main):
    current_tier = main.stats[Statistics.CURRENT_TIER]
    next_tier = [ALL_TIERS[i + 1] for i, t in enumerate(ALL_TIERS) if t == current_tier]
    main.stats[Statistics.CURRENT_TIER] = next_tier[0]


def check_answer(main) -> list:
    answer = main.answer
    expected_answer = main.item.finnish

    if answer == expected_answer:
        target_stats = Statistics.CORRECT
        score_delta = 1

        print(" ")

        col_w = int((SCREEN_WIDTH - 2) / 3)
        label = f"{'-' * col_w}<{'CORRECT ANSWER '.center(col_w)}>{'-' * col_w}"
        print_a_message(label, border="=")

    else:
        target_stats = Statistics.INCORRECT

        if main.item.item_type == ItemType.COMBINATION:
            score_delta = evaluate_answer(main)
            incorrect = {Word.ENGLISH: "", Word.FINNISH: "", Word.INCORRECT: ""}
            for index, score in enumerate(score_delta):
                if score == -1:
                    en = incorrect[Word.ENGLISH]
                    fi = incorrect[Word.FINNISH]
                    nc = incorrect[Word.INCORRECT]
                    ans_en = main.item.pattern[index][ENGLISH]
                    ans_fi = main.item.pattern[index][FINNISH]
                    false = answer.split()[index]

                    incorrect[Word.ENGLISH] = ans_en if not en else f"{en} {ans_en}"
                    incorrect[Word.FINNISH] = ans_fi if not fi else f"{fi} {ans_fi}"
                    incorrect[Word.INCORRECT] = false if not nc else f"{nc} {false}"

            main.incorrect_answers[main.index] = incorrect

            user_answer = f', not "{incorrect[Word.INCORRECT]}"' if answer else ""
            expected_answer = incorrect[Word.FINNISH]

        else:
            main.incorrect_answers[main.index] = {
                Word.ENGLISH: main.item.english,
                Word.FINNISH: expected_answer,
                Word.INCORRECT: answer,
            }

            score_delta = -1

            user_answer = f', not "{answer}"' if answer else ""

        if main.item.item_type == ItemType.VERB:
            inf_en = re.findall(r"\[(.*)\]", main.item.english)
            assert len(inf_en) == 1, "\n[ERROR] Couldn't parse infinitive"
            inf_en = inf_en[0]
            df = main.snapshot
            inf_fi = df.loc[df.English == inf_en].Infinitive.values[0]
            inf_fi = f" [{inf_fi}]"
        else:
            inf_fi = ""

        print("")
        print_a_message(
            f"""Sorry, it's "{expected_answer}"{user_answer}{inf_fi}""",
            border="~",
            centered=True,
        )
        print("")

        make_user_write_type_three_times(main)

    main.stats[target_stats] += 1
    update_current_tier(main) if Statistics.CURRENT_TIER in main.stats else do_nothing()
    remove_current_item_from_snapshot(main)

    return score_delta


def update_current_tier(main):
    major, minor = main.stats[Statistics.CURRENT_TIER]
    tiers = main.stats[Statistics.TIERS]
    tiers[major][minor][Tier.LEFT] -= 1


def make_user_write_type_three_times(main):
    if main.item.item_type == ItemType.COMBINATION:
        proper_answer = main.incorrect_answers[main.index][FINNISH]
    else:
        proper_answer = main.item.finnish
    print(f' Please type "{proper_answer}" and hit "Enter" three times.')

    correct_times = 0
    max_times = 3
    while correct_times != max_times:
        user_input = input(" >>> ").replace("a:", "ä").replace("o:", "ö")
        if user_input == proper_answer:
            correct_times += 1
            if correct_times == max_times:
                print(f" [SUCCESS] That's it :) Keep on learning :)")
            else:
                print(f" [SUCCESS] Yes! {max_times - correct_times} to go!")
        else:
            print(f' [FAILURE] Nope, you need to type "{proper_answer}".')


def remove_current_item_from_snapshot(main):
    df = main.snapshot
    if main.item.item_type == ItemType.COMBINATION:
        indices = find_item_in_db(main, df)
    else:
        indices = [find_item_in_db(main, df)]

    for index in indices:
        df.drop(index, inplace=True)


def find_item_in_db(main, df: DataFrame):
    items = None
    word = main.item
    finnish = word.finnish
    english = word.english

    if main.item.item_type == ItemType.WORD:
        items = df.loc[(df.Finnish == finnish) & (df.English == english)]
    elif main.item.item_type == ItemType.VERB:
        items = df.loc[df["Verb form"] == main.item.finnish]
    elif main.item.item_type == ItemType.COMBINATION:
        items = [
            df.loc[(df.Finnish == e[FINNISH]) & (df.English == e[ENGLISH])]
            for e in main.item.pattern.values()
        ]

    if len(items) == 1:
        return items.index.item()
    elif len(items) > 1:
        return [item.index.item() for item in items]
    else:
        raise Exception("\n[ERROR] Couldn't find an item in db")


def get_incorrect_answers(main):
    incorrect_answers = []

    for key, value in main.incorrect_answers.items():
        if main.item.item_type == ItemType.VERB:
            verb, correct, incorrect = main.incorrect_answers[key].values()
            verb = re.findall(r"\]\s\((.*)\)", verb)[0]
            result = [verb, correct, incorrect]
        elif main.item.item_type in [ItemType.WORD, ItemType.COMBINATION]:
            result = list(main.incorrect_answers[key].values())
        else:
            raise Exception("\n\n[ERROR] Unknown item_type\n")

        incorrect_answers.append(result)

    return incorrect_answers


def check_if_new_items_should_be_added(main):
    if main.item.item_type == ItemType.VERB:
        add_new_verbs(main)


def exclude_item_types(main, excluded_types: Union[List, bool]):
    df = main.snapshot
    modified_df = None

    for excluded_type in excluded_types:
        if modified_df is None:
            modified_df = df.loc[df.PartOfSpeech != excluded_type]
        else:
            modified_df = modified_df.loc[modified_df.PartOfSpeech != excluded_type]

    return modified_df


def include_only_items(main, included_types):
    df = main.snapshot
    modified_df = None

    for included_type in included_types:
        if modified_df is not None:
            df_ = df.loc[df.PartOfSpeech == included_type]
            modified_df = pd.concat([modified_df, df_])
        else:
            modified_df = df.loc[df.PartOfSpeech == included_type]

    return modified_df


def add_new_verbs(main):
    words = get_all_words(ALL_WORDS)
    verbs = words.loc[words.PartOfSpeech == "verb"]
    verb_list = list(verbs.Finnish.values)

    added_verbs = []
    skipped_verbs = []
    for verb_index, verb in enumerate(verb_list):
        # print(f" Checking verbs [{verb_index+1}/{len(verb_list)}]")

        is_in_db = len(main.snapshot.loc[main.snapshot.Infinitive == verb])
        if is_in_db:
            continue

        url = f"https://en.wiktionary.org/wiki/{verb}"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        if not soup.find(attrs={"class": "inflection-table"}):
            skipped_verbs.append(verb)
            continue

        target_tenses = {
            Mood.INDICATIVE: {Tense.PRESENT_TENSE: [POSITIVE, NEGATIVE]},
            Mood.CONDITIONAL: {Tense.PRESENT: [POSITIVE, NEGATIVE]},
        }
        column_index = {
            Tense.PRESENT: {POSITIVE: "1", NEGATIVE: "2"},
            Tense.PAST: {POSITIVE: "1", NEGATIVE: "2"},
            Tense.PERFECT: {POSITIVE: "3", NEGATIVE: "4"},
            Tense.PLUSPERFECT: {POSITIVE: "3", NEGATIVE: "4"},
        }

        for mood, target_tense in target_tenses.items():
            for tense, target_negativity in target_tense.items():

                proper_mood = soup.find(attrs={"title": mood})
                if mood == Mood.INDICATIVE:
                    proper_tense = proper_mood.find_next(attrs={"title": tense})
                else:
                    proper_tense = proper_mood.find_next("th", text="present\n")
                verb_forms_all = proper_tense.find_all_next("td")[0:24]

                for negativity in target_negativity:
                    tense = Tense.PRESENT if tense == Tense.PRESENT_TENSE else tense
                    index = column_index[tense][negativity]

                    verb_forms = [
                        verb_form.text.strip("\n")
                        for verb_form in verb_forms_all
                        if verb_form.attrs["data-accel-col"] == index
                    ]

                    english = verbs.loc[verbs.Finnish == verb, "English"].item()
                    save_verb_forms(verb_forms, tense, verb, negativity, mood, english)
                    added_verbs.append(verb)

    if added_verbs:
        df = get_all_words(ALL_VERBS)
        df.to_excel(ALL_VERBS, index=False)


def evaluate_answer(main):
    actual_split = main.answer.split()
    expected_split = main.item.finnish.split()
    df = main.snapshot
    score_delta = []

    # TODO ! Если len(actual_split) != expected_split
    for index, (actual, expected) in enumerate(zip(actual_split, expected_split)):
        english = main.item.pattern[index][ENGLISH]
        found_word = df.loc[(df.Finnish == actual) & (df.English == english)]
        if len(found_word) == 1:
            score_delta.append(1)
        elif len(found_word) == 0:
            score_delta.append(-1)
        else:
            raise Exception("\n[ERROR] Something is terribly wrong")

    return score_delta


def get_item(main):
    item = main.item_object(main.items_per_run)
    item.pattern = (
        {i: {"type": e} for i, e in enumerate(main.include)} if main.include else None
    )

    return item
