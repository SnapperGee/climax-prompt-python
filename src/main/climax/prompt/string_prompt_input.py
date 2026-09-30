r"""Exports a class capable of instantiating objects that can contain a formatted and original unformatted string.

See Also
--------
:mod:`climax.prompt.validator` : Module that uses the class this module exports.
"""

from typing import NamedTuple


class StringPromptInput(NamedTuple):
    r"""A container for a formatted ``string`` and the original unformatted ``string``.

    Intended for use as the return type of the :meth:`climax.prompt.StringPrompt.exec_string_input_loop`.

    See Also
    --------
    :func:`climax.prompt.validator.StringValidator` : Module that uses this
        class as a type argument for a generic type.
    """

    formatted: str
    r"""A formatted ``string``."""

    original: str
    r"""The raw unformatted original ``string``."""
