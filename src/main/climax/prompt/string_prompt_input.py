from typing import NamedTuple


class StringPromptInput(NamedTuple):
    r"""A container for a formatted ``string`` and the original unformatted ``string``."""

    formatted: str
    r"""A formatted ``string``."""

    original: str
    r"""The raw unformatted original ``string``."""
