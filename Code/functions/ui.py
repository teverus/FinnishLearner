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


def show_run_statistics(main):
    max_elements = {
        ItemType.WORD: Settings.WORDS_PER_RUN,
        ItemType.VERB: Settings.VERBS_PER_RUN,
        ItemType.COMBINATION: Settings.WORD_COMBINATIONS_PER_RUN
    }
    max_elements = max_elements[main.item.item_type]
    stats = main.stats

    correct = stats[Statistics.CORRECT]
    incorrect = stats[Statistics.INCORRECT]
    total = correct + incorrect
    words_per_run = int(CONFIG[max_elements])

    try:
        correct_percentage = round(correct / total * 100)
    except ZeroDivisionError:
        correct_percentage = 0
    try:
        incorrect_percentage = round(incorrect / total * 100)
    except ZeroDivisionError:
        incorrect_percentage = 0
    total_percentage = round(total / words_per_run * 100)

    space_for_bar = SCREEN_WIDTH - 18
    modifier = space_for_bar / 100
    correct_half = round(correct_percentage * modifier)
    incorrect_half = round(incorrect_percentage * modifier)
    total_half = round(total_percentage * modifier)
    remaining_correct = space_for_bar - correct_half
    remaining_incorrect = space_for_bar - incorrect_half
    remaining_total = space_for_bar - total_half

    correct_bar = f"{WHITE_BLOCK_UPPER * correct_half}{DOT * remaining_correct}"
    incorrect_bar = f"{WHITE_BLOCK_UPPER * incorrect_half}{DOT * remaining_incorrect}"
    total_bar = f"{WHITE_BLOCK_FULL * total_half}{LIGHT_SHADOW * remaining_total}"

    correct = str(correct).rjust(2, "0").rjust(3)
    incorrect = str(incorrect).rjust(2, "0").rjust(3)
    total = str(total).rjust(2, "0").rjust(3)

    correct_percentage = str(correct_percentage).rjust(2, "0").rjust(3)
    incorrect_percentage = str(incorrect_percentage).rjust(2, "0").rjust(3)
    total_percentage = str(total_percentage).rjust(2, "0").rjust(3)

    print(f" PASS{correct} |{correct_bar}| {correct_percentage} %")
    print(f" FAIL{incorrect} |{incorrect_bar}| {incorrect_percentage} %")
    print(f" DONE{total} |{total_bar}| {total_percentage} %")
    create_a_border("=")


def get_longest_total_number(stats: dict) -> int:
    max_number = []
    for element in list(stats[Statistics.TIERS].values()):
        for key, value in element.items():
            max_number.append(value[Tier.TOTAL])

    return len(str(max(max_number))) + 1


def show_title_head(main, user_tips=True):
    index = main.index
    max_index = main.item.per_run
    element_type = main.item.item_type

    os.system("cls")
    create_a_border("=")
    current_statistics = f"| {element_type} {index:02} OF {max_index:02} |"
    padding = int((SCREEN_WIDTH - len(current_statistics)) / 2)
    print(f"{'-' * padding}{current_statistics}{'-' * padding}")
    create_a_border("=")
    if user_tips:
        print(USER_TIPS.center(SCREEN_WIDTH))
    print(TRANSFORMATION.center(SCREEN_WIDTH))
    create_a_border()


def show_word_tiers(stats: dict):
    if Statistics.CURRENT_TIER not in stats:
        return

    current_tick = stats[Statistics.CURRENT_TIER]
    column_width = int((SCREEN_WIDTH - 2) / 3)
    ____ = "".center(column_width - 4)

    print(
        f"{''.center(column_width)}|{'Total'.center(column_width)}|{'Remaining'.center(column_width)}"
    )
    print(f"{'-' * column_width}+{'-' * column_width}+{'-' * column_width}")

    for index, (key, value) in enumerate(stats[Statistics.TIERS].items(), 1):
        name = key.center(column_width - 4)

        total_low = f"{value[Tier.LOWER][Tier.TOTAL]}".center(column_width)
        total_mid = f"{value[Tier.MIDDLE][Tier.TOTAL]}".center(column_width)
        total_top = f"{value[Tier.UPPER][Tier.TOTAL]}".center(column_width)

        left_low = f"{value[Tier.LOWER][Tier.LEFT]}".center(column_width)
        left_mid = f"{value[Tier.MIDDLE][Tier.LEFT]}".center(column_width)
        left_top = f"{value[Tier.UPPER][Tier.LEFT]}".center(column_width)

        tick_low = WHITE_BLOCK_FULL if current_tick == [key, Tier.LOWER] else " "
        tick_mid = WHITE_BLOCK_FULL if current_tick == [key, Tier.MIDDLE] else " "
        tick_top = WHITE_BLOCK_FULL if current_tick == [key, Tier.UPPER] else " "

        print(f" {____} |{tick_low}|{total_low}|{left_low}")
        print(f" {name} |{tick_mid}|{total_mid}|{left_mid}")
        print(f" {____} |{tick_top}|{total_top}|{left_top}")

        if index != len(stats[Statistics.TIERS]):
            print(f"{'-' * column_width}+{'-' * column_width}+{'-' * column_width}")
        else:
            create_a_border("=")


def show_translate_prompt(word: str):
    print(f"\n English: {word}")


def get_answer(main):
    column_width = int((SCREEN_WIDTH - 1) / 2)

    if not main.horizontal_prompt:
        print(f"{'ENGLISH'.center(column_width)}|{'FINNISH'.center(column_width)}")
        print(f"{'-' * column_width}+{'-' * column_width}")

    if main.item.item_type == ItemType.WORD:
        if len(main.item.english) > column_width:
            tail = main.item.english[-3:]
            head = main.item.english[: (column_width - len(tail) - 1)]
            target_word = f"{head}~{tail}"
        else:
            target_word = f"{main.item.english.center(column_width)}"

        answer = input(f"{target_word}| >>> ").strip()

    if main.item.item_type == ItemType.VERB:
        answer = input(f" English: {main.item.english} ").strip()

    if main.item.item_type == ItemType.COMBINATION:
        answer = input(f"{main.item.english.center(column_width)}| >>> ")

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
