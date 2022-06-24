from Code.constants import SCREEN_WIDTH
from Code.tables.Table import Table


class EndRunActionsTable(Table):
    def __init__(self, main):
        super(EndRunActionsTable, self).__init__(
            headers=["What would you like to do next?"],
            headers_centered=True,
            rows=[
                "Start a new run",
                'Go to "Settings"',
                "Go to main menu",
                "Exit the application",
            ],
            custom_index={"Exit the application": 0},
            headers_border_top=False,
            rows_border_bottom="=",
            table_width=SCREEN_WIDTH,
            index_column_width=len(str(len(main.incorrect_answers))),
        )
