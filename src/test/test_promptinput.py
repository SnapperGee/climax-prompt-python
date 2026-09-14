from typing import Final

from climax.prompt import PromptInput
from pytest import mark, raises


@mark.parametrize(
    "string,value,exception",
    (
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, Exception("An exception")),
        ("", None, Exception("An exception")),
    ),
)
def test_PromptResult_equality(string: str, value: object | None, exception: Exception | None) -> None:

    a_prompt_result: Final = PromptInput(string, value, exception)
    another_prompt_result: Final = PromptInput(string, value, exception)
    assert a_prompt_result == another_prompt_result


@mark.parametrize(
    "string,value,exception",
    (
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, Exception("An exception")),
        ("", None, Exception("An exception")),
    ),
)
def test_PromptResult_hash(string: str, value: object | None, exception: Exception | None) -> None:

    a_prompt_result: Final = PromptInput(string, value, exception)
    another_prompt_result: Final = PromptInput(string, value, exception)
    assert hash(a_prompt_result) == hash(another_prompt_result)


@mark.parametrize(
    "string,value,exception",
    (
        ("1", 1, Exception("An exception")),
        ("", False, Exception("An exception")),
    ),
)
def test_PromptResult_non_none_value_filed_with_truthy_exception_conversion_field_raises_ValueError(
    string: str, value: object, exception: Exception
) -> None:
    with raises(ValueError):
        PromptInput(string, value, exception)
