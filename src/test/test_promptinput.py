from typing import Final

from climax.prompt.input_string_conversion_error import InputStringConversionError
from climax.prompt.prompt_input import _PromptInput
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
def test_PromptResult_equality(string: str, value: object | None, exception: InputStringConversionError | None) -> None:

    a_prompt_result: Final = _PromptInput(string, value, exception)
    another_prompt_result: Final = _PromptInput(string, value, exception)
    assert a_prompt_result == another_prompt_result


@mark.parametrize(
    "string,value,exception",
    (
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, InputStringConversionError(Exception("An exception"))),
        ("", None, InputStringConversionError(Exception("An exception"))),
    ),
)
def test_PromptResult_hash(string: str, value: object | None, exception: InputStringConversionError | None) -> None:

    a_prompt_result: Final = _PromptInput(string, value, exception)
    another_prompt_result: Final = _PromptInput(string, value, exception)
    assert hash(a_prompt_result) == hash(another_prompt_result)


@mark.parametrize(
    "string,value,exception",
    (
        ("1", 1, InputStringConversionError(Exception("An exception"))),
        ("", False, InputStringConversionError(Exception("An exception"))),
    ),
)
def test_PromptResult_non_none_value_filed_with_truthy_exception_conversion_field_raises_ValueError(
    string: str, value: object, exception: InputStringConversionError
) -> None:
    with raises(ValueError):
        _PromptInput(string, value, exception)
