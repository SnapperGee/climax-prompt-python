from typing import Final

import pytest
from climax.prompt.input_string_conversion_error import InputStringConversionError
from climax.prompt.prompt_input import PromptInput


@pytest.mark.parametrize(
    ("string", "value", "exception"),
    [
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, InputStringConversionError(Exception("An exception"))),
        ("", None, InputStringConversionError(Exception("An exception"))),
    ],
)
def test_PromptInput_equality(string: str, value: object | None, exception: InputStringConversionError | None) -> None:

    prompt_input: Final = PromptInput(string, value, exception)
    other_prompt_input: Final = PromptInput(string, value, exception)
    assert prompt_input == other_prompt_input


@pytest.mark.parametrize(
    ("string", "value", "exception"),
    [
        ("Snake", True, None),
        ("1", 1, None),
        ("1", None, InputStringConversionError(Exception("An exception"))),
        ("", None, InputStringConversionError(Exception("An exception"))),
    ],
)
def test_PromptInput_hash(string: str, value: object | None, exception: InputStringConversionError | None) -> None:

    prompt_input: Final = PromptInput(string, value, exception)
    other_prompt_input: Final = PromptInput(string, value, exception)
    assert hash(prompt_input) == hash(other_prompt_input)


@pytest.mark.parametrize(
    ("string", "value", "exception"),
    [
        ("1", 1, InputStringConversionError(Exception("An exception"))),
        ("", False, InputStringConversionError(Exception("An exception"))),
    ],
)
def test_PromptInput_non_none_value_filed_with_truthy_exception_conversion_field_raises_ValueError(
    string: str, value: object, exception: InputStringConversionError
) -> None:
    with pytest.raises(
        ValueError,
        match=r"ValueError: PromptInput: truthy `conversion_exception` with non-None `value`: self.value=False",
    ):
        PromptInput(string, value, exception)
