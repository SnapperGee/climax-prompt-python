import builtins
from collections.abc import Callable
from typing import Final, Literal
from unittest.mock import patch

from climax.prompt import StringPrompt
from pytest import mark

_MESSAGE: Final = "message\n"

_PS1: Final = ">>> "


def _always_true_string_predicate(_: str) -> Literal[True]:
    return True


def _invalid_string_message_generator(raw_input: str, formatted_input: str) -> str:
    return f'Invalid raw input: "{raw_input}". Invalid formatted input: "{formatted_input}"\n"'


def test_stringprompt_fields() -> None:

    def formatter(string: str) -> str:
        return string.strip()

    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_true_string_predicate,
        _invalid_string_message_generator,
        formatter=formatter,
        ps1=_PS1,
    )

    assert string_prompt.message is _MESSAGE
    assert string_prompt.string_validator is _always_true_string_predicate
    assert string_prompt.invalid_string_message_generator is _invalid_string_message_generator
    assert string_prompt.formatter is formatter
    assert string_prompt.ps1 is _PS1


def test_stringprompt_default_field_values() -> None:
    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_true_string_predicate,
        _invalid_string_message_generator,
    )

    assert string_prompt.formatter is None
    assert string_prompt.ps1 is None


def test_stringprompt_default_format_method_is_identity_function() -> None:
    string: Final = "snake"

    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_true_string_predicate,
        _invalid_string_message_generator,
    )

    assert string_prompt.format(string) is string


@mark.parametrize(
    "validator,user_input",
    (
        (lambda string: len(string) == 0, ""),
        (lambda string: string.isdigit(), "123"),
        (lambda string: string == string[::-1], "level"),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input(validator: Callable[[str], bool], user_input: str) -> None:
    string_prompt: Final = StringPrompt(
        _MESSAGE,
        validator,
        _invalid_string_message_generator,
    )

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    assert result == user_input
    mock_input.assert_called_once_with(_MESSAGE)
