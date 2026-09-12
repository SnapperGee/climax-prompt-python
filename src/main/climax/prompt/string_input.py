from typing import NamedTuple


class StringInput(NamedTuple):
    r"""A container for a formatted ``string`` and the original unformatted ``string``."""

    formatted: str
    r"""A formatted ``string``."""

    original: str
    r"""The raw unformatted original ``string``."""
