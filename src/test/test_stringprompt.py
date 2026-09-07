import builtins
from collections.abc import Callable
from typing import Final
from unittest.mock import call, patch

from climax.prompt import StringInput, StringPrompt, StringValidator
from pytest import mark, raises

_MESSAGE: Final = "message\n"

_PS1: Final = ">>> "


def _always_none_string_validator(_: tuple[str, str]) -> None:
    return None


def _string_is_empty(strings: tuple[str, str]) -> str | None:
    return None if len(strings[0]) == 0 else f'String is not empty: "{strings[1]}"'


def _string_is_not_empty(strings: tuple[str, str]) -> str | None:
    return None if len(strings[0]) != 0 else "String is empty"


def _string_is_palindrome(strings: tuple[str, str]) -> str | None:
    return None if strings[0] == strings[0][::-1] else f'String is not a palindrome: "{strings[1]}"'


def _string_is_digit(strings: tuple[str, str]) -> str | None:
    return None if strings[0].isdigit() else f'String is not a digit: "{strings[1]}"'


def test_stringprompt_fields() -> None:

    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_none_string_validator,
        formatter=str.strip,
        ps1=_PS1,
    )

    assert string_prompt.message is _MESSAGE
    assert string_prompt.string_validator is _always_none_string_validator
    assert string_prompt.formatter is str.strip
    assert string_prompt.ps1 is _PS1


def test_stringprompt_default_field_values() -> None:
    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_none_string_validator,
    )

    assert string_prompt.formatter is None
    assert string_prompt.ps1 is None


def test_stringprompt_default_format_method_is_identity_function() -> None:
    string: Final = "snake"

    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_none_string_validator,
    )

    assert string_prompt.format(string) is string


@mark.parametrize(
    "validator,user_input,formatter,ps1",
    (
        (_string_is_empty, "", None, None),
        (_string_is_digit, "123", None, None),
        (_string_is_palindrome, "level", None, None),
        (_string_is_empty, "         ", str.strip, None),
        (_string_is_digit, "     123     ", str.strip, None),
        (_string_is_palindrome, "level         ", str.strip, None),
        (_string_is_empty, "", None, _PS1),
        (_string_is_digit, "123", None, _PS1),
        (_string_is_palindrome, "level", None, _PS1),
        (_string_is_empty, "         ", str.strip, _PS1),
        (_string_is_digit, "     123     ", str.strip, _PS1),
        (_string_is_palindrome, "level         ", str.strip, _PS1),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input_and_no_raw_string_return_argument(
    validator: StringValidator, user_input: str, formatter: Callable[[str], str] | None, ps1: str | None
) -> None:
    string_prompt: Final = StringPrompt(_MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    assert result == (formatter(user_input) if formatter else user_input)
    mock_input.assert_called_once_with(_MESSAGE + (ps1 or ""))


@mark.parametrize(
    "validator,user_input,formatter,ps1",
    (
        (_string_is_empty, "", None, None),
        (_string_is_digit, "123", None, None),
        (_string_is_palindrome, "level", None, None),
        (_string_is_empty, "         ", str.strip, None),
        (_string_is_digit, "     123     ", str.strip, None),
        (_string_is_palindrome, "level         ", str.strip, None),
        (_string_is_empty, "", None, _PS1),
        (_string_is_digit, "123", None, _PS1),
        (_string_is_palindrome, "level", None, _PS1),
        (_string_is_empty, "         ", str.strip, _PS1),
        (_string_is_digit, "     123     ", str.strip, _PS1),
        (_string_is_palindrome, "level         ", str.strip, _PS1),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input_and_false_raw_string_return_argument(
    validator: StringValidator, user_input: str, formatter: Callable[[str], str] | None, ps1: str | None
) -> None:
    string_prompt: Final = StringPrompt(_MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop(False)

    assert result == (formatter(user_input) if formatter else user_input)
    mock_input.assert_called_once_with(_MESSAGE + (ps1 or ""))


@mark.parametrize(
    "validator,user_input,formatter,ps1",
    (
        (_string_is_empty, "", None, None),
        (_string_is_digit, "123", None, None),
        (_string_is_palindrome, "level", None, None),
        (_string_is_empty, "         ", str.strip, None),
        (_string_is_digit, "     123     ", str.strip, None),
        (_string_is_palindrome, "level         ", str.strip, None),
        (_string_is_empty, "", None, _PS1),
        (_string_is_digit, "123", None, _PS1),
        (_string_is_palindrome, "level", None, _PS1),
        (_string_is_empty, "         ", str.strip, _PS1),
        (_string_is_digit, "     123     ", str.strip, _PS1),
        (_string_is_palindrome, "level         ", str.strip, _PS1),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input_and_raw_string_return_argument(
    validator: StringValidator, user_input: str, formatter: Callable[[str], str] | None, ps1: str | None
) -> None:
    string_prompt: Final = StringPrompt(_MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop(True)

    mock_input.assert_called_once_with(_MESSAGE + (ps1 or ""))

    assert isinstance(result, StringInput)
    assert result.formatted == (formatter(user_input) if formatter else user_input)
    assert result.raw_unformatted == user_input


@mark.parametrize(
    "validator,user_input,formatter,ps1",
    (
        (_string_is_not_empty, "", None, None),
        (_string_is_digit, "A123", None, None),
        (_string_is_palindrome, "Knights who say ni", None, None),
        (_string_is_not_empty, "         ", str.strip, None),
        (_string_is_digit, "  A   123     ", str.strip, None),
        (_string_is_palindrome, "Knights who say ni", str.strip, None),
        (_string_is_not_empty, "", None, _PS1),
        (_string_is_digit, "A123", None, _PS1),
        (_string_is_palindrome, "Knights who say ni", None, _PS1),
        (_string_is_not_empty, "         ", str.strip, _PS1),
        (_string_is_digit, "  A   123     ", str.strip, _PS1),
        (_string_is_palindrome, "Knights who say ni", str.strip, _PS1),
    ),
)
def test_stringprompt_execStringInputLoop_with_invalid_input(
    validator: StringValidator, user_input: str, formatter: Callable[[str], str] | None, ps1: str | None
) -> None:
    string_prompt: Final = StringPrompt(_MESSAGE, validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input, raises(StopIteration):
        string_prompt.exec_string_input_loop()

    assert mock_input.call_args_list == [
        call(_MESSAGE + (ps1 or "")),
        call(
            (validator(StringInput(formatter(user_input) if formatter else user_input, user_input)) or "")
            + _MESSAGE
            + (ps1 or "")
        ),
    ]
