from collections.abc import Callable

from .string_prompt_input import StringPromptInput

type Validator[T] = Callable[[T], str | None]
r"""A function that validates a value.

If validation fails then a ``string`` explaining why it failed should be
returned, otherwise ``None`` should be returned.
"""

type StringValidator = Validator[StringPromptInput]
r"""A function that validates a :class:`StringInput`.

If validation fails then a ``string`` explaining why it failed should be
returned, otherwise ``None`` should be returned.

See Also
--------
:obj:`Validator` : The type this type is based on.
"""
