from Code.constants import *
from Code.db_functions import get_all_words
from Code.table import Table
from Code.ui_functions import (
    get_user_choice,
    print_a_message,
    clear_console,
)


class ChangeSettings:
    def __init__(self, _):
        self.result = None
        self.run()

    def run(self):
        clear_console()
        available_options = Table(
            headers=["Name", "Value"],
            rows=[[key.capitalize(), value] for key, value in CONFIG.items()]
            + ["Exit the application", "Go back"],
            custom_index={"Exit the application": 0, "Go back": "00"},
            headers_centered=True,
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            table_title="Settings",
            border_headers_top="=",
            border_rows_bottom="=",
        ).available_options

        options = {"1": self.change_setting, "2": self.reset_scores}

        while True:
            user_choice = get_user_choice(available_options)
            if user_choice == "0":
                exit()
            elif user_choice == "00":
                self.result = ExitCodes.SHOW_WELCOME_SCREEN
                return
            else:
                options[user_choice](user_choice)

    @staticmethod
    def change_setting(user_choice):
        setting = list(CONFIG.keys())[int(user_choice) - 1]
        new_value = input(f' New value for "{setting.capitalize()}": ').strip()

        CONFIG_PARSER[SETTINGS][setting] = new_value
        with open(SETTINGS_FILE, "w") as config_file:
            CONFIG_PARSER.write(config_file)

        CONFIG[setting] = new_value

        print(" ")
        print_a_message(
            f'New value for "{setting.capitalize()}" has been saved',
            centered=True,
            border="=",
        )

    @staticmethod
    def reset_scores(_):
        df = get_all_words()
        df.loc[:, SCORE] = 0
        df.to_excel(ALL_WORDS, index=False)

        print(" ")
        print_a_message("Scores were set to zero", centered=True, border="=")


if __name__ == "__main__":
    ChangeSettings(None)
