import builtins
from collections.abc import Callable
from typing import Final, Literal
from unittest.mock import call, patch

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


def _string_is_empty(string: str) -> bool:
    return len(string) == 0


def _string_is_not_empty(string: str) -> bool:
    return len(string) != 0


def _string_is_palindrome(string: str) -> bool:
    return string == string[::-1]


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
    "validator,user_input,formatter",
    (
        (_string_is_empty, "", None),
        (str.isdigit, "123", None),
        (_string_is_palindrome, "level", None),
        (_string_is_empty, "         ", _strip_string),
        (str.isdigit, "     123     ", _strip_string),
        (_string_is_palindrome, "level         ", _strip_string),
    ),
)
def test_stringprompt_execStringInputLoop_with_valid_input(
    validator: Callable[[str], bool], user_input: str, formatter: Callable[[str], str] | None
) -> None:
    string_prompt: Final = StringPrompt(_MESSAGE, validator, _invalid_string_message_generator, formatter=formatter)

    with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
        result: Final = string_prompt.exec_string_input_loop()

    assert result == (formatter(user_input) if formatter else user_input)
    mock_input.assert_called_once_with(_MESSAGE)


# @mark.parametrize(
#     "validator,user_input,formatter",
#     (
#         (_string_is_not_empty, "", None),
#         (str.isdigit, "A123", None),
#         (_string_is_palindrome, "Knights who say ni", None),
#         (_string_is_not_empty, "         ", _strip_string),
#         (str.isdigit, "  A   123     ", _strip_string),
#         (_string_is_palindrome, "Knights who say ni", _strip_string),
#     ),
# )
# def test_stringprompt_execStringInputLoop_with_invalid_input(
#     validator: Callable[[str], bool], user_input: str, formatter: Callable[[str], str] | None
# ) -> None:
#     string_prompt: Final = StringPrompt(_MESSAGE, validator, _invalid_string_message_generator, formatter=formatter)

#     with patch.object(builtins, "input", side_effect=(user_input,)) as mock_input:
#         result: Final = string_prompt.exec_string_input_loop()

#     assert result is None
#     assert mock_input.call_args_list == [
#         call(_MESSAGE),
#         call(
#             _invalid_string_message_generator(
#                 user_input,
#                 formatter(user_input) if formatter else user_input,
#             )
#             + _MESSAGE
#         ),
#     ]
