from Code.ItemTypeClasses import WordCombination
from Code.constants import ALL_WORDS
from Code.modules.practice_abstract import PracticeAbstract


class PracticeWordCombinations(PracticeAbstract):
    def __init__(self, combinations_per_run):
        super(PracticeWordCombinations, self).__init__(
            combinations_per_run,
            WordCombination,
            ALL_WORDS,
            include=["adjective", "noun"],
            simple_stats=True
        )
