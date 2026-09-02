import builtins
from collections.abc import Callable
from typing import Final
from unittest.mock import patch

from climax.prompt import StringPrompt
from pytest import mark


def test_stringprompt_fields() -> None:
    message: Final = "Input a palindrome.\n"

    def string_validator(string: str) -> bool:
        return string == string[::-1]

    def invalid_string_message_generator(raw_string: str, _: str) -> str:
        return f'"{raw_string}" is not a palindrome.\n'

    def formatter(string: str) -> str:
        return string.strip()

    ps1: Final = ">>> "

    string_prompt: Final = StringPrompt(
        message,
        string_validator,
        invalid_string_message_generator,
        formatter=formatter,
        ps1=ps1,
    )

    assert string_prompt.message is message
    assert string_prompt.string_validator is string_validator
    assert string_prompt.invalid_string_message_generator is invalid_string_message_generator
    assert string_prompt.formatter is formatter
    assert string_prompt.ps1 is ps1


def test_stringprompt_default_field_values() -> None:
    string_prompt: Final = StringPrompt(
        "",
        lambda _: True,
        lambda _, __: "",
    )

    assert string_prompt.formatter is None
    assert string_prompt.ps1 is None


def test_stringprompt_default_format_method_is_identity_function() -> None:
    string: Final = "snake"

    string_prompt: Final = StringPrompt(
        "",
        lambda _: True,
        lambda _, __: "",
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
    message: Final = "message"

    def invalid_message_generator(raw_input: str, formatted_input: str) -> str:
        return f'Invalid raw input: "{raw_input}". Invalid formatted input: "{formatted_input}"\n"'

    string_prompt: Final = StringPrompt(
        message,
        validator,
        invalid_message_generator,
    )

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    assert result == user_input
    mock_input.assert_called_once_with(message)
