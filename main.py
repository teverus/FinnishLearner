from Code.constants import CONFIG, Settings
from Code.functions.ui import (
    get_user_choice,
    clear_console,
)
from Code.modules.change_settings import ChangeSettings
from Code.modules.practice_verbs import PracticeVerbs
from Code.modules.practice_word_combinations import PracticeWordCombinations
from Code.modules.practice_words import PracticeWords

# noinspection PyAttributeOutsideInit
from Code.tables.WelcomeTable import WelcomeTable


class FinnishWordsLearner:
    def __init__(self):
        super(FinnishWordsLearner, self).__init__()

        choice = self.show_welcome_screen()

        while True:
            options = self.get_options()
            selected = options[choice]

            if len(selected) == 1:
                choice = selected[0]()
            elif len(selected) == 2:
                choice = selected[1]().result
            elif len(selected) == 3:
                choice = selected[1](selected[2]).result

    def get_options(self):
        # [function]
        # ["Display name", function]
        # ["Display name", function, arguments]
        return {
            "1": ["Practice words", PracticeWords, int(CONFIG[Settings.WORDS_PER_RUN])],
            "2": ["Practice verbs", PracticeVerbs, int(CONFIG[Settings.VERBS_PER_RUN])],
            "3": [
                "Practice word combinations",
                PracticeWordCombinations,
                int(CONFIG[Settings.WORD_COMBINATIONS_PER_RUN]),
            ],
            "4": ["Settings", ChangeSettings],
            "0": ["Exit", exit],
            "00": [self.show_welcome_screen],
        }

    def show_welcome_screen(self):
        clear_console()
        options = self.get_options()
        available_options = WelcomeTable(options).available_options
        user_choice = get_user_choice(available_options)

        return user_choice


if __name__ == "__main__":
    FinnishWordsLearner()
