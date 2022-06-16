import requests
from bs4 import BeautifulSoup

from Code.DataClasses import VerbForm
from Code.Table import Table
from Code.constants import *
from Code.db_functions import get_all_words, save_verb_forms, update_item_score
from Code.functions import get_stats, get_random_item, check_answer
from Code.ui_functions import (
    show_title_head,
    show_run_statistics,
    show_word_tiers,
    get_answer,
    create_a_border,
    create_a_title, get_user_choice,
)


class PracticeVerbs:
    def __init__(self, verbs_per_run):
        self.snapshot = get_all_words(ALL_VERBS)
        self.stats = get_stats(self.snapshot)
        self.answer = None
        self.incorrect_answers = {}
        self.result = None
        self.index = None
        self.item = VerbForm(verbs_per_run)

        self.prepare()
        self.run()

    def prepare(self):
        self.check_if_new_verbs_should_be_added()

    def run(self):
        for index in range(1, self.item.per_run + 1):
            self.index = index
            get_random_item(self)

            show_title_head(self)
            show_run_statistics(self)
            show_word_tiers(self.stats)

            answer = get_answer(self, word=False, verb=True)
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
            incorrect_answers = [
                list(self.incorrect_answers[key].values())
                for key, value in self.incorrect_answers.items()
            ]

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

    def check_if_new_verbs_should_be_added(self):
        words = get_all_words()
        verbs = words.loc[words.PartOfSpeech == "verb"]
        verb_list = list(verbs.Finnish.values)

        added_verbs = []
        skipped_verbs = []
        for verb_index, verb in enumerate(verb_list):
            # print(f" Checking verbs [{verb_index+1}/{len(verb_list)}]")

            is_in_db = len(self.snapshot.loc[self.snapshot.Infinitive == verb])
            if is_in_db:
                continue

            url = f"https://en.wiktionary.org/wiki/{verb}"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            if not soup.find(attrs={"class": "inflection-table"}):
                skipped_verbs.append(verb)
                continue

            target_tenses = {
                Mood.INDICATIVE: {Tense.PRESENT_TENSE: [POSITIVE, NEGATIVE]},
                Mood.CONDITIONAL: {Tense.PRESENT: [POSITIVE, NEGATIVE]},
            }
            column_index = {
                Tense.PRESENT: {POSITIVE: "1", NEGATIVE: "2"},
                Tense.PAST: {POSITIVE: "1", NEGATIVE: "2"},
                Tense.PERFECT: {POSITIVE: "3", NEGATIVE: "4"},
                Tense.PLUSPERFECT: {POSITIVE: "3", NEGATIVE: "4"},
            }

            for mood, target_tense in target_tenses.items():
                for tense, target_negativity in target_tense.items():

                    proper_mood = soup.find(attrs={"title": mood})
                    if mood == Mood.INDICATIVE:
                        proper_tense = proper_mood.find_next(attrs={"title": tense})
                    else:
                        proper_tense = proper_mood.find_next("th", text="present\n")
                    verb_forms_all = proper_tense.find_all_next("td")[0:24]

                    for negativity in target_negativity:
                        tense = Tense.PRESENT if tense == Tense.PRESENT_TENSE else tense
                        index = column_index[tense][negativity]

                        verb_forms = [
                            verb_form.text.strip("\n")
                            for verb_form in verb_forms_all
                            if verb_form.attrs["data-accel-col"] == index
                        ]

                        save_verb_forms(verb_forms, tense, verb, negativity, mood)
                        added_verbs.append(verb)

        if added_verbs:
            df = get_all_words(ALL_VERBS)
            df.to_excel(ALL_VERBS, index=False)


if __name__ == "__main__":
    PracticeVerbs(None)
