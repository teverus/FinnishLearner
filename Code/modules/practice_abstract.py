from Code.constants import ExitCodes
from Code.functions.db import update_item_score_in_db
from Code.functions.general import (
    get_stats,
    check_if_new_items_should_be_added,
    get_random_item,
    check_answer,
    get_incorrect_answers,
    exclude_item_types,
    include_only_items, get_item,
)
from Code.functions.high_level import get_all_words
from Code.functions.ui import (
    show_title_head,
    show_run_statistics,
    show_word_tiers,
    get_answer,
    create_a_border,
    create_a_title,
    get_user_choice,
)
from Code.tables.EndRunActionsTable import EndRunActionsTable
from Code.tables.IncorrectAnswersTable import IncorrectAnswersTable


# TODO можно добавлять артикль


class PracticeAbstract:
    def __init__(
        self,
        items_per_run,
        item_object,
        target_file,
        horizontal_prompt=False,
        exclude=False,
        include=False,
        simple_stats=False,
    ):
        self.snapshot = get_all_words(target_file)
        self.snapshot = exclude_item_types(self, exclude) if exclude else self.snapshot
        self.snapshot = include_only_items(self, include) if include else self.snapshot
        self.stats = get_stats(self.snapshot, simple_stats)
        self.answer = None
        self.incorrect_answers = {}
        self.result = None
        self.index = None
        self.item_object = item_object
        self.items_per_run = items_per_run
        self.include = include
        self.item = get_item(self)
        self.horizontal_prompt = horizontal_prompt

        self.set_up()
        self.run()
        self.tear_down()

    def set_up(self):
        check_if_new_items_should_be_added(self)

    def run(self):
        for index in range(1, self.item.per_run + 1):
            self.item = get_item(self)

            self.index = index
            get_random_item(self)

            show_title_head(self)
            show_run_statistics(self)
            show_word_tiers(self.stats)

            answer = get_answer(self)
            create_a_border("=")

            if answer:
                score_delta = check_answer(self)
                update_item_score_in_db(self, score_delta)
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
