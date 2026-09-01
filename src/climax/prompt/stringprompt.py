from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, final


def _always_true_predicate(_: object) -> Literal[True]:
    return True


def _default_invalid_string_message_generator(_: str, __: str) -> Literal[""]:
    return ""


def _default_formatter(string: str) -> str:
    return string


@dataclass(frozen=True)
class StringPrompt:
    message: str
    string_validator: Callable[[str], bool] | None
    invalid_string_message_generator: Callable[[str, str], str] | None
    formatter: Callable[[str], str] | None = field(kw_only=True, default=None)
    ps1: str | None = field(kw_only=True, default=None)

    @final
    @cached_property
    def _string_validator(self) -> Callable[[str], bool]:
        return self.string_validator or _always_true_predicate

    @final
    @cached_property
    def _invalid_string_message_generator(self) -> Callable[[str, str], str]:
        return (
            self.invalid_string_message_generator
            or _default_invalid_string_message_generator
        )

    @final
    @cached_property
    def _formatter(self) -> Callable[[str], str]:
        return self.formatter or _default_formatter

    @final
    @cached_property
    def _ps1(self) -> str:
        return self.ps1 if self.ps1 is not None else ""

    @final
    def exec_string_input_loop(self) -> str:
        _input = input(self.message + self._ps1)
        formatted_input = self._formatter(_input)

        while not self._string_validator(formatted_input):
            invalid_input_string = self._invalid_string_message_generator(
                _input, formatted_input
            )
            _input = input(invalid_input_string + self.message + self._ps1)
            formatted_input = self._formatter(_input)

        return formatted_input
