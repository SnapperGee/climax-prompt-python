from typing import NamedTuple


class StringPromptInput(NamedTuple):
    r"""A container for a formatted ``string`` and the original unformatted ``string``.

    Intended for use as the return type of the :meth:`climax.prompt.StringPrompt.exec_string_input_loop`.
    """

    formatted: str
    r"""A formatted ``string``."""

    original: str
    r"""The raw unformatted original ``string``."""
