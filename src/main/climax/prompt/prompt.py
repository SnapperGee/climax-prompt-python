from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import final

from ._util import always_none_returning_function
from .input_string_conversion_error import InputStringConversionError
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

    @final
    def exec_input_loop(self) -> PromptInputSuccessfulConversion[ValueType] | PromptInputFailedConversion[ValueType]:
        r"""Execute an input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator`, gets converted via the :attr:`converter`, and
        then validated with the :attr:`validator`, and will return either the
        value (resulting from the converted ``string`` input) or both the value
        and raw unformatted ``string`` input indicated by the
        ``include_original_input`` parameter.

        Returns
        -------
        PromptInput
            The original raw unformatted ``string`` input and either the
            converted value of the formatted ``string`` input or the raised
            exception if one is raised during conversion.
        """
        formatted_string_input, original_string_input = super().exec_string_input_loop()

        try:
            converted_input = self.converter(formatted_string_input)
        except Exception as exception:  # noqa: BLE001
            return PromptInputFailedConversion[ValueType](original_string_input, InputStringConversionError(exception))

        while (invalid_input_string_message := self._validator(converted_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="")

            formatted_string_input, original_string_input = super().exec_string_input_loop()

            try:
                converted_input = self.converter(formatted_string_input)
            except Exception as exception:  # noqa: BLE001
                return PromptInputFailedConversion[ValueType](
                    original_string_input, InputStringConversionError(exception)
                )

        return PromptInputSuccessfulConversion[ValueType](original_string_input, converted_input, None)
