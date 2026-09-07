from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, final, overload


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
        return self.invalid_string_message_generator or _default_invalid_string_message_generator

    @final
    @cached_property
    def _formatter(self) -> Callable[[str], str]:
        return self.formatter or _default_formatter

    @final
    @cached_property
    def _ps1(self) -> str:
        return self.ps1 if self.ps1 is not None else ""

    @final
    def format(self, string: str) -> str:
        return self._formatter(string)

    @overload
    def exec_string_input_loop(self) -> str: ...
    @overload
    def exec_string_input_loop(self, include_raw_input: Literal[False]) -> str: ...
    @overload
    def exec_string_input_loop(self, include_raw_input: Literal[True]) -> tuple[str, str]: ...
    @final
    def exec_string_input_loop(self, include_raw_input: Literal[True, False] = False) -> str | tuple[str, str]:
        _input = input(self.message + self._ps1)
        formatted_input = self.format(_input)

        while not self._string_validator(formatted_input):
            invalid_input_string = self._invalid_string_message_generator(_input, formatted_input)
            _input = input(invalid_input_string + self.message + self._ps1)
            formatted_input = self.format(_input)

        return formatted_input if not include_raw_input else (formatted_input, _input)


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    converter: Callable[[str], ValueType]
    validator: Callable[[ValueType], bool] | None
    invalid_value_message_generator: Callable[[ValueType], str] | None

    @cached_property
    def _validator(self) -> Callable[[ValueType], bool]:
        return self.validator or _always_true_predicate

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
        string_input = super().exec_string_input_loop(include_raw_input)
        converted_input = self.converter(string_input if isinstance(string_input, str) else string_input[0])

        while not self._validator(converted_input):
            if self.invalid_value_message_generator:
                print(self.invalid_value_message_generator(converted_input), end="")

            string_input = super().exec_string_input_loop(include_raw_input)
            converted_input = self.converter(string_input if isinstance(string_input, str) else string_input[0])

        return converted_input if isinstance(string_input, str) else (converted_input, string_input[1])
