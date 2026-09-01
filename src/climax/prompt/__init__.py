from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import Literal, final

from .stringprompt import StringPrompt, _always_true_predicate


def _identity_function[T](arg: T) -> T:
    return arg


def _default_invalid_value_message_generator(_: object) -> Literal[""]:
    return ""


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    converter: Callable[[str], ValueType]
    validator: Callable[[ValueType], bool] | None
    invalid_value_message_generator: Callable[[ValueType], str] | None

    @cached_property
    def _validator(self) -> Callable[[ValueType], bool]:
        return self.validator if self.validator else _always_true_predicate

    @cached_property
    def _invalid_value_message_generator(self) -> Callable[[ValueType], str]:
        return (
            self.invalid_value_message_generator
            if self.invalid_value_message_generator
            else _default_invalid_value_message_generator
        )

    def exec_input_loop(self) -> ValueType:
        string_input = super().exec_string_input_loop()
        converted_input = self.converter(string_input)

        while not self._validator(converted_input):
            invalid_input_string = self._invalid_value_message_generator(
                converted_input
            )
            print(invalid_input_string, end=None)
            string_input = super().exec_string_input_loop()
            converted_input = self.converter(string_input)

        return converted_input
