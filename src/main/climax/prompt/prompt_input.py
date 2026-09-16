from dataclasses import dataclass
from typing import final

from .input_string_conversion_error import InputStringConversionError


def _exception_key(exception: Exception | None) -> tuple[type[Exception], tuple[object, ...]] | None:
    if exception is None:
        return None

    return (type(exception), exception.args)


@dataclass(frozen=True)
class PromptInput[ValueType]:
    r"""Container for a string and either a value or exception.

    Intended for use as the return type of the :meth:`climax.prompt.Prompt.exec_input_loop`.

    If a :attr:`~PromptInput.value` is set to a non-``None`` value and a
    :attr:`~PromptInput.conversion_exception` is also set (to any truthy value)
    at the same time then a ``ValueError`` is thrown.
    """

    original_input_string: str
    r"""The raw unformatted original ``string``."""

    value: ValueType | None
    r"""The value of the converted formatted input string.

    If an exception is raised during conversion then this value should be set to
    ``None``.

    If this field is set to ``None`` then :attr:`conversion_exception` muse be
    set to a truthy value otherwise a ``ValueError`` is raised.
    """

    conversion_exception: InputStringConversionError | None
    r"""The exception thrown during conversion if one is thrown.

    If this field is set to a truthy value, then :attr:`value` must be set to
    ``None`` otherwise a ``ValueError`` is raised.
    """

    def __post_init__(self) -> None:
        if self.conversion_exception and self.value is not None:
            raise ValueError(
                f"{type(self).__name__}: truthy `conversion_exception` with "
                f"non-None `value`:\n{self.value=}\n\n{self.conversion_exception!r}"
            )

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if not isinstance(other, PromptInput):
            return NotImplemented

        if self.original_input_string != other.original_input_string or self.value != other.value:
            return False

        return _exception_key(self.conversion_exception) == _exception_key(other.conversion_exception)

    def __hash__(self) -> int:
        return hash((self.original_input_string, self.value, _exception_key(self.conversion_exception)))


@final
@dataclass(frozen=True)
class PromptInputSuccessfulConversion[ValueType](PromptInput[ValueType]):
    original_input_string: str
    value: ValueType
    conversion_exception: None


@final
@dataclass(frozen=True)
class PromptInputFailedConversion(PromptInput[None]):
    original_input_string: str
    value: None
    conversion_exception: InputStringConversionError
