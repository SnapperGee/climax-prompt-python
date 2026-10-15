import builtins
from collections.abc import Callable
from sys import stderr
from typing import Final
from unittest.mock import call, patch

import pytest
from climax.prompt import (
    StringPrompt,
    StringPromptInput,
    StringValidator,
)
from climax.prompt._util import always_none_returning_function, identity
from climax.prompt.prompt import Prompt
from climax.prompt.prompt_result import PromptResultFailure

from .util import MESSAGE, PS1, string_is_digit_validator


def _string_is_empty(strings: StringPromptInput) -> str | None:
    return None if len(strings.formatted) == 0 else f'String is not empty: "{strings[1]}".\n'


def _string_is_not_empty(strings: StringPromptInput) -> str | None:
    return None if len(strings.formatted) != 0 else "String is empty.\n"


def _string_is_palindrome(strings: StringPromptInput) -> str | None:
    return None if strings.formatted == strings.formatted[::-1] else f'String is not a palindrome: "{strings[1]}".\n'


def test_StringPrompt_fields() -> None:

    string_prompt: Final = StringPrompt(
        MESSAGE,
        string_validator=_string_is_empty,
        formatter=str.strip,
        ps1=PS1,
    )

    assert string_prompt.message is MESSAGE
    assert string_prompt.string_validator is _string_is_empty
    assert string_prompt.formatter is str.strip
    assert string_prompt.ps1 is PS1


def test_StringPrompt_default_field_values() -> None:
    string_prompt: Final = StringPrompt(MESSAGE)

    assert string_prompt.formatter is identity
    assert string_prompt.string_validator is always_none_returning_function
    assert string_prompt.formatter is identity
    assert string_prompt.ps1 == ""


def test_StringPrompt_returns_last_input_after_retry() -> None:
    string_prompt: Final = StringPrompt(
        MESSAGE, string_validator=string_is_digit_validator, formatter=str.strip, ps1=PS1
    )

    with (
        patch.object(builtins, "input", side_effect=("  A1  ", "  22  ")) as mock_input,
        patch.object(builtins, "print") as mock_print,
    ):
        result: Final = string_prompt.exec_string_input_loop()

    assert result == StringPromptInput("22", "  22  ")
    assert mock_input.call_count == 2
    mock_print.assert_called_once_with('String is not a digit: "  A1  ".\n', end="", file=stderr)


def test_StringPrompt_reprompts_without_printing_when_message_is_empty() -> None:
    def reject_first_call(strings: StringPromptInput) -> str | None:
        return "" if strings.formatted == "bad" else None

    string_prompt: Final = StringPrompt(MESSAGE, string_validator=reject_first_call)

    with (
        patch.object(builtins, "input", side_effect=("bad", "good")),
        patch.object(builtins, "print") as mock_print,
    ):
        result: Final = string_prompt.exec_string_input_loop()

    assert result == StringPromptInput("good", "good")
    mock_print.assert_not_called()


def test_Prompt_returns_failure_when_conversion_fails_after_retry() -> None:
    def is_even(integer: int) -> str | None:
        return None if integer % 2 == 0 else "odd\n"

    prompt: Final = Prompt.create(MESSAGE, int, validator=is_even)

    with (
        patch.object(builtins, "input", side_effect=("3", "abc")),
        patch.object(builtins, "print"),
    ):
        result: Final = prompt.exec_input_loop()

    assert result == PromptResultFailure("abc", ValueError("invalid literal for int() with base 10: 'abc'"))


@pytest.mark.parametrize(
    ("validator", "formatter", "ps1", "user_input"),
    [
        (_string_is_empty, identity, PS1, ""),
        (string_is_digit_validator, identity, PS1, "123"),
        (_string_is_palindrome, identity, PS1, "level"),
        (_string_is_empty, str.strip, PS1, "         "),
        (string_is_digit_validator, str.strip, PS1, "     123     "),
        (_string_is_palindrome, str.strip, PS1, "level         "),
    ],
)
def test_StringPrompt_execStringInputLoop_with_valid_input(
    validator: StringValidator, formatter: Callable[[str], str], ps1: str, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(MESSAGE, string_validator=validator, formatter=formatter, ps1=ps1)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    mock_input.assert_called_once_with(MESSAGE + ps1)

    assert isinstance(result, StringPromptInput)
    assert result == StringPromptInput(formatter(user_input), user_input)


@pytest.mark.parametrize(
    ("validator", "formatter", "ps1", "user_input"),
    [
        (_string_is_not_empty, identity, PS1, ""),
        (string_is_digit_validator, identity, PS1, "A123"),
        (_string_is_palindrome, identity, PS1, "Knights who say ni"),
        (_string_is_not_empty, str.strip, PS1, "         "),
        (string_is_digit_validator, str.strip, PS1, "  A   123     "),
        (_string_is_palindrome, str.strip, PS1, "Knights who say ni"),
    ],
)
def test_StringPrompt_execStringInputLoop_with_invalid_input(
    validator: StringValidator, formatter: Callable[[str], str], ps1: str, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(MESSAGE, string_validator=validator, formatter=formatter, ps1=ps1)

    with (
        patch.object(builtins, "input", side_effect=(user_input,)) as mock_input,
        patch.object(builtins, "print") as mock_print,
        pytest.raises(StopIteration),
    ):
        string_prompt.exec_string_input_loop()

    message_with_ps1: Final = MESSAGE + ps1
    invalid_message: Final = validator(StringPromptInput(formatter(user_input), user_input))

    assert mock_input.call_args_list == [
        call(message_with_ps1),
        call(message_with_ps1),
    ]

    mock_print.assert_called_once_with(invalid_message, end="", file=stderr)
