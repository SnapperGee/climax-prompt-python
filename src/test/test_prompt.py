import builtins
from collections.abc import Callable
from typing import Final
from unittest.mock import call, patch

from climax.prompt import (
    Prompt,
    StringInput,
    StringValidator,
    Validator,
    _always_none_string_validator,
    _string_identity_function,
)
from pytest import mark, raises

from .util import MESSAGE, PS1, string_is_digit


def _is_even_positive_integer(integer: int) -> str | None:
    if integer <= 0:
        return f"Integer is not positive: {integer}"

    if integer % 2 != 0:
        return f"Integer is not even: {integer}"

    return None


def _string_is_float(strings: tuple[str, str]) -> str | None:
    return (
        None
        if (split_string := strings[0].split(".", 1))
        and len(split_string) == 2
        and split_string[0].isdecimal()
        and split_string[1].isdecimal()
        else f'String is not a float: "{strings[1]}".\n'
    )


def _float_contains_non_zero_decimals(a_float: float) -> str | None:
    return None if a_float != int(a_float) else f"Float contains no non zero decimals: {a_float}"


@mark.parametrize(
    "string_validator,_type,validator,formatter,ps1,user_input,expected",
    (
        (string_is_digit, int, _is_even_positive_integer, None, None, "124", 124),
        (string_is_digit, int, _is_even_positive_integer, str.strip, None, "     2     ", 2),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "253242", 253242),
        (string_is_digit, int, _is_even_positive_integer, str.strip, PS1, "     26     ", 26),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, None, "124.1", 124.1),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, None, "     1.04     ", 1.04),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, PS1, "253242.252523", 253242.252523),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, PS1, "     26.1111     ", 26.1111),
    ),
)
def test_prompt_execInputLoop_with_valid_input_and_no_raw_string_return_argument(
    string_validator: StringValidator,
    _type: type,
    validator: Validator,
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: float,
) -> None:
    prompt: Final = Prompt(MESSAGE, string_validator, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop()

    assert result == expected
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))


@mark.parametrize(
    "string_validator,_type,validator,formatter,ps1,user_input,expected",
    (
        (string_is_digit, int, _is_even_positive_integer, None, None, "124", 124),
        (string_is_digit, int, _is_even_positive_integer, str.strip, None, "     2     ", 2),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "253242", 253242),
        (string_is_digit, int, _is_even_positive_integer, str.strip, PS1, "     26     ", 26),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, None, "124.1", 124.1),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, None, "     1.04     ", 1.04),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, PS1, "253242.252523", 253242.252523),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, PS1, "     26.1111     ", 26.1111),
    ),
)
def test_prompt_execInputLoop_with_valid_input_and_false_raw_string_return_argument(
    string_validator: StringValidator,
    _type: type,
    validator: Validator,
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: float,
) -> None:
    prompt: Final = Prompt(MESSAGE, string_validator, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop(False)

    assert result == expected
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))


@mark.parametrize(
    "string_validator,_type,validator,formatter,ps1,user_input,expected",
    (
        (string_is_digit, int, _is_even_positive_integer, None, None, "124", 124),
        (string_is_digit, int, _is_even_positive_integer, str.strip, None, "     2     ", 2),
        (string_is_digit, int, _is_even_positive_integer, None, PS1, "253242", 253242),
        (string_is_digit, int, _is_even_positive_integer, str.strip, PS1, "     26     ", 26),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, None, "124.1", 124.1),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, None, "     1.04     ", 1.04),
        (_string_is_float, float, _float_contains_non_zero_decimals, None, PS1, "253242.252523", 253242.252523),
        (_string_is_float, float, _float_contains_non_zero_decimals, str.strip, PS1, "     26.1111     ", 26.1111),
    ),
)
def test_stringprompt_execInputLoop_with_valid_input_and_raw_string_return_argument(
    string_validator: StringValidator,
    _type: type,
    validator: Validator,
    formatter: Callable[[str], str] | None,
    ps1: str | None,
    user_input: str,
    expected: float,
) -> None:
    prompt: Final = Prompt(MESSAGE, string_validator, _type, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = prompt.exec_input_loop(True)

    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))

    assert isinstance(result, tuple)
    assert result[0] == expected
    assert result[1] == user_input
