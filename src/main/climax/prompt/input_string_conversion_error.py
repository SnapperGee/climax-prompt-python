from typing import Final, final


@final
class InputStringConversionError(Exception):
    r"""Wraps exception raised during string input conversion."""

    cause: Final[Exception]

    def __init__(self, cause: Exception, message: str | None = None) -> None:
        super().__init__(f"Input string conversion failed: {cause}" if message is None else message)
        self.__cause__ = cause
        self.cause = cause
