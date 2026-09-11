import builtins
from collections.abc import Callable
from typing import Final
from unittest.mock import call, patch

from climax.prompt import (
    StringInput,
    StringPrompt,
    StringValidator,
    _always_none_string_validator,
    _string_identity_function,
)
from pytest import mark, raises

from .util import MESSAGE, PS1, string_is_digit


def _string_is_empty(strings: tuple[str, str]) -> str | None:
    return None if len(strings[0]) == 0 else f'String is not empty: "{strings[1]}".\n'


def _string_is_not_empty(strings: tuple[str, str]) -> str | None:
    return None if len(strings[0]) != 0 else "String is empty.\n"


def _string_is_palindrome(strings: tuple[str, str]) -> str | None:
    return None if strings[0] == strings[0][::-1] else f'String is not a palindrome: "{strings[1]}".\n'


def test_stringprompt_fields() -> None:

    string_prompt: Final = StringPrompt(
        MESSAGE,
        _string_is_empty,
        formatter=str.strip,
        ps1=PS1,
    )

    assert string_prompt.message is MESSAGE
    assert string_prompt.string_validator is _string_is_empty
    assert string_prompt.formatter is str.strip
    assert string_prompt.ps1 is PS1


def test_stringprompt_default_field_values() -> None:
    string_prompt: Final = StringPrompt(
        MESSAGE,
        None,
    )

    assert string_prompt._formatter is _string_identity_function
    assert string_prompt._string_validator is _always_none_string_validator
    assert string_prompt.formatter is None
    assert string_prompt.ps1 is None


@mark.parametrize(
    "validator,formatter,ps1,user_input",
    (
        (_string_is_empty, None, None, ""),
        (string_is_digit, None, None, "123"),
        (_string_is_palindrome, None, None, "level"),
        (_string_is_empty, str.strip, None, "         "),
        (string_is_digit, str.strip, None, "     123     "),
        (_string_is_palindrome, str.strip, None, "level         "),
        (_string_is_empty, None, PS1, ""),
        (string_is_digit, None, PS1, "123"),
        (_string_is_palindrome, None, PS1, "level"),
        (_string_is_empty, str.strip, PS1, "         "),
        (string_is_digit, str.strip, PS1, "     123     "),
        (_string_is_palindrome, str.strip, PS1, "level         "),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input_and_no_original_string_return_argument(
    validator: StringValidator, formatter: Callable[[str], str] | None, ps1: str | None, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    assert result == (formatter(user_input) if formatter else user_input)
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))


@mark.parametrize(
    "validator,formatter,ps1,user_input",
    (
        (_string_is_empty, None, None, ""),
        (string_is_digit, None, None, "123"),
        (_string_is_palindrome, None, None, "level"),
        (_string_is_empty, str.strip, None, "         "),
        (string_is_digit, str.strip, None, "     123     "),
        (_string_is_palindrome, str.strip, None, "level         "),
        (_string_is_empty, None, PS1, ""),
        (string_is_digit, None, PS1, "123"),
        (_string_is_palindrome, None, PS1, "level"),
        (_string_is_empty, str.strip, PS1, "         "),
        (string_is_digit, str.strip, PS1, "     123     "),
        (_string_is_palindrome, str.strip, PS1, "level         "),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input_and_false_original_string_return_argument(
    validator: StringValidator, formatter: Callable[[str], str] | None, ps1: str | None, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop(False)

    assert result == (formatter(user_input) if formatter else user_input)
    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))


@mark.parametrize(
    "validator,formatter,ps1,user_input",
    (
        (_string_is_empty, None, None, ""),
        (string_is_digit, None, None, "123"),
        (_string_is_palindrome, None, None, "level"),
        (_string_is_empty, str.strip, None, "         "),
        (string_is_digit, str.strip, None, "     123     "),
        (_string_is_palindrome, str.strip, None, "level         "),
        (_string_is_empty, None, PS1, ""),
        (string_is_digit, None, PS1, "123"),
        (_string_is_palindrome, None, PS1, "level"),
        (_string_is_empty, str.strip, PS1, "         "),
        (string_is_digit, str.strip, PS1, "     123     "),
        (_string_is_palindrome, str.strip, PS1, "level         "),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input_and_original_original_string_return_argument(
    validator: StringValidator, formatter: Callable[[str], str] | None, ps1: str | None, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop(True)

    mock_input.assert_called_once_with(MESSAGE + (ps1 or ""))

    assert isinstance(result, StringInput)
    assert result.formatted == (formatter(user_input) if formatter else user_input)
    assert result.original == user_input


@mark.parametrize(
    "validator,formatter,ps1,user_input",
    (
        (_string_is_not_empty, None, None, ""),
        (string_is_digit, None, None, "A123"),
        (_string_is_palindrome, None, None, "Knights who say ni"),
        (_string_is_not_empty, str.strip, None, "         "),
        (string_is_digit, str.strip, None, "  A   123     "),
        (_string_is_palindrome, str.strip, None, "Knights who say ni"),
        (_string_is_not_empty, None, PS1, ""),
        (string_is_digit, None, PS1, "A123"),
        (_string_is_palindrome, None, PS1, "Knights who say ni"),
        (_string_is_not_empty, str.strip, PS1, "         "),
        (string_is_digit, str.strip, PS1, "  A   123     "),
        (_string_is_palindrome, str.strip, PS1, "Knights who say ni"),
    ),
)
def test_stringprompt_execStringInputLoop_with_invalid_input(
    validator: StringValidator, formatter: Callable[[str], str] | None, ps1: str | None, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input, raises(StopIteration):
        string_prompt.exec_string_input_loop()

    message_with_ps1: Final = MESSAGE + (ps1 or "")

    assert mock_input.call_args_list == [
        call(message_with_ps1),
        call(
            (validator(StringInput(formatter(user_input) if formatter else user_input, user_input)) or "")
            + message_with_ps1
        ),
    ]
