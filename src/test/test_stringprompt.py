from typing import Final

from climax.prompt import StringPrompt


class TestStringPrompt:
    def test_stringprompt_fields(self) -> None:
        message: Final = "Input a palidrome.\n"
        string_validator: Final = lambda string: string == string[::-1]
        invalid_string_message_generator: Final = (
            lambda raw_string, _: f'"{raw_string}" is not a palindrome.\n'
        )
        formatter: Final = lambda string: string.strip()
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
