r"""Provides types defining ``Callable``s that can be used as validator functions."""

from collections.abc import Callable

from .string_prompt_input import StringPromptInput

type Validator[T] = Callable[[T], str | None]
r"""A function that validates a value.

If validation fails then a ``string`` explaining why it failed should be
returned, otherwise ``None`` should be returned.
"""

type StringValidator = Validator[StringPromptInput]
r"""A function that validates a :class:`StringPromptInput`.

If validation fails then a ``string`` explaining why it failed should be
returned, otherwise ``None`` should be returned.

See Also
--------
:class:`Validator` : The type this type is based on.
"""
