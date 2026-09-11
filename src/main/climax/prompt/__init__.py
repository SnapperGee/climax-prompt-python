from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, NamedTuple, final, overload


def _always_none_returning_function(_: object) -> None:
    r"""A function that consumes an ``object`` and returns ``None``."""
    return


def _string_identity_function(string: str) -> str:
    r"""An identity function that consumes a ``string`` and returns the same ``string``."""
    return string


class StringInput(NamedTuple):
    r"""A container for a formatted ``string`` and the original unformatted ``string``."""

    formatted: str
    r"""A formatted ``string``."""

    raw_unformatted: str
    r"""A raw unformatted ``string``."""


type Validator[T] = Callable[[T], str | None]
r"""A function that validates a value.

If validation fails then a ``string`` explaining why it failed should be
returned, otherwise ``None`` should be returned.
"""

type StringValidator = Validator[StringInput]
r"""A function that validates a :class:`StringInput`.

If validation fails then a ``string`` explaining why it failed should be
returned, otherwise ``None`` should be returned.

See Also
--------
:obj:`Validator` : The type this type is based on.
"""


def _always_none_string_validator(_result: StringInput) -> None:
    r"""A function that consumes a :class:`StringInput` object and returns ``None``."""
    return


@dataclass(frozen=True)
class StringPrompt:
    r"""Create a loop prompting a user for ``string`` input until valid input is given.

    The input value is always interpreted and returned as a ``string``.

    See Also
    --------
    :class:`Prompt` : A class derived from this one that can process inputs of
    arbitrary types (not just ``str``).
    """

    message: str
    r"""A ``string`` message presented to the user."""

    string_validator: StringValidator | None
    r"""Validates ``string`` input.

    If validation fails it returns a ``string`` message explaining why
    validation failed that gets displayed to the user. It has access to both the
    formatted and raw unformatted ``string`` input.

    If field is set to ``None``, then all ``string`` input is considered valid.

    See Also
    --------
    :obj:`StringValidator` : The type of function used for :class:`StringInput` validation.
    """

    formatter: Callable[[str], str] | None = field(kw_only=True, default=None)
    r"""Formats ``string`` input.

    If field is set to ``None`` then no formatting is performed.
    """

    ps1: str | None = field(kw_only=True, default=None)
    r"""Optional ``string`` appended to the :attr:`message` ``string`` indicating where input will be entered."""

    @final
    @cached_property
    def _string_validator(self) -> StringValidator:
        return self.string_validator or _always_none_string_validator

    @final
    @cached_property
    def _formatter(self) -> Callable[[str], str]:
        return self.formatter or _string_identity_function

    @final
    @cached_property
    def _ps1(self) -> str:
        return self.ps1 if self.ps1 is not None else ""

    @overload
    def exec_string_input_loop(self) -> str: ...
    @overload
    def exec_string_input_loop(self, include_raw_input: Literal[False]) -> str: ...
    @overload
    def exec_string_input_loop(self, include_raw_input: Literal[True]) -> StringInput: ...
    @overload
    def exec_string_input_loop(self, include_raw_input: bool) -> str | StringInput: ...
    @final
    def exec_string_input_loop(self, include_raw_input: bool = False) -> str | StringInput:
        r"""Execute a ``string`` input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator` validation and will return either the formatted
        ``string`` or both the formatted and raw unformatted ``string``
        indicated by the ``include_raw_input`` parameter.

        Parameters
        ----------
        include_raw_input : bool, optional
            Flag indicating whether to include the raw unformatted ``string``
            input in the return. Defaults to ``False``.

        Returns
        -------
        str | StringInput
            The validated formatted ``string`` input or both the validated
            formatted and raw unformatted ``string`` input.

        See Also
        --------
        :obj:`StringInput`
        """
        raw_string_input = input(self.message + self._ps1)
        string_input = StringInput(self._formatter(raw_string_input), raw_string_input)

        while (invalid_input_string_message := self._string_validator(string_input)) is not None:
            raw_string_input = input(invalid_input_string_message + self.message + self._ps1)
            string_input = StringInput(self._formatter(raw_string_input), raw_string_input)

        return string_input if include_raw_input else string_input.formatted


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    r"""Create a loop prompting a user for input until valid input is given.

    The input value is initially interpreted as a ``string`` and validated and
    then (if it passes validation) gets converted to an arbitrary type that then
    gets validated again.

    Type Parameters
    ---------------
    ValueType
        The type the ``string`` input gets converted to.

    See Also
    --------
    :class:`StringPrompt` : The base class from which this class is derived,
    which processes only ``str`` inputs.
    """

    converter: Callable[[str], ValueType]
    r"""Function that converts the ``str`` input to ``ValueType``."""

    validator: Validator[ValueType] | None
    r"""Validates the converted ``string`` input.

    If validation fails it returns a ``string`` message explaining why
    validation failed that gets displayed to the user.

    If field is set to ``None``, then all values are considered valid.

    See Also
    --------
    :obj:`Validator` : The type of function used for validation.
    """

    @cached_property
    def _validator(self) -> Callable[[ValueType], str | None]:
        return self.validator or _always_none_returning_function

    @overload
    def exec_input_loop(self) -> ValueType: ...
    @overload
    def exec_input_loop(self, include_raw_input: Literal[False]) -> ValueType: ...
    @overload
    def exec_input_loop(self, include_raw_input: Literal[True]) -> tuple[ValueType, str]: ...
    @overload
    def exec_input_loop(self, include_raw_input: bool) -> ValueType | tuple[ValueType, str]: ...
    @final
    def exec_input_loop(self, include_raw_input: bool = False) -> ValueType | tuple[ValueType, str]:
        r"""Execute an input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator`, gets converted via the :attr:`converter`, and
        then validated with the :attr:`validator`, and will return either the
        value (resulting from the converted ``string`` input) or both the value
        and raw unformatted ``string`` input indicated by the
        ``include_raw_input`` parameter.

        Parameters
        ----------
        include_raw_input : bool, optional
            Flag indicating whether to include the raw unformatted ``string``
            input in the return. Defaults to ``False``.

        Returns
        -------
        ValueType | tuple[ValueType, str]
            The value (resulting from the converted ``string`` input) or both
            the value and raw unformatted ``string`` input.
        """
        string_input = super().exec_string_input_loop(include_raw_input)
        converted_input = self.converter(string_input if isinstance(string_input, str) else string_input.formatted)

        while (invalid_input_string_message := self._validator(converted_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="")

            string_input = super().exec_string_input_loop(include_raw_input)
            converted_input = self.converter(string_input if isinstance(string_input, str) else string_input.formatted)

        return converted_input if isinstance(string_input, str) else (converted_input, string_input.raw_unformatted)
