from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Final


@dataclass(frozen=True)
class StringPrompt:
    message: str
    string_validator: Callable[[str], bool] | None
    invalid_string_message_generator: Callable[[str], str] | None
    formatter: Callable[[str], str] | None = field(kw_only=True, default=None)
    ps1: str | None = field(kw_only=True, default=None)

    def exec_string_input_loop(self) -> str:
        ps1: Final = self.ps1 if self.ps1 is not None else ""
        _input = input(self.message + ps1)
        formatted_input = self.formatter(_input) if self.formatter else _input

        if self.string_validator:
            while not self.string_validator(formatted_input):
                invalid_input_string = (
                    self.invalid_string_message_generator(_input)
                    if self.invalid_string_message_generator
                    else ""
                )

                _input = input(invalid_input_string + self.message + ps1)
                formatted_input = self.formatter(_input) if self.formatter else _input

        return formatted_input
