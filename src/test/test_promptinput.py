from typing import Final

from climax.prompt.input_string_conversion_error import InputStringConversionError
from climax.prompt.prompt_input import PromptInput
from pytest import mark, raises


@mark.parametrize(
    "string,value,exception",
    (
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, InputStringConversionError(Exception("An exception"))),
        ("", None, InputStringConversionError(Exception("An exception"))),
    ),
)
def test_PromptInput_equality(string: str, value: object | None, exception: InputStringConversionError | None) -> None:

    prompt_input: Final = PromptInput(string, value, exception)
    other_prompt_input: Final = PromptInput(string, value, exception)
    assert prompt_input == other_prompt_input


@mark.parametrize(
    "string,value,exception",
    (
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, InputStringConversionError(Exception("An exception"))),
        ("", None, InputStringConversionError(Exception("An exception"))),
    ),
)
def test_PromptInput_hash(string: str, value: object | None, exception: InputStringConversionError | None) -> None:

    prompt_input: Final = PromptInput(string, value, exception)
    other_prompt_input: Final = PromptInput(string, value, exception)
    assert hash(prompt_input) == hash(other_prompt_input)


@mark.parametrize(
    "string,value,exception",
    (
        ("1", 1, InputStringConversionError(Exception("An exception"))),
        ("", False, InputStringConversionError(Exception("An exception"))),
    ),
)
def test_PromptInput_non_none_value_filed_with_truthy_exception_conversion_field_raises_ValueError(
    string: str, value: object, exception: InputStringConversionError
) -> None:
    with raises(ValueError):
        PromptInput(string, value, exception)
