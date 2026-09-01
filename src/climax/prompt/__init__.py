from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import final

from .stringprompt import StringPrompt, _always_true_predicate


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    converter: Callable[[str], ValueType]
    validator: Callable[[ValueType], bool] | None
    invalid_value_message_generator: Callable[[ValueType], str] | None

    @cached_property
    def _validator(self) -> Callable[[ValueType], bool]:
        return self.validator or _always_true_predicate

    def exec_input_loop(self) -> ValueType:
        string_input = super().exec_string_input_loop()
        converted_input = self.converter(string_input)

        while not self._validator(converted_input):
            if self.invalid_value_message_generator:
                print(self.invalid_value_message_generator(converted_input), end=None)

            string_input = super().exec_string_input_loop()
            converted_input = self.converter(string_input)

        return converted_input
