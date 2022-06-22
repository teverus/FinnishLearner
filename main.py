from Code.constants import CONFIG, Settings
from Code.functions.ui import (
    get_user_choice,
    clear_console,
)
from Code.modules.change_settings import ChangeSettings
from Code.modules.practice_sentences import PracticeSentences
from Code.modules.practice_verbs import PracticeVerbs
from Code.modules.practice_words import PracticeWords

# noinspection PyAttributeOutsideInit
from Code.tables.WelcomeTable import WelcomeTable


class FinnishWordsLearner:
    def __init__(self):
        super(FinnishWordsLearner, self).__init__()

        choice = self.show_welcome_screen()

        while True:
            opts = self.get_options()
            function = opts[choice][1] if len(opts[choice]) >= 2 else opts[choice][0]
            arguments = opts[choice][2] if len(opts[choice]) >= 3 else None

            if choice in ["0", "00"]:
                choice = function()
            elif choice == "4":
                choice = function().result
            else:
                choice = function(arguments).result

    def get_options(self):
        return {
            "1": ["Practice words", PracticeWords, int(CONFIG[Settings.WORDS_PER_RUN])],
            "2": ["Practice verbs", PracticeVerbs, int(CONFIG[Settings.VERBS_PER_RUN])],
            "3": [
                "Practice sentences",
                PracticeSentences,
                int(CONFIG[Settings.SENTENCES_PER_RUN]),
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
