from Code.constants import WELCOME_MESSAGE, SCREEN_WIDTH
from Code.tables.Table import Table


class WelcomeTable(Table):
    def __init__(self, main):
        super(WelcomeTable, self).__init__(
            table_title=WELCOME_MESSAGE,
            headers=["Option", "Words/sentences to practice"],
            headers_centered=True,
            rows=[
                ["Practice words", main.words_per_run],
                ["Practice verbs", main.verbs_per_run],
                ["Practice sentences", main.sentences_per_run],
                ["Settings"],
                ["Exit"],
            ],
            custom_index={"Exit": 0},
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            border_headers_top="=",
            border_rows_bottom="=",
        )
