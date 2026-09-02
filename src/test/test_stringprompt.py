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


def _strip_string(string: str) -> str:
    return string.strip()


def test_stringprompt_fields() -> None:

    string_prompt: Final = StringPrompt(
        _MESSAGE,
        _always_true_string_predicate,
        _invalid_string_message_generator,
        formatter=_strip_string,
        ps1=_PS1,
    )

    assert string_prompt.message is _MESSAGE
    assert string_prompt.string_validator is _always_true_string_predicate
    assert string_prompt.invalid_string_message_generator is _invalid_string_message_generator
    assert string_prompt.formatter is _strip_string
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
    "validator,formatter,user_input",
    (
        (lambda string: len(string) == 0, None, ""),
        (lambda string: string.isdigit(), None, "123"),
        (lambda string: string == string[::-1], None, "level"),
        (lambda string: len(string) == 0, _strip_string, "         "),
        (lambda string: string.isdigit(), _strip_string, "     123     "),
        (lambda string: string == string[::-1], _strip_string, "level         "),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input(
    validator: Callable[[str], bool], formatter: Callable[[str], str] | None, user_input: str
) -> None:
    string_prompt: Final = StringPrompt(_MESSAGE, validator, _invalid_string_message_generator, formatter=formatter)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    assert result == (formatter(user_input) if formatter else user_input)
    mock_input.assert_called_once_with(_MESSAGE)
