from Code.modules.practice_sentences import PracticeSentences
from Code.tables.Table import Table
from Code.constants import CONFIG, Settings, WELCOME_MESSAGE, SCREEN_WIDTH
from Code.modules.change_settings import ChangeSettings
from Code.modules.practice_verbs import PracticeVerbs
from Code.modules.practice_words import PracticeWords
from Code.functions.ui import (
    get_user_choice,
    clear_console,
)


# noinspection PyAttributeOutsideInit
from Code.tables.WelcomeTable import WelcomeTable


class FinnishWordsLearner:
    def __init__(self):
        super(FinnishWordsLearner, self).__init__()

        self.options = {
            "1": PracticeWords,
            "2": PracticeVerbs,
            "3": PracticeSentences,
            "4": ChangeSettings,
            "0": exit,
            "00": self.show_welcome_screen,
        }

        choice = self.show_welcome_screen()

        while True:
            self.values_per_run = self.get_values_per_run()

            choice = self.options[choice]() if choice in ["0", "00"] else choice
            module = self.options[choice](self.values_per_run[choice])
            choice = module.result

    def get_values_per_run(self):
        self.words_per_run = int(CONFIG[Settings.WORDS_PER_RUN])
        self.verbs_per_run = int(CONFIG[Settings.VERBS_PER_RUN])
        self.sentences_per_run = int(CONFIG[Settings.SENTENCES_PER_RUN])

        return {
            "1": self.words_per_run,
            "2": self.verbs_per_run,
            "3": self.sentences_per_run,
            "4": None,
        }

    def show_welcome_screen(self):
        clear_console()
        self.get_values_per_run()
        available_options = WelcomeTable(self).available_options

        user_choice = get_user_choice(available_options)

        return user_choice


if __name__ == "__main__":
    FinnishWordsLearner()
