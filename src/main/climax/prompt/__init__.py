from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, NamedTuple, final, overload


def _always_none_returning_function(_: object) -> None:
    return None


def _string_identity_function(string: str) -> str:
    return string


class StringInput(NamedTuple):
    formatted: str
    raw_unformatted: str


type StringValidator = Callable[[StringInput], str | None]

type Validator[T] = Callable[[T], str | None]


def _always_none_string_validator(_result: StringInput) -> None:
    return None


@dataclass(frozen=True)
class StringPrompt:
    message: str
    string_validator: StringValidator | None
    formatter: Callable[[str], str] | None = field(kw_only=True, default=None)
    ps1: str | None = field(kw_only=True, default=None)

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
        raw_string_input = input(self.message + self._ps1)
        string_input = StringInput(self._formatter(raw_string_input), raw_string_input)

        while (invalid_input_string_message := self._string_validator(string_input)) is not None:
            raw_string_input = input(invalid_input_string_message + self.message + self._ps1)
            string_input = StringInput(self._formatter(raw_string_input), raw_string_input)

        return string_input if include_raw_input else string_input.formatted


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    converter: Callable[[str], ValueType]
    validator: Validator[ValueType] | None

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
        string_input = super().exec_string_input_loop(include_raw_input)
        converted_input = self.converter(string_input if isinstance(string_input, str) else string_input[0])

        while (invalid_input_string_message := self._validator(converted_input)) is not None:
            if invalid_input_string_message:
                print(invalid_input_string_message, end="")

            string_input = super().exec_string_input_loop(include_raw_input)
            converted_input = self.converter(string_input if isinstance(string_input, str) else string_input.formatted)

        return converted_input if isinstance(string_input, str) else (converted_input, string_input.raw_unformatted)
