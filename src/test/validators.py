def string_is_digit(strings: tuple[str, str]) -> str | None:
    return None if strings[0].isdigit() else f'String is not a digit: "{strings[1]}".\n'
