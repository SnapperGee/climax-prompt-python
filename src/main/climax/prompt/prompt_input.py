from dataclasses import dataclass, field
from functools import cached_property
from typing import TypeIs, final


@dataclass(frozen=True)
class PromptInput[ValueType]:
    r"""Container for a string and either a value or exception.

    Intended for use as the return type of the :meth:`climax.prompt.Prompt.exec_input_loop`.

    If a :attr:`~PromptInput.value` is set to a non-``None`` value and a
    :attr:`~PromptInput.conversion_exception` is also set (to any truthy value)
    at the same time then a ``ValueError`` is raised.
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

    conversion_exception: Exception | None
    r"""The exception thrown during conversion if one is thrown.

    If this field is set to a truthy value, then :attr:`value` must be set to
    ``None`` otherwise a ``ValueError`` is raised.
    """

    def __post_init__(self) -> None:
        if self.conversion_exception and self.value is not None:
            raise ValueError(
                f"{type(self).__name__}: truthy `conversion_exception` with "
                f"non-None `value`:\n{self.value}\n\n{self.conversion_exception!r}"
            )

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if not isinstance(other, PromptInput):
            return NotImplemented

        if self.original_input_string != other.original_input_string or self.value != other.value:
            return False

        return self._conversion_exception_tuple == other._conversion_exception_tuple

    def __hash__(self) -> int:
        return hash((self.original_input_string, self.value, self._conversion_exception_tuple))

    @cached_property
    def _conversion_exception_tuple(self) -> tuple[type[Exception], tuple[object, ...]] | None:
        return (type(self.conversion_exception), self.conversion_exception.args) if self.conversion_exception else None


@final
@dataclass(frozen=True, eq=False)
class PromptInputSuccessfulConversion[ValueType](PromptInput[ValueType]):
    original_input_string: str
    value: ValueType
    conversion_exception: None = field(default=None, init=False)


@final
@dataclass(frozen=True, eq=False)
class PromptInputFailedConversion[ValueType](PromptInput[ValueType]):
    original_input_string: str
    value: None = field(default=None, init=False)
    conversion_exception: Exception


def is_successful_conversion[ValueType](
    prompt_input: PromptInput[ValueType],
) -> TypeIs[PromptInputSuccessfulConversion[ValueType]]:
    r"""Determine whether a prompt input represents a successful conversion.

    Parameters
    ----------
    prompt_input : PromptInput
        The prompt input to check.

    Returns
    -------
    bool
        ``True`` if ``prompt_input`` is a
        :class:`PromptInputSuccessfulConversion`; otherwise, ``False``.

    Notes
    -----
    When this function returns ``True``, type checkers can narrow
    ``prompt_input`` to :class:`PromptInputSuccessfulConversion`.
    """
    return isinstance(prompt_input, PromptInputSuccessfulConversion)
