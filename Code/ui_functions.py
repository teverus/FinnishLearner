import os
from typing import Union, List

from tabulate import tabulate

from Code.constants import *


def do_nothing():
    pass


def clear_console():
    os.system("cls")


def print_a_message(
    message: Union[str, list],
    centered: bool = False,
    upper: bool = False,
    clear_screen: bool = False,
    border: str = "-",
):
    clear_console() if clear_screen else do_nothing()

    print(f"{border * SCREEN_WIDTH}") if border else do_nothing()

    message = [message] if not isinstance(message, list) else message

    for index, element in enumerate(message):
        if "\n" in element:
            del message[index]
            new_index = index
            new_elements = element.split("\n")
            for new_element in new_elements:
                message.insert(new_index, new_element)
                new_index += 1

    for line in message:
        line = line.upper() if upper else line
        line = line.center(SCREEN_WIDTH) if centered else line
        print(line)

    print(f"{border * SCREEN_WIDTH}") if border else do_nothing()


def create_a_title(text: Union[str, list], upper=True):
    print_a_message(text, centered=True, upper=upper, clear_screen=True, border="=")


def create_a_border(symbol: str = "-"):
    print(f"{symbol * SCREEN_WIDTH}")


def show_options(options: list, title: str = None, last_is_zero: bool = False) -> int:
    available_options = []

    if title:
        print(title)

    for index, element in enumerate(options, 1):
        index = 0 if last_is_zero and index == len(options) else index
        print(f" {index} - {element}")
        available_options.append(str(index))

    user_choice = get_user_choice(available_options)

    return user_choice


def get_user_choice(available_options: List[str]) -> str:
    user_choice = input("\n Please, enter your choice: ")

    while user_choice not in available_options:
        guidelines = ", ".join(available_options)
        print(f" [WARNING] You must enter one of these values: {guidelines}")
        user_choice = input("\n Please, enter your choice: ")

    return user_choice


def show_run_statistics(stats: dict):
    correct = stats[Statistics.CORRECT]
    incorrect = stats[Statistics.INCORRECT]
    total = correct + incorrect
    words_per_run = int(CONFIG[Settings.WORDS_PER_RUN])

    try:
        correct_percentage = round(correct / total * 100)
    except ZeroDivisionError:
        correct_percentage = 0
    try:
        incorrect_percentage = round(incorrect / total * 100)
    except ZeroDivisionError:
        incorrect_percentage = 0
    total_percentage = round(total / words_per_run * 100)

    correct_half = round(correct_percentage / 2)
    incorrect_half = round(incorrect_percentage / 2)
    total_half = round(total_percentage / 2)
    remaining_correct = 50 - correct_half
    remaining_incorrect = 50 - incorrect_half
    remaining_total = 50 - total_half

    correct_bar = f"{WHITE_BLOCK_UPPER * correct_half}{DOT * remaining_correct}"
    incorrect_bar = f"{WHITE_BLOCK_UPPER * incorrect_half}{DOT * remaining_incorrect}"
    total_bar = f"{WHITE_BLOCK_FULL * total_half}{LIGHT_SHADOW * remaining_total}"

    correct = str(correct).rjust(2, "0").rjust(3)
    incorrect = str(incorrect).rjust(2, "0").rjust(3)
    total = str(total).rjust(2, "0").rjust(3)

    correct_percentage = str(correct_percentage).rjust(2, "0").rjust(3)
    incorrect_percentage = str(incorrect_percentage).rjust(2, "0").rjust(3)
    total_percentage = str(total_percentage).rjust(2, "0").rjust(3)

    print(f" PASS {correct} |{correct_bar}| {correct_percentage} %")
    print(f" FAIL {incorrect} |{incorrect_bar}| {incorrect_percentage} %")
    print(f" DONE {total} |{total_bar}| {total_percentage} %")
    create_a_border("=")


def get_longest_total_number(stats: dict) -> int:
    max_number = []
    for element in list(stats[Statistics.TIERS].values()):
        for key, value in element.items():
            max_number.append(value[Tier.TOTAL])

    return len(str(max(max_number))) + 1


def show_title_head(self):
    os.system("cls")
    create_a_border("=")
    current_statistics = f"WORD {self.index:02} OF {self.words_per_run:02}".center(22)
    print(f"{'-' * 22}|{current_statistics}|{'-' * 23}")
    create_a_border("=")
    print(USER_TIPS.center(SCREEN_WIDTH))
    print(TRANSFORMATION.center(SCREEN_WIDTH))
    create_a_border()


