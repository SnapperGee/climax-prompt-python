from typing import Final, Literal

MESSAGE: Final = "message\n"

PS1: Final = ">>> "


def string_is_digit(strings: tuple[str, str]) -> str | None:
    return (
        None
        if (strings[0].isdecimal() if not strings[0].startswith("-") else strings[0][1:].isdecimal())
        else f'String is not a digit: "{strings[1]}".\n'
    )

def always_true_returning_function(_: object) -> Literal[True]:
    return True
