from Code.TeverusSDK.CLI_tools.table import Table
from Code.constants import CONFIG, Settings, WELCOME_MESSAGE, SCREEN_WIDTH
from Code.modules.change_settings import ChangeSettings
from Code.modules.start_application import StartARun
from Code.ui_functions import (
    get_user_choice,
    clear_console,
)


class FinnishWordsLearner:
    def __init__(self):
        super(FinnishWordsLearner, self).__init__()

        self.words_per_run = int(CONFIG[Settings.WORDS_PER_RUN])

        self.options = {
            "1": StartARun,
            "2": ChangeSettings,
            "0": exit,
            "00": self.show_welcome_screen,
        }

        choice = self.show_welcome_screen()

        while True:
            self.words_per_run = int(CONFIG[Settings.WORDS_PER_RUN])
            choice = self.options[choice]() if choice in ["0", "00"] else choice

            module = self.options[choice](self.words_per_run)
            choice = module.result

    def show_welcome_screen(self):
        clear_console()
        available_options = Table(
            table_title=WELCOME_MESSAGE,
            headers=["Option", "Words to practice"],
            headers_centered=True,
            rows=[["Start a run", self.words_per_run], ["Settings"], ["Exit"]],
            custom_index={"Exit": 0},
            rows_centered=True,
            table_width=SCREEN_WIDTH,
            border_headers_top="=",
            border_rows_bottom="=",
        ).available_options

        user_choice = get_user_choice(available_options)

        return user_choice


if __name__ == "__main__":
    FinnishWordsLearner()
