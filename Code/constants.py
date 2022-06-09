from configparser import ConfigParser

SCREEN_WIDTH = 69
WELCOME_MESSAGE = "Welcome to Finnish Learner"
SETTINGS_FILE = "settings.ini"
SETTINGS = "settings"

WHITE_BLOCK_FULL = "\u2588"
WHITE_BLOCK_UPPER = "\u2501"
LIGHT_SHADOW = "\u2591"
DOT = "\u00b7"

TITLE = "[ Word {} of {} ]"
USER_TIPS = """If you can't remember a specific word, just press "Enter" key"""
TRANSFORMATION = """a: -> ä | o: -> ö | q -> end run | r -> start a new run"""

ALL_WORDS = "all_words.xlsx"
ALL_WORDS_SENTENCES = "all_words_sentences.xlsx"
ALL_CONSTRUCTIONS = "all_constructions.xlsx"
ALL_VERBS = "all_verbs.xlsx"

SCORE = "Score"
COUNT = "Count"
PART_OF_SPEECH = "PartOfSpeech"

VERB_FORMS = [
    "Verb form",
    "Tense",
    "Negative",
    "Person",
    "Plural",
    "Score",
    "Infinitive",
]


class Settings:
    WORDS_PER_RUN = "words per run"
    SENTENCES_PER_RUN = "sentences per run"
    VERBS_PER_RUN = "verbs per run"


class Statistics:
    CORRECT = "Correct"
    INCORRECT = "Incorrect"
    TIERS = "Tiers"
    CURRENT_TIER = "Current tier"


class Tier:
    BEGINNER = "Beginner"
    PRE_INTERMEDIATE = "Pre-Intermediate"
    INTERMEDIATE = "Intermediate"
    UPPER_INTERMEDIATE = "Upper-Intermediate"
    ADVANCED = "Advanced"
    ALL_TIERS = [BEGINNER, PRE_INTERMEDIATE, INTERMEDIATE, UPPER_INTERMEDIATE, ADVANCED]
    MAX_LENGTH = max([len(_) for _ in ALL_TIERS])

    LOWER = "Lower"
    MIDDLE = "Middle"
    UPPER = "Upper"
    ALL_LEVELS = [LOWER, MIDDLE, UPPER]

    TOTAL = "Total"
    LEFT = "Left"


class ExitCodes:
    SHOW_WELCOME_SCREEN = "00"
    START_THE_APPLICATION = "1"
    GO_TO_SETTINGS = "4"


class Word:
    ENGLISH = "English"
    FINNISH = "Finnish"
    INCORRECT = "Incorrect"


SCORE_TO_TIER = {}
i = 0
for tier in Tier.ALL_TIERS:
    for level in Tier.ALL_LEVELS:
        SCORE_TO_TIER[i] = [tier, level]
        i += 1

ALL_TIERS = list(SCORE_TO_TIER.values())

config = ConfigParser()
config.read(SETTINGS_FILE)

CONFIG_PARSER = config
CONFIG = config[SETTINGS]
