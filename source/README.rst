Climax Prompt
=============

Prompt for input via the CLI.

|python badge| |pytest badge| |ruff badge| |Sphinx| |poetry badge| |Git|
|GitLab| |github badge| |MIT|

Synopsis
--------

This package exports primarily 2 classes that contain the majority of
its functionality. The ``StringPrompt`` and ``Prompt`` classes. The main
difference between the 2 is that ``StringPrompt``\ s only processes
strings while ``Prompt``\ s can process any arbitrary type.

The ``StringPrompt.exec_string_input_loop(...)`` and
``Prompt.exec_input_loop(...)`` methods of each class create a loop that
prompts a user for input and will reprompt until valid input is inputted
and return that inputted string or value.

Usage Examples
--------------

``StringPrompt`` Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from climax.prompt import StringInput, StringPrompt


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

   # the formatted input that passes the string prompt's validation will be retrieved
   inputted_palindrome: str = palindrome_prompt.exec_string_input_loop()

   print(f'You inputted the palindrome: "{inputted_palindrome}"')

Calling the ``StringPrompt.exec_string_input_loop(...)`` method will
result in the following process:

1. The ``StringPrompt.message`` to be printed to stdout followed by the
   ``StringPrompt.ps1`` if set.

2. The string inputted to stdin then gets passed to the
   ``StringPrompt.formatter(str)``.

3. The formatted and raw unformatted original input string then gets
   passed to the ``StringPrompt.string_validator``.

4. If validation passes (the ``StringPrompt.string_validator`` returns
   ``None``) then the formatted string input or both the formatted and
   unformatted string input gets returned.

5. If validation fails (the ``StringPrompt.string_validator(str)``
   returns a string error message) then the string error message gets
   printed to stdout and the process is repeated.

When the method in the example above is called this will result in the
following prompt in the terminal:

.. code:: text

   Input a palindrome...
   >>> slITher                                   # simulated user input
   Provided input is not a palindrome: "slITher" # raw unformatted original string used in error message
   Input a palindrome...
   >>> level                                     # simulated user input
   You inputted the palindrome: "level"

``Prompt`` Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from climax.prompt import Prompt, StringInput


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

   # the input that passes the prompt's validation will be retrieved
   inputted_positive_even_integer: int = positive_even_integer_prompt.exec_input_loop()

   print("You inputted the positive even integer:", inputted_positive_even_integer)

Calling the ``Prompt.exec_input_loop(...)`` method will result in the
same process outlined above when
``StringPrompt.exec_string_input_loop(...)`` is called, except it
performs additional conversion of the string input and validation on
that converted string input as outlined below **if** string input
validation passes (otherwise the reprompt process is identical):

1. The *formatted* validated string input is passed to the
   ``Prompt.converter(str)``.

2. The converted string input is then passed to the
   ``Prompt.validator(...)``.

3. If validation passes (the ``Prompt.validator(...)`` returns ``None``)
   then the *converted* string input or both the *converted* and raw
   unformatted original string input gets returned.

4. If validation fails (the ``Prompt.validator(...)`` returns a string
   error message) then the error message gets printed to stdout and the
   process is repeated.

When the method in the example above is called this will result in the
following prompt in the terminal:

.. code:: text

   Input a positive even integer:    slither          # simulated user input
   Provided input is not an integer: "slither"        # formatted string input is used in this message
   Input a positive even integer: -34                 # simulated user input
   Integer isn't positive: -34
   Input a positive even integer: 7                   # simulated user input
   Integer isn't even: 7
   Input a positive even integer: 22                  # simulated user input
   You inputted the positive even integer: 22

Installing Package
------------------

This package is available on pypi and can be installed via any of the
standard methods:

.. code:: sh

   # via poetry
   poetry add climax-prompt

   # via uv
   uv add climax-prompt

   # via pip
   pip install climax-prompt

Repo
----

Tooling Tasks
~~~~~~~~~~~~~

The repo for this project uses `ruff <https://docs.astral.sh/ruff/>`__
and `mypy <https://mypy-lang.org/>`__ for linting,
`ruff <https://docs.astral.sh/ruff/>`__ for formatting,
`pytest <https://docs.pytest.org/en/stable/>`__ for testing, and
`sphinx <https://www.sphinx-doc.org/>`__ (with
`numpydoc <https://numpydoc.readthedocs.io/en/latest/>`__) for
generating API documentation.

All repo tasks can be executed via the ``make`` targets listed below:

-  ``setup`` - Installs all package dependencies and pre-commit hook(s).
-  ``lint`` - This runs both the ``ruff`` checker and ``mypy`` static
   type checker.
-  ``format`` - Formats source code with ``ruff``.
-  ``test`` - Runs unit tests.
-  ``serve`` - Generates and serves html API docs on ``127.0.0.1:8000``.

In addition to the ``make`` targets listed above, all ``sphinx`` targets
are available and valid as well.

Remotes
~~~~~~~

The primary remote repo for this package is hosted on
`gitlab <https://gitlab.com/SnapperGee/climax-prompt-python>`__, but is
also mirrored to
`github <https://github.com/SnapperGee/climax-prompt-python>`__.

MIT License
-----------

This package is licensed under the MIT license and can be found in
`LICENSE.txt <./LICENSE.txt>`__.

.. |python badge| image:: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
   :target: https://www.python.org/
.. |pytest badge| image:: https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3
   :target: https://docs.pytest.org/en/stable/
.. |ruff badge| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge
   :target: https://docs.astral.sh/ruff/
.. |Sphinx| image:: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg?style=for-the-badge
   :target: https://www.sphinx-doc.org/
.. |poetry badge| image:: https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D
   :target: https://python-poetry.org/
.. |Git| image:: https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white
   :target: https://git-scm.com/
.. |GitLab| image:: https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white
   :target: https://gitlab.com/SnapperGee/climax-prompt-python
.. |github badge| image:: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
   :target: https://github.com/SnapperGee/climax-prompt-python
.. |MIT| image:: https://img.shields.io/badge/license-MIT-green?style=for-the-badge
   :target: ./LICENSE.txt
