from Code.constants import CONFIG, SCREEN_WIDTH
from Code.tables.Table import Table


class SettingsTable(Table):
    def __init__(self):
        super(SettingsTable, self).__init__(
            headers=["Name", "Value"],
            rows=[[key.capitalize(), value] for key, value in CONFIG.items()]
            # TODO получать слово для частичного сбрасывания счета
            + ["Reset all scores", "Exit the application", "Go back"],
            custom_index={"Exit the application": 0, "Go back": "00"},
            headers_centered=True,
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            table_title="Settings",
            border_headers_top="=",
            border_rows_bottom="=",
        )
