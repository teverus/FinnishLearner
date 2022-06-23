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
        self.result = None
        self.run()

    def run(self):
        clear_console()
        available_options = SettingsTable().available_options

        # TODO создавать словарь, где первые ключи - по числу настроек в файле settings
        mode = {
            "1": self.change_setting,
            "2": self.change_setting,
            "3": self.change_setting,
            "4": self.reset_scores,
        }

        while True:
            user_choice = get_user_choice(available_options)
            if user_choice == "0":
                exit()
            elif user_choice == "00":
                self.result = ExitCodes.SHOW_WELCOME_SCREEN
                return
            else:
                mode[user_choice](user_choice)

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
        # TODO возможность сбрасывать и счет глаголов
        df = get_all_words(ALL_WORDS)
        df.loc[:, SCORE] = 0
        df.to_excel(ALL_WORDS, index=False)

        print(" ")
        print_a_message("Scores were set to zero", centered=True, border="=")


if __name__ == "__main__":
    ChangeSettings()
