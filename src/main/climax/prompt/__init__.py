r"""This package makes it possible to easily get validated command line prompt input from a user.

The :class:`~prompt.Prompt` and :class:`~string_prompt.StringPrompt` classes are
the 2 core abstractions exported by this package and will most likely be the
primary way users interface with this API.

The main difference between these 2 classes is that the
:class:`~string_prompt.StringPrompt` class only works with and processes
``string``s while the :class:`~prompt.Prompt` class is capable of working with
and processing any arbitrary types, not just ``string``s.
"""

from .prompt import Prompt
from .prompt_input import PromptInput
from .string_prompt import StringPrompt
from .string_prompt_input import StringPromptInput
from .validator import StringValidator, Validator

__all__ = ("Prompt", "PromptInput", "StringPrompt", "StringPromptInput", "StringValidator", "Validator")
