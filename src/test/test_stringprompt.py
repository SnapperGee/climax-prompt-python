import builtins
from typing import Final
from unittest.mock import call, patch

from climax.prompt import StringPrompt


class TestStringPrompt:
    def test_stringprompt_fields(self) -> None:
        message: Final = "Input a palindrome.\n"
        string_validator: Final = lambda string: string == string[::-1]
        def invalid_string_message_generator(raw_string: str, _: str) -> str:
            return f'"{raw_string}" is not a palindrome.\n'
        def formatter(string: str) -> str:
            return string.strip()
        ps1: Final = ">>> "

        string_prompt: Final = StringPrompt(
            message,
            string_validator,
            invalid_string_message_generator,
            formatter=formatter,
            ps1=ps1,
        )

        assert string_prompt.message is message
        assert string_prompt.string_validator is string_validator
        assert (
            string_prompt.invalid_string_message_generator
            is invalid_string_message_generator
        )
        assert string_prompt.formatter is formatter
        assert string_prompt.ps1 is ps1

    def test_stringprompt_default_field_values(self) -> None:
        string_prompt: Final = StringPrompt(
            "",
            lambda _: True,
            lambda _, __: "",
        )

        assert string_prompt.formatter is None
        assert string_prompt.ps1 is None

    def test_stringprompt_default_format_method_is_identity_function(self) -> None:
        string: Final = "snake"

        string_prompt: Final = StringPrompt(
            "",
            lambda _: True,
            lambda _, __: "",
        )

        assert string_prompt.format(string) is string

    def test_stringprompt_exec_string_input_loop(self) -> None:
        message: Final = "Enter an integer: "
        def invalid_message_generator(raw_input: str, _: str) -> str:
            return f'"{raw_input} is not an integer.\n"'

        string_prompt: Final = StringPrompt(
            message,
            lambda string: string.isdigit(),
            invalid_message_generator,
        )

        invalid_input: Final = "abc"
        valid_input: Final = "123"

        with patch.object(builtins, "input", side_effect=(invalid_input, valid_input)) as mock_input:
            result: Final = string_prompt.exec_string_input_loop()

        assert result == valid_input
        assert mock_input.call_args_list == [
            call(message),
            call(invalid_message_generator(invalid_input, "") + message),
        ]
