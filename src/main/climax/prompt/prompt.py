from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import Literal, final, overload

from .stringprompt import StringPrompt
from .validator import Validator


def _always_none_returning_function(_: object) -> None:
    r"""A function that consumes an ``object`` and returns ``None``."""
    return


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    r"""Create a loop prompting a user for input until valid input is given.

    The input value is initially interpreted as a ``string`` and validated and
    then (if it passes validation) gets converted to an arbitrary type that then
    gets validated again.

    ``ValueType`` is the type to which the ``str`` input is converted.

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
    def exec_input_loop(self, include_original_input: Literal[False]) -> ValueType: ...
    @overload
    def exec_input_loop(self, include_original_input: Literal[True]) -> tuple[ValueType, str]: ...
    @overload
    def exec_input_loop(self, include_original_input: bool) -> ValueType | tuple[ValueType, str]: ...
    @final
    def exec_input_loop(self, include_original_input: bool = False) -> ValueType | tuple[ValueType, str]:
        r"""Execute an input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator`, gets converted via the :attr:`converter`, and
        then validated with the :attr:`validator`, and will return either the
        value (resulting from the converted ``string`` input) or both the value
        and raw unformatted ``string`` input indicated by the
        ``include_original_input`` parameter.

        Parameters
        ----------
        include_original_input : bool, optional
            Flag indicating whether to include the raw unformatted original
            ``string`` input in the return. Defaults to ``False``.

        Returns
        -------
        ValueType | tuple[ValueType, str]
            The value (resulting from the converted ``string`` input) or both
            the value and raw unformatted ``string`` input.
        """
        string_input = super().exec_string_input_loop(include_original_input)
        converted_input = self.converter(string_input if isinstance(string_input, str) else string_input.formatted)

        while (invalid_input_string_message := self._validator(converted_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="")

            string_input = super().exec_string_input_loop(include_original_input)
            converted_input = self.converter(string_input if isinstance(string_input, str) else string_input.formatted)

        return converted_input if isinstance(string_input, str) else (converted_input, string_input.original)
