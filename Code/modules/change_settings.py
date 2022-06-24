from Code.constants import *
from Code.functions.high_level import get_all_words
from Code.functions.ui import (
    get_user_choice,
    print_a_message,
    clear_console,
)
from Code.tables.SettingsTable import SettingsTable


class ChangeSettings:
    def __init__(self):
        self.options = self.get_options()
        self.result = None
        self.run()

    def run(self):
        clear_console()
        available_options = SettingsTable().available_options

        while True:
            user_choice = get_user_choice(available_options)
            if user_choice == "0":
                exit()
            elif user_choice == "00":
                self.result = ExitCodes.SHOW_WELCOME_SCREEN
                return
            else:
                self.options[user_choice](user_choice)

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
    def reset_scores(user_choice):
        available_options = list(CONFIG.keys())
        proper_index = int(user_choice) - len(available_options)
        proper_option = available_options[proper_index - 1].split()[0]
        proper_file = item_type_to_excel_file[proper_option]

        df = get_all_words(proper_file)
        df.loc[:, SCORE] = 0
        df.to_excel(proper_file, index=False)

        print(" ")
        print_a_message(
            f"{proper_option.capitalize()} scores were set to zero",
            centered=True,
            border="=",
        )

    def get_options(self):
        number = len(CONFIG.keys())
        change = {str(i + 1): self.change_setting for i in range(number)}
        reset = {str(i + 1 + number): self.reset_scores for i in range(number)}
        reset_all = {str((number * 2) + 1): self.reset_scores}

        return {**change, **reset, **reset_all}
