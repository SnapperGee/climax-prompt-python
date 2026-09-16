import builtins
from collections.abc import Callable
from typing import Final
from unittest.mock import call, patch

from climax.prompt import (
    Prompt,
    StringPromptInput,
    StringValidator,
    Validator,
)
from climax.prompt.input_string_conversion_error import InputStringConversionError
from climax.prompt.prompt_input import PromptInput
from pytest import mark, raises

from .util import MESSAGE, PS1, string_is_digit


def _always_none_returning_function(_: object) -> None:
    return


def _is_even_positive_integer(integer: int) -> str | None:
    if integer <= 0:
        return f"Integer is not positive: {integer}\n"

    if integer % 2 != 0:
        return f"Integer is not even: {integer}\n"

    return None


def _string_is_float(strings: tuple[str, str]) -> str | None:
    return (
        None
        if (
            split_string := strings[0].split(".", 2) if not strings[0].startswith("-") else strings[0][1:].split(".", 2)
        )
        and len(split_string) == 2
        and split_string[0].isdecimal()
        and split_string[1].isdecimal()
        else f'String is not a float: "{strings[1]}".\n'
    )


def _float_contains_non_zero_decimals(a_float: float) -> str | None:
    return None if a_float != int(a_float) else f"Float contains no non zero decimals: {a_float}\n"


@mark.parametrize(
    "string_validator,_type,validator,formatter,ps1,user_input,expected",
    (
        (string_is_digit, int, _is_even_positive_integer, None, None, "124", PromptInput("124", 124, None)),
        (
            string_is_digit,
            int,
            _is_even_positive_integer,
            str.strip,
            None,
            "     2     ",
            PromptInput("     2     ", 2, None),
        ),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "253242", PromptInput("253242", 253242, None)),
        (
            string_is_digit,
            int,
            _is_even_positive_integer,
            str.strip,
            PS1,
            "     26     ",
            PromptInput("     26     ", 26, None),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            None,
            None,
            "124.1",
            PromptInput("124.1", 124.1, None),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            str.strip,
            None,
            "     1.04     ",
            PromptInput("     1.04     ", 1.04, None),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            None,
            PS1,
            "253242.252523",
            PromptInput("253242.252523", 253242.252523, None),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            str.strip,
            PS1,
            "     26.1111     ",
            PromptInput("     26.1111     ", 26.1111, None),
        ),
    ),
)
def test_Prompt_execInputLoop_with_valid_input(
    string_validator: StringValidator,
    _type: type,
    validator: Validator[int | float],
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: PromptInput[int | float],
) -> None:
    prompt: Final = Prompt(MESSAGE, string_validator, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop()

    assert result == expected
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))


@mark.parametrize(
    "string_validator,_type,validator,formatter,ps1,user_input",
    (
        (string_is_digit, int, _is_even_positive_integer, None, None, "124XXX"),
        (string_is_digit, int, _is_even_positive_integer, None, None, "111"),
        (string_is_digit, int, _is_even_positive_integer, None, None, "-999"),
        (string_is_digit, int, _is_even_positive_integer, str.strip, None, "     7     "),
        (string_is_digit, int, _is_even_positive_integer, str.strip, None, "     2  snake   "),
        (string_is_digit, int, _is_even_positive_integer, str.strip, None, "     -2     "),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "333333"),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "253242XX"),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "-253242"),
        (string_is_digit, int, _is_even_positive_integer, str.strip, PS1, "  snake   26     "),
        (string_is_digit, int, _is_even_positive_integer, str.strip, PS1, "     21     "),
        (string_is_digit, int, _is_even_positive_integer, str.strip, PS1, "     -26     "),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, None, "124"),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, None, "124.000"),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, None, "     1     "),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, None, "     1.00     "),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, PS1, "253242.000000"),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, PS1, "     26.0000     "),
    ),
)
def test_Prompt_execInputLoop_with_invalid_input(
    string_validator: StringValidator,
    _type: type,
    validator: Validator[int | float],
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
) -> None:
    prompt: Final = Prompt(MESSAGE, string_validator, _type, validator, formatter=formatter, ps1=ps1)

    with (
        patch.object(builtins, "print") as mock_print,
        patch.object(builtins, "input", side_effect=(user_input,)) as mock_input,
        raises(StopIteration),
    ):
        prompt.exec_input_loop()

    formatted_user_input: Final = formatter(user_input) if formatter else user_input
    message_with_ps1: Final = MESSAGE + (ps1 or "")

    string_error_message: Final = string_validator(StringPromptInput(formatted_user_input, user_input))

    assert mock_input.call_count == 2
    assert mock_input.call_args_list[0] == call(message_with_ps1)

    if string_error_message is not None:
        assert mock_input.call_args_list[1] == call(string_error_message + message_with_ps1)
    else:
        error_message: Final = validator(_type(formatted_user_input)) or ""
        mock_print.assert_called_once_with(error_message, end="")


@mark.parametrize(
    "_type,validator,formatter,ps1,user_input,expected",
    (
        (
            int,
            _is_even_positive_integer,
            str.strip,
            None,
            "abc",
            PromptInput(
                "abc", None, InputStringConversionError(ValueError("invalid literal for int() with base 10: 'abc'"))
            ),
        ),
        (
            float,
            _float_contains_non_zero_decimals,
            str.strip,
            PS1,
            "XXX",
            PromptInput(
                "XXX", None, InputStringConversionError(ValueError("could not convert string to float: 'XXX'"))
            ),
        ),
    ),
)
def test_Prompt_execInputLoop_with_conversion_error(
    _type: type,
    validator: Validator[int | float],
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: PromptInput[int | float],
) -> None:
    prompt: Final = Prompt(MESSAGE, _always_none_returning_function, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop()

    assert result == expected
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))
