from typing import Final

from climax.prompt import StringPromptInput

MESSAGE: Final = "message\n"

PS1: Final = ">>> "


def string_is_integer_validator(strings: StringPromptInput) -> str | None:
    return None if strings.formatted.removeprefix("-").isdecimal() else f'String is not a digit: "{strings[1]}".\n'
