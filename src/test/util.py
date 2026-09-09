from typing import Final

MESSAGE: Final = "message\n"

PS1: Final = ">>> "


def string_is_digit(strings: tuple[str, str]) -> str | None:
    return None if strings[0].isdecimal() else f'String is not a digit: "{strings[1]}".\n'
