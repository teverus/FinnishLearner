import requests
from bs4 import BeautifulSoup

from Code.constants import Statistics, Settings, ALL_VERBS
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

        for verb in verb_list:
            is_in_db = len(self.verb_forms.loc[self.verb_forms.Infinitive == verb])

            if not is_in_db:
                url = f"https://cooljugator.com/fi/{verb}"
                try:
                    response = requests.get(url).text
                except Exception:
                    raise Exception(f"\n[ERROR] Couldn't open {url}")

                soup = BeautifulSoup(response, "html.parser")

                present_forms = {}
                present_negative_forms = {}
                conditional_forms = {}
                conditional_negative_forms = {}

                forms = {
                    "present{}": present_forms,
                    "present{}_neg": present_negative_forms,
                    "conditional{}": conditional_forms,
                    "conditional{}_neg": conditional_negative_forms,
                }

                for form in forms.keys():
                    for index in range(1, 7):
                        proper_id = form.format(index)

                        search_results = soup.find_all(attrs={"id": proper_id})
                        assert len(search_results) == 1

                        verb = search_results[0].attrs

                        finnish = verb["data-default"]
                        assert finnish != ""

                        english = verb["data-tooltip"]
                        assert english != ""

                        if index == 2:
                            english = english.replace("you", "you (singular)")
                        elif index == 3:
                            english = english.replace("he/she", "s/he/it")
                            english = english.replace("do not", "does not")
                        elif index == 5:
                            english = english.replace("you all", "you (plural)")

                        forms[form][finnish] = english

                [save_verb_forms(verb_forms, verb) for verb_forms in forms.values()]


if __name__ == "__main__":
    PracticeVerbs(None)
