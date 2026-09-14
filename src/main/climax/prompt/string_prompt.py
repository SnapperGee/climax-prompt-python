from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, final, overload

from ._util import always_none_returning_function, string_identity_function
from .string_prompt_input import StringPromptInput
from .validator import StringValidator


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
    formatted and raw unformatted original ``string`` input.

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
        return self.string_validator or always_none_returning_function

    @final
    @cached_property
    def _formatter(self) -> Callable[[str], str]:
        return self.formatter or string_identity_function

    @final
    @cached_property
    def _ps1(self) -> str:
        return self.ps1 if self.ps1 is not None else ""

    @overload
    def exec_string_input_loop(self) -> str: ...
    @overload
    def exec_string_input_loop(self, include_original_input: Literal[False]) -> str: ...
    @overload
    def exec_string_input_loop(self, include_original_input: Literal[True]) -> StringPromptInput: ...
    @overload
    def exec_string_input_loop(self, include_original_input: bool) -> str | StringPromptInput: ...
    @final
    def exec_string_input_loop(self, include_original_input: bool = False) -> str | StringPromptInput:
        r"""Execute a ``string`` input prompt loop.

        The loop will require a user to input a ``string`` that passes the
        :attr:`string_validator` validation and will return either the formatted
        ``string`` or both the formatted and raw unformatted ``string``
        indicated by the ``include_original_input`` parameter.

        Parameters
        ----------
        include_original_input : bool, optional
            Flag indicating whether to include the raw unformatted original
            ``string`` input in the return. Defaults to ``False``.

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
        string_input = StringPromptInput(self._formatter(raw_string_input), raw_string_input)

        while (invalid_input_string_message := self._string_validator(string_input)) is not None:
            raw_string_input = input(invalid_input_string_message + self.message + self._ps1)
            string_input = StringPromptInput(self._formatter(raw_string_input), raw_string_input)

        return string_input if include_original_input else string_input.formatted
