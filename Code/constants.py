from configparser import ConfigParser

# SCREEN_WIDTH = 69
SCREEN_WIDTH = 100
WELCOME_MESSAGE = "Welcome to Finnish Learner"
SETTINGS_FILE = "settings.ini"
SETTINGS = "settings"

WHITE_BLOCK_FULL = "\u2588"
WHITE_BLOCK_UPPER = "\u2501"
LIGHT_SHADOW = "\u2591"
DOT = "\u00b7"

TITLE = "[ Word {} of {} ]"
USER_TIPS = """If you can't remember the correct answer, press the "Enter" key"""
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
    "Mood",
    "Tense",
    "Negative",
    "Person",
    "Plural",
    "Score",
    "Infinitive",
    "English"
]


item_type_to_excel_file = {"words": ALL_WORDS, "verbs": ALL_VERBS}


class Settings:
    WORDS_PER_RUN = "words per run"
    VERBS_PER_RUN = "verbs per run"
    WORD_COMBINATIONS_PER_RUN = "word combinations per run"


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

POSITIVE = "positive"
NEGATIVE = "negative"


class Mood:
    INDICATIVE = "indicative mood"
    CONDITIONAL = "conditional mood"


class Tense:
    PRESENT_TENSE = "present tense"
    PRESENT = "present"
    PAST = "past"
    PERFECT = "perfect"
    PLUSPERFECT = "plusperfect"


class ItemType:
    WORD = "WORD"
    VERB = "VERB"


PERSONAL_PRONOUNS = {
    "1 Singular": "minä",
    "2 Singular": "sinä",
    "3 Singular": "hän",
    "1 Plural": "me",
    "2 Plural": "te",
    "3 Plural": "he",
}
