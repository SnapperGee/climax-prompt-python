r"""Provides classes that instantiate prompt objects capable of processing inputs of arbitrary types.

See Also
--------
:mod:`climax.prompt.string_prompt` : Module that provides the object class the
    class this module exports wraps.
"""

import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Self, final

from ._util import always_none_returning_function, identity
from .prompt_result import PromptResult, PromptResultFailure, PromptResultSuccess
from .string_prompt import StringPrompt
from .validator import StringValidator, Validator


@final
@dataclass(frozen=True)
class Prompt[ValueType]:
    r"""Create a loop prompting a user for input until valid input is given.

    The input value is initially interpreted as a ``string`` and validated and
    then (if it passes validation) gets converted to an arbitrary type that then
    gets validated again.

    ``ValueType`` is the type to which the ``str`` input is converted.

    See Also
    --------
    :class:`StringPrompt` : The class wrapped by this class responsible for
        displaying the initial message and processing the string input before
        converting it.
    """

    string_prompt: StringPrompt
    r"""Displays the initial message and processes the string input before converting it."""

    converter: Callable[[str], ValueType]
    r"""Function that converts the ``str`` input to ``ValueType``."""

    validator: Validator[ValueType] = always_none_returning_function
    r"""Validates the converted value.

    If validation fails it returns a ``string`` message explaining why
    validation failed that gets displayed to the user.

    See Also
    --------
    :class:`Validator` : The type of function used for validation.
    """

    @classmethod
    def create(
        cls,
        message: str,
        converter: Callable[[str], ValueType],
        *,
        validator: Validator[ValueType] | None = always_none_returning_function,
        string_validator: StringValidator | None = always_none_returning_function,
        formatter: Callable[[str], str] | None = identity,
        ps1: str | None = "",
    ) -> Self:
        r"""Creates an instance of a :class:`Prompt` object.

        Parameters
        ----------
        message : str
            ``string`` message presented to the user.
        converter : Callable[[str], ValueType]
            Function that converts the ``str`` input to ``ValueType``.
        validator : Validator[ValueType] | None, optional
            Function that validates the converted value. Successful validation
            returns ``None`` while failed validation returns a ``string``
            message explaining failure reasons. Defaults to a validator that
            interprets every value as valid.
        string_validator : StringValidator | None, optional
            Function that validates the formatted string value before converting
            it. Successful validation returns ``None`` while failed validation
            returns a ``string`` message explaining failure reasons. Defaults to
            a validator that interprets string as valid.
        formatter : Callable[[str], str] | None, optional
            Function that formats/transforms the string input before validating
            it. Defaults to a function that returns the argument passed to it
            (performs no formatting).
        ps1 : str | None, optional
            ``string`` appended to the ``message`` visually indicating where
            input is entered. Defaults to an empty string.

        Returns
        -------
        :class:`Prompt`
            An instance of a :class:`Prompt` object.
        """

        return cls(
            StringPrompt(
                message,
                string_validator=string_validator or always_none_returning_function,
                formatter=formatter or identity,
                ps1=ps1 or "",
            ),
            converter,
            validator or always_none_returning_function,
        )

    def exec_input_loop(self) -> PromptResult[ValueType]:
        r"""Execute an input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator`, gets converted via the :attr:`converter`, and
        then validated with the :attr:`validator`, and will return the value
        (resulting from the converted ``string`` input) and original raw
        unformatted input ``string``.

        Returns
        -------
        PromptResultSuccess[ValueType] | PromptResultFailure
            The value of the converted formatted ``string`` input and the
            original unformatted input ``string``.
        """
        formatted_string_input, original_string_input = self.string_prompt.exec_string_input_loop()

        try:
            converted_input = self.converter(formatted_string_input)
        except Exception as exception:  # noqa: BLE001
            return PromptResultFailure(original_string_input, exception)

        while (invalid_input_string_message := self.validator(converted_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="", file=sys.stderr)

            formatted_string_input, original_string_input = self.string_prompt.exec_string_input_loop()

            try:
                converted_input = self.converter(formatted_string_input)
            except Exception as exception:  # noqa: BLE001
                return PromptResultFailure(original_string_input, exception)

        return PromptResultSuccess[ValueType](original_string_input, converted_input)
