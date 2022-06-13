import requests
from bs4 import BeautifulSoup

from Code.DataClasses import VerbForm
from Code.constants import *
from Code.db_functions import get_all_words, save_verb_forms
from Code.functions import get_stats, get_random_item
from Code.ui_functions import show_title_head, show_run_statistics, show_word_tiers, \
    get_answer, create_a_border


class PracticeVerbs:
    def __init__(self, verbs_per_run):
        self.items_per_run = verbs_per_run
        self.snapshot = get_all_words(ALL_VERBS)
        self.stats = get_stats(self.snapshot)
        self.answer = None
        self.incorrect_answers = {}
        self.result = None
        self.index = None
        self.item = VerbForm()

        self.prepare()
        self.run()

    def prepare(self):
        self.check_if_new_verbs_should_be_added()

    def run(self):
        for index in range(1, self.items_per_run + 1):
            self.index = index
            get_random_item(self, ItemType.VERB)

            show_title_head(index, self.items_per_run, ItemType.VERB)
            show_run_statistics(self.stats, Settings.VERBS_PER_RUN)
            show_word_tiers(self.stats)

            # TODO засунуть в get_answer. Переименовать метод
            print(f" {'ENGLISH'.center(31)} | {'FINNISH'.center(31)}")
            print(f"{'-' * 33}+{'-' * 35}")

            answer = get_answer(self, word=False, verb=True)
            create_a_border("=")

            a = 1

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
