from Code.constants import Statistics, Settings
from Code.ui_functions import show_title_head, show_run_statistics


class PracticeSentences:
    def __init__(self, sentences_per_run):
        self.sentences_per_run = sentences_per_run
        self.stats = {Statistics.CORRECT: 0, Statistics.INCORRECT: 0}

        self.run()

    def run(self):
        for index in range(1, self.sentences_per_run + 1):
            show_title_head(index, self.sentences_per_run, "SENTENCE", user_tips=False)
            show_run_statistics(self.stats, Settings.SENTENCES_PER_RUN)
            a = 1
