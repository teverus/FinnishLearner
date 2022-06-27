import random

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

from Code.constants import *
from Code.functions.high_level import get_all_words, save_verb_forms
from Code.functions.ui import print_a_message


def get_stats(df: DataFrame) -> dict:
    stats = get_stats_dict()
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


def get_stats_dict() -> dict:
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
        pronoun = f"{ri.Person} {ri.Plural}"
        pronoun = PERSONAL_PRONOUNS[pronoun]
        main.item.english = (
            f"({ri.Mood}|{ri.Tense}|{ri.Negative}) [{ri.Infinitive}] {pronoun} "
        )


def advance_current_tier(main):
    current_tier = main.stats[Statistics.CURRENT_TIER]
    next_tier = [ALL_TIERS[i + 1] for i, t in enumerate(ALL_TIERS) if t == current_tier]
    main.stats[Statistics.CURRENT_TIER] = next_tier[0]


def check_answer(main) -> int:
    answer = main.answer
    expected_answer = main.item.finnish

    if answer == expected_answer:
        target_stats = Statistics.CORRECT
        score_delta = 1

        print(" ")

        print_a_message(
            f"{'-' * 22}<{'CORRECT ANSWER'.center(22)}>{'-' * 23}", border="="
        )

    else:
        main.incorrect_answers[main.index] = {Word.ENGLISH: main.item.english}
        main.incorrect_answers[main.index][Word.FINNISH] = expected_answer
        main.incorrect_answers[main.index][Word.INCORRECT] = answer
        target_stats = Statistics.INCORRECT
        score_delta = -1

        user_answer = f', not "{answer}"' if answer else ""
        print("")
        print_a_message(
            f"""Sorry, it's "{expected_answer}"{user_answer}""",
            border="~",
            centered=True,
        )
        print("")

        make_user_write_type_three_times(main)

    main.stats[target_stats] += 1
    update_current_tier(main)
    remove_current_word_from_snapshot(main)

    return score_delta


def update_current_tier(main):
    major, minor = main.stats[Statistics.CURRENT_TIER]
    tiers = main.stats[Statistics.TIERS]
    tiers[major][minor][Tier.LEFT] -= 1


def make_user_write_type_three_times(main):
    print(f' Please type "{main.item.finnish}" and hit "Enter" three times.')

    correct_times = 0
    max_times = 3
    while correct_times != max_times:
        user_input = input(" >>> ").replace("a:", "ä").replace("o:", "ö")
        if user_input == main.item.finnish:
            correct_times += 1
            if correct_times == max_times:
                print(f" [SUCCESS] That's it :) Keep on learning :)")
            else:
                print(f" [SUCCESS] Yes! {max_times - correct_times} to go!")
        else:
            print(f' [FAILURE] Nope, you need to type "{main.item.finnish}".')


def remove_current_word_from_snapshot(main):
    df = main.snapshot
    index = find_item_in_db(main, df).index.item()

    df.drop(index, inplace=True)


def find_item_in_db(main, df: DataFrame):
    item = None
    word = main.item
    finnish = word.finnish
    english = word.english

    if main.item.item_type == ItemType.WORD:
        item = df.loc[(df.Finnish == finnish) & (df.English == english)]
    elif main.item.item_type == ItemType.VERB:
        item = df.loc[df["Verb form"] == main.item.finnish]

    if len(item):
        return item
    else:
        raise Exception("\n[ERROR] Couldn't find an item in db")


def get_incorrect_answers(main):
    incorrect_answers = []

    for key, value in main.incorrect_answers.items():
        if main.item.item_type == ItemType.VERB:
            verb, correct, incorrect = main.incorrect_answers[key].values()
            verb = verb.split("[")[0].strip().strip("(").strip(")")
            result = [verb, correct, incorrect]
        elif main.item.item_type == ItemType.WORD:
            result = list(main.incorrect_answers[key].values())
        else:
            raise Exception("\n[ERROR] Unknown item_type")

        incorrect_answers.append(result)

    return incorrect_answers


def check_if_new_items_should_be_added(main):
    if main.item.item_type == ItemType.VERB:
        # TODO добавить добавление англ
        add_new_verbs(main)


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
