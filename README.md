# Climax Prompt

Prompt for input via the CLI.

[![python badge]][python website]
[![pytest badge]][pytest website]
[![ruff badge]][ruff website]
[![poetry badge]][poetry website]
![Git][git badge]
[![GitLab][gitlab badge]][gitlab repo]
[![github badge]][github repo]
[![MIT][mit shield]][mit website]

## Synopsis

This package exports primarily 2 classes that contain the majority of its
functionality. The `StringPrompt` and `Prompt` classes. The main difference
between the 2 is that `StringPrompt`s only processes strings while `Prompt`s
can process any arbitrary type.

The `StringPrompt.exec_string_input_loop(...)` and `Prompt.exec_input_loop(...)`
methods of each class create a loop that prompts a user for input and will
reprompt until valid input is inputted and return that inputted string.

## `StringPrompt` Usage Examples

The `StringPrompt` class can be used as such:

```python
from climax.prompt import StringPrompt

palindrome_prompt = StringPrompt(
    "Input a palindrome...\n",
    lambda string_input: string_input == string_input[::-1],
    lambda invalid_formatted_string_input, _invalid_raw_string_input: f'Provided input is not a palindrome: "{invalid_formatted_string_input}"\n',
    formatter=lambda string_input: string_input.strip().lower(),
    ps1=">>> ",
)

# the formatted input that passes the string prompt's validation will be retrieved
inputted_palindrome = palindrome_prompt.exec_string_input_loop()

print(f'You inputted the palindrome: "{inputted_palindrome}"')
```

Calling the `StringPrompt.exec_string_input_loop(...)` method will result in the
following process:

1. the `StringPrompt.message` to be printed to stdout followed by the
   `StringPrompt.ps1` if set.

1. the string inputted to stdin then gets passed to the
   `StringPrompt.formatter(str)` if set otherwise the string remains unchanged.

1. The formatted (or unformatted) string then gets passed to the
   `StringPrompt.string_validator(str)` string predicate.

1. If validation passes (the `StringPrompt.string_validator(str)` string
   predicate returns `True`) then the formatted string input or both the
   formatted and unformatted string input gets returned.

1. If validation fails (the `StringPrompt.string_validator(str)` string
   predicate returns `False`) then the formatted and unformatted string input
   gets passed to the `StringPrompt.invalid_string_message_generator(str,str)`
   to create a string that gets printed to stdout and the process is repeated.

It's important to note that string input gets formatted ***before*** being
validated.

When the method in the example above is called this will result in the following
prompt in the terminal:

```text
Input a palindrome...
>>> slITher                 # simulated user input
Provided input is not a palindrome: "slither" # not that the formatted string input is used in the message
Input a palindrome...
>>> level                   # simulated user input
You inputted the palindrome: "level"
```

## `Prompt` Usage Example

The `Prompt` class can be used as such:

```python
from climax.prompt import Prompt

positive_even_integer_prompt = Prompt[int](
    "Input a positive even integer: ",
    lambda string_input: string_input.isdigit(), # could also have just passed `str.isdigit`
    lambda invalid_formatted_string_input, _invalid_raw_string_input: f'Provided input is not an integer: "{invalid_formatted_string_input}"\n',
    lambda string_input: int(string_input), # could also just have passed `int`
    lambda int_input: int_input > 0 and int_input % 2 == 0,
    lambda invalid_int_input: f"Inputted integer isn't positive and/or even: {invalid_int_input}"
    formatter=str.strip
)

# the input that passes the prompt's validation will be retrieved
inputted_positive_even_integer: int = positive_even_integer_prompt.exec_input_loop()

print("You inputted the positive even integer: ", inputted_positive_even_integer)
```

Calling the `Prompt.exec_input_loop(...)` method will result in the same process
outlined above when `StringPrompt.exec_string_input_loop(...)` is called, except
it performs additional conversion of the string input and validation on that
converted string input as outlined below ***if*** string input validation passes
(otherwise the reprompt process is identical):

1. The *formatted* validated string input is passed to the
   `Prompt.converter(str)`.

1. The converted string input is then passed to the `Prompt.validator(...)`.

1. If validation passes (the `Prompt.validator(...)` predicate returns `True`)
   then the *converted* string input or both the *converted* and unformatted
   string input gets returned.

1. If validation fails (the `Prompt.validator(...)` predicate returns `False`)
   then the converted string input gets passed to the
   `Prompt.invalid_value_message_generator(...)` to create a string that gets
   printed to stdout and the process is repeated.

When the method in the example above is called this will result in the following
prompt in the terminal:

```text
Input a positive even integer: slither             # simulated user input
Provided input is not an integer: "slither"
Input a positive even integer: -33                 # simulated user input
Inputted integer isn't positive and/or even: -33
Input a positive even integer: 21                  # simulated user input
You inputted the positive even integer: 21
```

[python badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54 "Python"
[python website]: https://www.python.org/ "Python"
[pytest badge]: https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3 "PyTest"
[pytest website]: https://docs.pytest.org/en/stable/ "PyTest"
[ruff badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge "Ruff"
[ruff website]: https://docs.astral.sh/ruff/ "Ruff"
[poetry badge]: https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D "Poetry"
[poetry website]: https://python-poetry.org/ "Poetry"
[git badge]: https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white "Git"
[gitlab badge]: https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white "GitLab repo"
[gitlab repo]: https://gitlab.com/SnapperGee/termite-invasion "GitLab repo"
[github badge]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white "GitHub"
[github repo]: https://github.com/SnapperGee/wedaviz "GitHub"
[mit shield]: https://img.shields.io/badge/license-MIT-green?style=for-the-badge "MIT"
[mit website]: https://opensource.org/license/mit "MIT"
