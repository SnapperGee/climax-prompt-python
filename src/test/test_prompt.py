import builtins
from collections.abc import Callable
from sys import stderr
from typing import Final
from unittest.mock import call, patch

import pytest
from climax.prompt import (
    Prompt,
    StringPromptInput,
    StringValidator,
    Validator,
)
from climax.prompt.input_string_conversion_error import InputStringConversionError
from climax.prompt.prompt_input import (
    PromptInputFailedConversion,
    PromptInputSuccessfulConversion,
    is_successful_conversion,
)

from .util import MESSAGE, PS1, string_is_digit


def _always_none_returning_function(_: object) -> None:
    return


def _is_even_positive_integer(integer: int) -> str | None:
    if integer <= 0:
        return f"Integer is not positive: {integer}\n"

    if integer % 2 != 0:
        return f"Integer is not even: {integer}\n"

    return None


def _string_is_float(strings: StringPromptInput) -> str | None:
    return (
        None
        if (
            split_string := strings.formatted.split(".", 2)
            if not strings.formatted.startswith("-")
            else strings.formatted[1:].split(".", 2)
        )
        and len(split_string) == 2
        and split_string[0].isdecimal()
        and split_string[1].isdecimal()
        else f'String is not a float: "{strings[1]}".\n'
    )


def _float_contains_non_zero_decimals(a_float: float) -> str | None:
    return None if a_float != int(a_float) else f"Float contains no non zero decimals: {a_float}\n"


@pytest.mark.parametrize(
    ("string_validator", "_type", "validator", "formatter", "ps1", "user_input", "expected"),
    [
        (
            string_is_digit,
            int,
            _is_even_positive_integer,
            None,
            None,
            "124",
            PromptInputSuccessfulConversion("124", 124),
        ),
        (
            string_is_digit,
            int,
            _is_even_positive_integer,
            str.strip,
            None,
            "     2     ",
            PromptInputSuccessfulConversion("     2     ", 2),
        ),
        (
            string_is_digit,
            int,
            _is_even_positive_integer,
            None,
            PS1,
            "253242",
            PromptInputSuccessfulConversion("253242", 253242),
        ),
        (
            string_is_digit,
            int,
            _is_even_positive_integer,
            str.strip,
            PS1,
            "     26     ",
            PromptInputSuccessfulConversion("     26     ", 26),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            None,
            None,
            "124.1",
            PromptInputSuccessfulConversion("124.1", 124.1),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            str.strip,
            None,
            "     1.04     ",
            PromptInputSuccessfulConversion("     1.04     ", 1.04),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            None,
            PS1,
            "253242.252523",
            PromptInputSuccessfulConversion("253242.252523", 253242.252523),
        ),
        (
            _string_is_float,
            float,
            _float_contains_non_zero_decimals,
            str.strip,
            PS1,
            "     26.1111     ",
            PromptInputSuccessfulConversion("     26.1111     ", 26.1111),
        ),
    ],
)
def test_Prompt_execInputLoop_with_valid_input(
    string_validator: StringValidator,
    _type: type,
    validator: Validator[int | float],
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: PromptInputSuccessfulConversion[int | float],
) -> None:
    prompt: Final = Prompt(MESSAGE, string_validator, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop()

    assert is_successful_conversion(result)
    assert result == expected
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))


@pytest.mark.parametrize(
    ("string_validator", "_type", "validator", "formatter", "ps1", "user_input"),
    [
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
    ],
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
        patch.object(builtins, "input", side_effect=(user_input,)) as mock_input,
        patch.object(builtins, "print") as mock_print,
        pytest.raises(StopIteration),
    ):
        prompt.exec_input_loop()

    formatted_user_input: Final = formatter(user_input) if formatter else user_input
    message_with_ps1: Final = MESSAGE + (ps1 or "")

    string_error_message: Final = string_validator(StringPromptInput(formatted_user_input, user_input))

    assert mock_input.call_args_list == [
        call(message_with_ps1),
        call(message_with_ps1),
    ]

    if string_error_message:
        mock_print.assert_called_once_with(string_error_message, end="", file=stderr)
    else:
        error_message: Final = validator(_type(formatted_user_input))
        mock_print.assert_called_once_with(error_message, end="", file=stderr)


@pytest.mark.parametrize(
    ("_type", "validator", "formatter", "ps1", "user_input", "expected"),
    [
        (
            int,
            _is_even_positive_integer,
            str.strip,
            None,
            "abc",
            PromptInputFailedConversion[int](
                "abc", InputStringConversionError(ValueError("invalid literal for int() with base 10: 'abc'"))
            ),
        ),
        (
            float,
            _float_contains_non_zero_decimals,
            str.strip,
            PS1,
            "XXX",
            PromptInputFailedConversion[float](
                "XXX", InputStringConversionError(ValueError("could not convert string to float: 'XXX'"))
            ),
        ),
    ],
)
def test_Prompt_execInputLoop_with_conversion_error(
    _type: type,
    validator: Validator[int | float],
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: PromptInputFailedConversion[int | float],
) -> None:
    prompt: Final = Prompt(MESSAGE, _always_none_returning_function, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop()

    assert not is_successful_conversion(result)
    assert result == expected
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))