def show_word_tiers(stats: dict):
    ____ = "".center(Tier.MAX_LENGTH)
    # max_total = get_longest_total_number(stats)
    max_total = Tier.MAX_LENGTH + 2
    current_tick = stats[Statistics.CURRENT_TIER]

    print(
        f" {''.center(Tier.MAX_LENGTH)}   | {'Total'.center(20)} | {'Remaining'.center(20)}"
    )
    print(f"{'-' * 20}--+{'-' * 22}+{'-' * 23}")

    for index, (key, value) in enumerate(stats[Statistics.TIERS].items(), 1):
        name = key.center(Tier.MAX_LENGTH)

        total_low = f"{value[Tier.LOWER][Tier.TOTAL]}".center(max_total)
        total_mid = f"{value[Tier.MIDDLE][Tier.TOTAL]}".center(max_total)
        total_top = f"{value[Tier.UPPER][Tier.TOTAL]}".center(max_total)

        left_low = f"{value[Tier.LOWER][Tier.LEFT]}".center(max_total)
        left_mid = f"{value[Tier.MIDDLE][Tier.LEFT]}".center(max_total)
        left_top = f"{value[Tier.UPPER][Tier.LEFT]}".center(max_total)

        tick_low = WHITE_BLOCK_FULL if current_tick == [key, Tier.LOWER] else " "
        tick_mid = WHITE_BLOCK_FULL if current_tick == [key, Tier.MIDDLE] else " "
        tick_top = WHITE_BLOCK_FULL if current_tick == [key, Tier.UPPER] else " "

        print(f" {____} |{tick_low}| {total_low} | {left_low}")
        print(f" {name} |{tick_mid}| {total_mid} | {left_mid}")
        print(f" {____} |{tick_top}| {total_top} | {left_top}")

        if index != len(stats[Statistics.TIERS]):
            print(f"{'-' * 20}+-+{'-' * 22}+{'-' * 23}")
        else:
            create_a_border("=")


def show_translate_prompt(word: str):
    print(f"\n English: {word}")


def get_answer(main):
    max_width = 31
    if len(main.word.english) > max_width:
        tail = main.word.english[-3:]
        head = main.word.english[: (max_width - len(tail) - 1)]
        word = f"{head}~{tail}"
    else:
        word = f"{main.word.english.center(31)}"

    answer = input(f" {word} | >>> ").strip()

    if answer in ["q", "r"]:
        return False
    else:
        main.answer = answer.replace("a:", "ä").replace("o:", "ö")
        return True


def create_a_settings_table() -> List[str]:
    headers = ["#", "Name".center(50), "Value"]
    table = [
        [index, key.capitalize(), value]
        for index, (key, value) in enumerate(CONFIG.items(), 1)
    ]
    table += [[0, "Exit", ""]]

    print(tabulate(table, headers, tablefmt="orgtbl"))
    create_a_border()

    return [str(element[0]) for element in table]


def create_a_table_old(
    headers: list,
    rows: list,
    bottom_border: str = "=",
    center: bool = False,
    show_exit: bool = True,
    go_back: bool = False,
    show_index: bool = True,
    index_start: int = 1,
    upper_headers: bool = False,
    capitalize_rows: bool = True,
) -> List[str]:
    full_width, remainder, remainder_used = get_paddings(headers)

    headers.insert(0, "#") if show_index else headers
    headers = [h.upper() for h in headers] if upper_headers else headers

    if len(headers[1:]) == 1:
        headers[1] = headers[1].ljust(full_width)
    else:
        for index, header in enumerate(headers):
            if index != 0:
                extra = remainder if not remainder_used else 0
                padding_final = round(full_width / len(headers[1:])) + extra
                if center:
                    headers[index] = headers[index].center(padding_final)
                else:
                    headers[index] = headers[index].ljust(padding_final)
                remainder_used = True

    for index, row in enumerate(rows):
        row = [row] if not isinstance(row, list) else row
        for index_, element in enumerate(row):
            element = str(element)
            element = f"{element[:18]}~" if len(element) >= 22 else element
            row[index_] = element.capitalize() if capitalize_rows else element

    table = [
        [index] + row if isinstance(row, list) else [index, row.capitalize()]
        for index, row in enumerate(rows, index_start)
    ]

    table = table + [[0, "Exit the application", ""]] if show_exit else table
    table = table + [["00", "Go back", ""]] if go_back else table

    print(
        tabulate(
            table,
            headers,
            tablefmt="presto",
            stralign="center" if center else "default",
        )
    )
    create_a_border(bottom_border)

    return [str(element[0]) for element in table]


def get_paddings(headers):
    index_column = 5
    separators = len(headers)
    inside_cell = len(headers) * 1
    padding = len(headers) * 3
    full_width = SCREEN_WIDTH - sum([index_column, separators, inside_cell, padding])
    remainder = full_width % 2 if full_width % 2 != 0 else 0
    remainder_used = False

    return full_width, remainder, remainder_used
