from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from sys import stderr
from typing import final

from ._util import always_none_returning_function
from .prompt_input import PromptInputFailedConversion, PromptInputSuccessfulConversion
from .string_prompt import StringPrompt
from .validator import Validator


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
        return self.validator or always_none_returning_function

    def exec_input_loop(self) -> PromptInputSuccessfulConversion[ValueType] | PromptInputFailedConversion[ValueType]:
        r"""Execute an input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator`, gets converted via the :attr:`converter`, and
        then validated with the :attr:`validator`, and will return the value
        (resulting from the converted ``string`` input) and original raw
        unformatted input ``string``.

        Returns
        -------
        PromptInputSuccessfulConversion[ValueType] | PromptInputFailedConversion[ValueType]
            The value of the converted formatted ``string`` input and the
            original unformatted input ``string``.
        """
        formatted_string_input, original_string_input = super().exec_string_input_loop()

        try:
            converted_input = self.converter(formatted_string_input)
        except Exception as exception:  # noqa: BLE001
            return PromptInputFailedConversion[ValueType](original_string_input, exception)

        while (invalid_input_string_message := self._validator(converted_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="", file=stderr)

            formatted_string_input, original_string_input = super().exec_string_input_loop()

            try:
                converted_input = self.converter(formatted_string_input)
            except Exception as exception:  # noqa: BLE001
                return PromptInputFailedConversion[ValueType](original_string_input, exception)

        return PromptInputSuccessfulConversion[ValueType](original_string_input, converted_input)
