from Code.constants import SCREEN_WIDTH
from Code.tables.Table import Table


class IncorrectAnswersTable(Table):
    def __init__(self, incorrect_answers):
        super(IncorrectAnswersTable, self).__init__(
            headers=["English", "Correct", "Incorrect"],
            headers_upper=True,
            headers_centered=True,
            rows=incorrect_answers,
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            headers_border_top=False,
            rows_border_bottom="=",
        )
