import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import final

from ._util import always_none_returning_function, identity
from .string_prompt_input import StringPromptInput
from .validator import StringValidator


@final
@dataclass(frozen=True)
class StringPrompt:
    r"""Create a loop prompting a user for ``string`` input until valid input is given.

    The input value is always interpreted and returned as a ``string``.

    See Also
    --------
    :class:`Prompt` : A class wrapped around this one that can process inputs of
        arbitrary types (not just ``str``).
    """

    message: str
    r"""A ``string`` message presented to the user."""

    string_validator: StringValidator = field(kw_only=True, default=always_none_returning_function)
    r"""Validates ``string`` input.

    If validation fails it returns a ``string`` message explaining why
    validation failed that gets displayed to the user. It has access to both the
    formatted and raw unformatted original ``string`` input.

    See Also
    --------
    :class:`StringValidator` : The type of function used for :class:`StringPromptInput` validation.
    """

    formatter: Callable[[str], str] = field(kw_only=True, default=identity)
    r"""Formats ``string`` input."""

    ps1: str = field(kw_only=True, default="")
    r"""``string`` appended to the :attr:`message` ``string`` visually indicating where input will be entered."""

    @final
    def exec_string_input_loop(self) -> StringPromptInput:
        r"""Execute a ``string`` input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator` validation and will return both the formatted
        and original raw unformatted ``string`` inputted by the user.

        Returns
        -------
        StringPromptInput
            The formatted and original raw unformatted ``string`` input that passed validation.

        See Also
        --------
        :class:`StringPromptInput`
        """
        raw_unformatted_string_input = input(self.message + self.ps1)
        string_input = StringPromptInput(self.formatter(raw_unformatted_string_input), raw_unformatted_string_input)

        while (invalid_input_string_message := self.string_validator(string_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="", file=sys.stderr)
            raw_unformatted_string_input = input(self.message + self.ps1)
            string_input = StringPromptInput(self.formatter(raw_unformatted_string_input), raw_unformatted_string_input)

        return string_input
