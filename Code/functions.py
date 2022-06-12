import logging
import os
import random

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Code.constants import *
from Code.ui_functions import print_a_message


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
        words_on_this_tier = df.loc[df.Score <= max_score]
    elif max_score == 15:
        words_on_this_tier = df.loc[df.Score >= max_score]
    else:
        words_on_this_tier = df.loc[df.Score == max_score]

    if len(words_on_this_tier) == 0:
        return False

    elif len(words_on_this_tier.groupby(SCORE)) != 1:
        available_groups = list(words_on_this_tier.groupby(SCORE).groups.keys())
        for group in available_groups:
            words_on_this_tier = df.loc[df.Score == group]
            break

    random_number = random.randint(0, len(words_on_this_tier) - 1)
    random_word = words_on_this_tier.iloc[random_number]

    # TODO разное поведение для word и verb
    main.item.finnish = random_word.Finnish
    main.item.english = random_word.English


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
    word = main.item
    finnish = word.finnish
    english = word.english

    index = df.loc[(df.Finnish == finnish) & (df.English == english)].index.item()

    df.drop(index, inplace=True)


def driver():
    """Creates an instance of a driver that will be used in the tests"""

    # Make WebDriver save a driver executable in the root directory of the project
    os.environ["WDM_LOCAL"] = "1"

    # Turn on logging in the console
    logging.getLogger("WDM").setLevel(logging.NOTSET)
    os.environ["WDM_LOG"] = "false"

    # Start a driver with the desired options
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1080")  # Must match virtual display size
    options.add_argument("--lang=en")  # Controls browser's UI language
    options.add_argument("--disable-gpu")  # Best for console chrome
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")

    # Remove Chrome browser debugging info from the console (cosmetics only)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    return driver
