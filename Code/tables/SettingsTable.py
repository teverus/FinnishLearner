from Code.constants import CONFIG, SCREEN_WIDTH
from Code.tables.Table import Table


class SettingsTable(Table):
    def __init__(self):
        settings_and_values = [[k.capitalize(), v] for k, v in CONFIG.items()]
        score_type = [f"Reset {k.split(' per run')[0]}" for k in CONFIG.keys()]
        super(SettingsTable, self).__init__(
            headers=["Name", "Value"],
            rows=settings_and_values
            + score_type
            + ["Reset all scores", "Exit the application", "Go back"],
            custom_index={"Exit the application": 0, "Go back": "00"},
            headers_centered=True,
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            table_title="Settings",
            headers_border_top="=",
            rows_border_bottom="=",
        )
