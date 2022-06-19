from Code.ItemTypeClasses import Word
from Code.constants import ALL_WORDS
from Code.modules.practice_abstract import PracticeAbstract


class PracticeWords(PracticeAbstract):
    def __init__(self, words_per_run):
        super(PracticeWords, self).__init__(words_per_run, Word, ALL_WORDS)
