from typing import Final

import pytest
from climax.prompt.prompt_result import PromptResultFailure, PromptResultSuccess


class _CustomError(ValueError):
    pass


_EXCEPTION: Final = Exception("An exception")

_SUCCESSFUL_CONVERSION_PARAMETERS: Final = [
    ("Snake", True),
    ("1", 1),
    ("", ""),
    ("None", None),
]

# (string, first exception, second exception) where the two exceptions are
# different objects (except for the first case) that must give equal results
_EQUAL_FAILED_CONVERSION_PARAMETERS: Final = [
    ("1", _EXCEPTION, _EXCEPTION),
    ("1", ValueError("bad"), ValueError("bad")),
    ("", ValueError(), ValueError()),
    ("1", ValueError([1]), ValueError([1])),
]


@pytest.mark.parametrize(("string", "value"), _SUCCESSFUL_CONVERSION_PARAMETERS)
def test_PromptResultSuccess_equality(string: str, value: object) -> None:
    prompt_input: Final = PromptResultSuccess(string, value)
    other_prompt_input: Final = PromptResultSuccess(string, value)
    assert prompt_input == other_prompt_input


@pytest.mark.parametrize(
    ("string", "value", "other_string", "other_value"),
    [
        ("1", 1, "2", 1),
        ("1", 1, "1", 2),
        ("1", None, "1", 0),
        ("1", 0, "1", None),
    ],
)
def test_PromptResultSuccess_inequality(string: str, value: object, other_string: str, other_value: object) -> None:
    prompt_input: Final = PromptResultSuccess(string, value)
    other_prompt_input: Final = PromptResultSuccess(other_string, other_value)
    assert prompt_input != other_prompt_input


@pytest.mark.parametrize(("string", "value"), _SUCCESSFUL_CONVERSION_PARAMETERS)
def test_PromptResultSuccess_hash(string: str, value: object) -> None:
    prompt_input: Final = PromptResultSuccess(string, value)
    other_prompt_input: Final = PromptResultSuccess(string, value)
    assert hash(prompt_input) == hash(other_prompt_input)


@pytest.mark.parametrize("other", ["1", 1, None, object()])
def test_PromptResultSuccess_not_equal_to_other_types(other: object) -> None:
    prompt_input: Final = PromptResultSuccess("1", 1)
    assert prompt_input != other


@pytest.mark.parametrize(("string", "exception", "other_exception"), _EQUAL_FAILED_CONVERSION_PARAMETERS)
def test_PromptResultFailure_equality(string: str, exception: Exception, other_exception: Exception) -> None:
    prompt_input: Final = PromptResultFailure(string, exception)
    other_prompt_input: Final = PromptResultFailure(string, other_exception)
    assert prompt_input == other_prompt_input


@pytest.mark.parametrize(
    ("string", "exception", "other_string", "other_exception"),
    [
        ("1", ValueError("bad"), "2", ValueError("bad")),
        ("1", ValueError("bad"), "1", ValueError("worse")),
        ("1", ValueError("bad"), "1", TypeError("bad")),
        ("1", ValueError("bad"), "1", _CustomError("bad")),
    ],
)
def test_PromptResultFailure_inequality(
    string: str, exception: Exception, other_string: str, other_exception: Exception
) -> None:
    prompt_input: Final = PromptResultFailure(string, exception)
    other_prompt_input: Final = PromptResultFailure(other_string, other_exception)
    assert prompt_input != other_prompt_input


@pytest.mark.parametrize(("string", "exception", "other_exception"), _EQUAL_FAILED_CONVERSION_PARAMETERS)
def test_PromptResultFailure_hash(string: str, exception: Exception, other_exception: Exception) -> None:
    prompt_input: Final = PromptResultFailure(string, exception)
    other_prompt_input: Final = PromptResultFailure(string, other_exception)
    assert hash(prompt_input) == hash(other_prompt_input)


def test_PromptResultFailure_hash_with_unhashable_exception_args_does_not_raise() -> None:
    hash(PromptResultFailure("1", ValueError([1])))


def test_PromptResultFailure_set_keeps_instances_that_differ_only_in_exception_args() -> None:
    prompt_inputs: Final = {
        PromptResultFailure("1", ValueError([1])),
        PromptResultFailure("1", ValueError([1])),
        PromptResultFailure("1", ValueError([2])),
    }
    assert len(prompt_inputs) == 2


@pytest.mark.parametrize("other", ["1", 1, None, object()])
def test_PromptResultFailure_not_equal_to_other_types(other: object) -> None:
    prompt_input: Final = PromptResultFailure("1", _EXCEPTION)
    assert prompt_input != other


def test_PromptResultSuccess_not_equal_to_PromptResultFailure() -> None:
    successful: Final[object] = PromptResultSuccess("1", 1)
    failed: Final[object] = PromptResultFailure("1", _EXCEPTION)
    assert successful != failed
    assert failed != successful
