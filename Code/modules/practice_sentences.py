import random

from Code.constants import Statistics, Settings, ALL_WORDS_SENTENCES, PART_OF_SPEECH
from Code.db_functions import get_all_words, export_constructions
from Code.grammar_functions import get_all_constructions
from Code.ui_functions import show_title_head, show_run_statistics


class PracticeSentences:
    def __init__(self, sentences_per_run):
        self.sentences_per_run = sentences_per_run
        self.stats = {Statistics.CORRECT: 0, Statistics.INCORRECT: 0}
        self.all_words = get_all_words(ALL_WORDS_SENTENCES, sort_by=PART_OF_SPEECH)
        self.constructions = get_all_constructions()
        export_constructions(self.constructions)
        self.run()

    def run(self):
        for index in range(1, self.sentences_per_run + 1):
            self.show_statistics(index)
            sentence = self.choose_a_sentence()
            self.display_the_sentence(sentence)
            self.get_user_answer()
            self.evaluate_the_answer()

    def show_statistics(self, index):
        show_title_head(index, self.sentences_per_run, "SENTENCE", user_tips=False)
        show_run_statistics(self.stats, Settings.SENTENCES_PER_RUN)

    def choose_a_sentence(self):
        return random.choice(self.constructions)

    def display_the_sentence(self, sentence):
        print(sentence)

    def get_user_answer(self):
        a = 1

    def evaluate_the_answer(self):
        pass
