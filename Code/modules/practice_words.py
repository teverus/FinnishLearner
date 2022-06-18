from Code.ItemTypeClasses import Word
from Code.constants import SCREEN_WIDTH, ExitCodes, ItemType
from Code.functions.db import get_all_words, update_item_score
from Code.functions.general import check_answer, get_stats, get_random_item
from Code.tables.Table import Table
from Code.functions.ui import (
    create_a_title,
    show_run_statistics,
    show_word_tiers,
    get_answer,
    show_title_head,
    get_user_choice,
    create_a_border,
)


class PracticeWords:
    def __init__(self, words_per_run):
        self.snapshot = get_all_words()
        self.stats = get_stats(self.snapshot)
        self.answer = None
        self.incorrect_answers = {}
        self.result = None
        self.index = None
        self.item = Word(words_per_run)

        self.set_up()
        self.run()

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

        self.show_results()

        available_options = Table(
            headers=["What would you like to do next?"],
            headers_centered=True,
            rows=[
                "Start a new run",
                'Go to "Settings"',
                "Go to main menu",
                "Exit the application",
            ],
            custom_index={"Exit the application": 0},
            border_headers_top=False,
            border_rows_bottom="=",
            table_width=SCREEN_WIDTH,
            index_column_width=len(str(len(self.incorrect_answers))),
        ).available_options
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

    def show_results(self):
        create_a_title("Your results")
        show_run_statistics(self)

        if self.incorrect_answers:
            incorrect_answers = []

            for key, value in self.incorrect_answers.items():
                if self.item.item_type == ItemType.VERB:
                    verb, correct, incorrect = self.incorrect_answers[key].values()
                    verb = verb.split("[")[0].strip().strip("(").strip(")")
                    result = [verb, correct, incorrect]
                else:
                    result = list(self.incorrect_answers[key].values())

                incorrect_answers.append(result)


            Table(
                headers=["English", "Correct", "Incorrect"],
                headers_upper=True,
                headers_centered=True,
                rows=incorrect_answers,
                rows_centered=True,
                table_width=SCREEN_WIDTH,
                border_headers_top=False,
                border_rows_bottom="=",
            )


if __name__ == "__main__":
    PracticeWords(None)
