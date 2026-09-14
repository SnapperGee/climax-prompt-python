# Climax Prompt

Prompt for input via the CLI.

[![python badge]][python website]
[![pytest badge]][pytest website]
[![ruff badge]][ruff website]
[![Sphinx][sphinx badge]][sphinx website]
[![poetry badge]][poetry website]
[![Git][git badge]][git website]
[![GitLab][gitlab badge]][gitlab repo]
[![github badge]][github repo]
[![MIT][mit shield]][mit license]

## Synopsis

This package exports primarily 2 classes that contain the majority of its
functionality. The `Prompt` and `StringPrompt` classes. The main difference
between the 2 is that `StringPrompt`s only processes strings while `Prompt`s
can process any arbitrary type.

The `StringPrompt.exec_string_input_loop(...)` and `Prompt.exec_input_loop(...)`
methods of each class create a loop that prompts a user for input and will
reprompt until valid input is inputted and return that inputted string or value.

## Usage Examples

### `StringPrompt` Usage Example

```python
from climax.prompt import PromptStringInput, StringPrompt


def is_palindrome(strings: StringInput) -> str | None:
    return (
        f'Provided input is not a palindrome: "{strings.unformatted}"\n'
        if strings.formatted != strings.formatted[::-1]
        else None
    )


palindrome_prompt = StringPrompt(
    "Input a palindrome...\n",
    is_palindrome,
    formatter=lambda string_input: string_input.strip().lower(),
    ps1=">>> ",
)

# the formatted input that passes the string prompt's validation and the original
# # raw string input will be retrieved
formatted_palindrome_string_input, original_palindrome_string_input: PromptStringInput = palindrome_prompt.exec_string_input_loop()

print(f'You inputted the palindrome: "{formatted_palindrome_string_input}"')
```

Calling the `StringPrompt.exec_string_input_loop(...)` method will result in the
following process:

1. The `StringPrompt.message` to be printed to stdout followed by the
   `StringPrompt.ps1` if set.

1. The string inputted to stdin then gets passed to the
   `StringPrompt.formatter(str)`.

1. The formatted and raw unformatted original input string then gets passed to
   the `StringPrompt.string_validator`.

1. If validation passes (the `StringPrompt.string_validator` returns
   `None`) then both the formatted and original unformatted string input gets returned.

1. If validation fails (the `StringPrompt.string_validator` returns a
   string error message) then the string error message gets printed to stdout
   and the process is repeated.

When the method in the example above is called this will result in the following
prompt in the terminal:

```text
Input a palindrome...
>>> slITher                                   # simulated user input
Provided input is not a palindrome: "slITher" # raw unformatted original string used in error message
Input a palindrome...
>>> level                                     # simulated user input
You inputted the palindrome: "level"
```

### `Prompt` Usage Example

```python
from climax.prompt import Prompt, PromptInput, StringInput


def string_is_integer(strings: StringInput) -> str | None:
    return None if strings.formatted.isdecimal() else f'Provided input is not an integer: "{strings.original}"\n'


def is_positive_even_integer(integer: int) -> str | None:
    if integer <= 0:
        return f"Integer isn't positive: {integer}\n"

    if integer % 2 != 0:
        return f"Integer isn't even: {integer}\n"

    return None


positive_even_integer_prompt = Prompt[int](
    "Input a positive even integer: ",
    string_is_integer,
    lambda string_input: int(string_input),  # could also just have passed `int` constructor method directly
    is_positive_even_integer,
    formatter=str.strip,
)

positive_even_integer_prompt_result: PromptResult = positive_even_integer_prompt.exec_input_loop()

if positive_even_integer_prompt_result.conversion_exception:
    print("Error converting input to an int:", positive_even_integer_prompt_result.original_input_string)

print("You inputted the positive even integer:", positive_even_integer_prompt_result.value)
```

Calling the `Prompt.exec_input_loop(...)` method will result in the same process
outlined above when `StringPrompt.exec_string_input_loop(...)` is called, except
it performs additional conversion of the string input and validation on that
converted string input as outlined below ***if*** string input validation passes
(otherwise the reprompt process is identical):

1. The *formatted* validated string input is passed to the
   `Prompt.converter(str)`.

1. If an exception occurs during conversion, then a `PromptInput` is returned
   with the original input string and the `Exception` that was raised.

1. If conversion succeeds without raising an exception, the string input is
   then passed to the `Prompt.validator(...)`.

1. If validation passes (the `Prompt.validator(...)` returns `None`) then a
   `PromptInput` containing the original input string and its converted value
   is returned.

1. If validation fails (the `Prompt.validator(...)` returns a string error
   message) then the error message gets printed to stdout and the process is
   repeated.

When the method in the example above is called this will result in the following
prompt in the terminal:

```text
Input a positive even integer:    slither          # simulated user input
Provided input is not an integer: "slither"        # formatted string input is used in this message
Input a positive even integer: -34                 # simulated user input
Integer isn't positive: -34
Input a positive even integer: 7                   # simulated user input
Integer isn't even: 7
Input a positive even integer: 22                  # simulated user input
You inputted the positive even integer: 22
```

## Installing Package

This package is available on pypi and can be installed via any of the standard
methods:

```sh
# via poetry
poetry add climax-prompt

# via uv
uv add climax-prompt

# via pip
pip install climax-prompt
```

## Repo

### Tooling Tasks

The repo for this project uses [ruff][ruff website] and [mypy][mypy website] for
linting, [ruff][ruff website] for formatting, [pytest][pytest website] for
testing, and [sphinx][sphinx website] (with [numpydoc][numpydoc website]) for
generating API documentation.

All repo tasks can be executed via the `make` targets listed below:

- `setup` - Installs all package dependencies and pre-commit hook(s).
- `lint` - This runs both the `ruff` checker and `mypy` static type checker.
- `format` - Formats source code with `ruff`.
- `test` - Runs unit tests.
- `serve` - Generates and serves html API docs on `127.0.0.1:8000`.
- `readme` - Generate `source/README.rst` by using `pandoc` to convert the root `README.md` to rst.

In addition to the `make` targets listed above, all sphinx `make` targets are
available and valid as well.

### Remotes

The primary remote repo for this package is hosted on [gitlab][gitlab repo], but
is also mirrored to [github][github repo].

## MIT License

This package is licensed under the MIT license and can be found in
[LICENSE.txt][mit license].

[python badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54 "Python"
[python website]: https://www.python.org/ "Python"
[pytest badge]: https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3 "PyTest"
[pytest website]: https://docs.pytest.org/en/stable/ "PyTest"
[ruff badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge "Ruff"
[ruff website]: https://docs.astral.sh/ruff/ "Ruff"
[sphinx website]: https://www.sphinx-doc.org/ "Sphinx"
[sphinx badge]: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg?style=for-the-badge "Sphinx"
[numpydoc website]: https://numpydoc.readthedocs.io/en/latest/ "numpydoc"
[mypy website]: https://mypy-lang.org/ "mypy"
[poetry badge]: https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D "Poetry"
[poetry website]: https://python-poetry.org/ "Poetry"
[git badge]: https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white "git"
[git website]: https://git-scm.com/ "git"
[gitlab badge]: https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white "GitLab"
[gitlab repo]: https://gitlab.com/SnapperGee/climax-prompt-python "GitLab repo"
[github badge]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white "GitHub"
[github repo]: https://github.com/SnapperGee/climax-prompt-python "GitHub"
[mit shield]: https://img.shields.io/badge/license-MIT-green?style=for-the-badge "MIT"
[mit license]: ./LICENSE.txt "MIT"
