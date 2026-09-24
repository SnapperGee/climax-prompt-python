from re import escape
from typing import Final

import pytest
from climax.prompt.prompt_input import PromptInput

_EXCEPTION: Final = Exception("An exception")


@pytest.mark.parametrize(
    ("string", "value", "exception"),
    [
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, _EXCEPTION),
        ("", None, _EXCEPTION),
    ],
)
def test_PromptInput_equality(string: str, value: object | None, exception: Exception | None) -> None:

    prompt_input: Final = PromptInput(string, value, exception)
    other_prompt_input: Final = PromptInput(string, value, exception)
    assert prompt_input == other_prompt_input


@pytest.mark.parametrize(
    ("string", "value", "exception"),
    [
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, _EXCEPTION),
        ("", None, _EXCEPTION),
    ],
)
def test_PromptInput_hash(string: str, value: object | None, exception: Exception | None) -> None:

    prompt_input: Final = PromptInput(string, value, exception)
    other_prompt_input: Final = PromptInput(string, value, exception)
    assert hash(prompt_input) == hash(other_prompt_input)


@pytest.mark.parametrize(
    ("string", "value", "exception"),
    [
        ("1", 1, _EXCEPTION),
        ("", False, _EXCEPTION),
    ],
)
def test_PromptInput_non_none_value_filed_with_truthy_exception_conversion_field_raises_ValueError(
    string: str, value: object, exception: Exception
) -> None:
    with pytest.raises(
        ValueError,
        match=escape(
            f"{PromptInput.__name__}: truthy `conversion_exception` with non-None `value`:\n{value}\n\n{exception!r}"
        ),
    ):
        PromptInput(string, value, exception)
