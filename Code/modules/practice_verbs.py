from Code.ItemTypeClasses import VerbForm
from Code.constants import ALL_VERBS
from Code.modules.practice_abstract import PracticeAbstract


class PracticeVerbs(PracticeAbstract):
    def __init__(self, verbs_per_run):
        super(PracticeVerbs, self).__init__(verbs_per_run, VerbForm, ALL_VERBS)
