from Code.ItemTypeClasses import Word
from Code.constants import ExitCodes, ALL_WORDS
from Code.functions.db import update_item_score
from Code.functions.general import (
    check_answer,
    get_stats,
    get_random_item,
    get_incorrect_answers,
)
from Code.functions.high_level import get_all_words
from Code.functions.ui import (
    create_a_title,
    show_run_statistics,
    show_word_tiers,
    get_answer,
    show_title_head,
    get_user_choice,
    create_a_border,
)
from Code.tables.EndRunActionsTable import EndRunActionsTable
from Code.tables.IncorrectAnswersTable import IncorrectAnswersTable


class PracticeWords:
    def __init__(self, words_per_run):
        self.snapshot = get_all_words(ALL_WORDS)
        self.stats = get_stats(self.snapshot)
        self.answer = None
        self.incorrect_answers = {}
        self.result = None
        self.index = None
        self.item = Word(words_per_run)

        self.set_up()
        self.run()
        self.tear_down()

    def set_up(self):

        pass

    def run(self):
        for index in range(1, self.item.per_run + 1):
            self.index = index
            get_random_item(self)

            show_title_head(self)
            show_run_statistics(self)
            show_word_tiers(self.stats)

            answer = get_answer(self)
            create_a_border("=")

            if answer:
                score_delta = check_answer(self)

                update_item_score(self, score_delta)

                input("""\n Press "Enter" to continue...""")

            else:
                break

    def tear_down(self):
        create_a_title("Your results")
        show_run_statistics(self)

        if self.incorrect_answers:
            incorrect_answers = get_incorrect_answers(self)
            IncorrectAnswersTable(incorrect_answers)

        available_options = EndRunActionsTable(self).available_options
        user_choice = get_user_choice(available_options)

        if user_choice == "0":
            exit()
        else:
            options = {
                "1": ExitCodes.START_THE_APPLICATION,
                "2": ExitCodes.GO_TO_SETTINGS,
                "3": ExitCodes.SHOW_WELCOME_SCREEN,
            }
            self.result = options[user_choice]
            return


if __name__ == "__main__":
    PracticeWords(None)
