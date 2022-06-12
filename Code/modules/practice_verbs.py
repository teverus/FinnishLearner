import requests
from bs4 import BeautifulSoup

from Code.constants import Statistics, Settings, ALL_VERBS, Mood, Tense, POSITIVE, \
    NEGATIVE
from Code.db_functions import get_all_words, save_verb_forms
from Code.ui_functions import show_title_head, show_run_statistics


class PracticeVerbs:
    def __init__(self, verbs_per_run):
        self.verbs_per_run = verbs_per_run
        self.stats = {Statistics.CORRECT: 0, Statistics.INCORRECT: 0}
        self.verb_forms = get_all_words(ALL_VERBS)

        self.check_if_new_verbs_were_added()

        for index in range(1, self.verbs_per_run + 1):
            self.show_statistics(index)
            a = 1

    def show_statistics(self, index):
        show_title_head(index, self.verbs_per_run, "VERB", user_tips=False)
        show_run_statistics(self.stats, Settings.VERBS_PER_RUN)

    def check_if_new_verbs_were_added(self):
        words = get_all_words()
        verbs = words.loc[words.PartOfSpeech == "verb"]
        verb_list = list(verbs.Finnish.values)

        skipped_verbs = []
        for verb_index, verb in enumerate(verb_list):

            is_in_db = len(self.verb_forms.loc[self.verb_forms.Infinitive == verb])
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

                        save_verb_forms(verb_forms, tense, verb, negativity)

        # if skipped_verbs:
        #     print(f"These verbs were skipped:\n{skipped_verbs}")


if __name__ == "__main__":
    PracticeVerbs(None)
