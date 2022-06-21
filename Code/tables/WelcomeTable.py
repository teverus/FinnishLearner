from Code.constants import WELCOME_MESSAGE, SCREEN_WIDTH
from Code.tables.Table import Table


class WelcomeTable(Table):
    def __init__(self, main):
        options = []
        for v in main.values():
            if isinstance(v[0], str):
                if len(v) >= 3:
                    options.append([v[0], v[2]])
                else:
                    options.append([v[0]])

        super(WelcomeTable, self).__init__(
            table_title=WELCOME_MESSAGE,
            headers=["Option", "Items to practice"],
            headers_centered=True,
            rows=options,
            custom_index={"Exit": 0},
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            border_headers_top="=",
            border_rows_bottom="=",
        )
