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
SCORE = "Score"
COUNT = "Count"


class Settings:
    WORDS_PER_RUN = "words per run"


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
    GO_TO_SETTINGS = "2"


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
