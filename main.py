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
class FinnishWordsLearner:
    def __init__(self):
        super(FinnishWordsLearner, self).__init__()

        self.get_values_per_run()

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
            self.stats = self.get_values_per_run()

            choice = self.options[choice]() if choice in ["0", "00"] else choice
            module = self.options[choice](self.stats[choice])
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
        available_options = Table(
            table_title=WELCOME_MESSAGE,
            headers=["Option", "Words/sentences to practice"],
            headers_centered=True,
            rows=[
                ["Practice words", self.words_per_run],
                ["Practice verbs", self.verbs_per_run],
                ["Practice sentences", self.sentences_per_run],
                ["Settings"],
                ["Exit"],
            ],
            custom_index={"Exit": 0},
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            border_headers_top="=",
            border_rows_bottom="=",
        ).available_options

        user_choice = get_user_choice(available_options)

        return user_choice


if __name__ == "__main__":
    FinnishWordsLearner()
