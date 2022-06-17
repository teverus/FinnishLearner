from Code.constants import ItemType


class AbstractItem:
    def __init__(self, per_run, item_type):
        self.per_run = per_run
        self.item_type = item_type
        self.finnish = ""
        self.english = ""


class Word(AbstractItem):
    def __init__(self, per_run):
        super(Word, self).__init__(per_run, ItemType.WORD)


class VerbForm(AbstractItem):
    def __init__(self, per_run):
        super(VerbForm, self).__init__(per_run, ItemType.VERB)
