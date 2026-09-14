from typing import Final, final


@final
class InputStringConversionError(Exception):
    r"""Wraps exception raised during string input conversion."""

    cause: Final[Exception]

    def __init__(self, cause: Exception, message: str | None = None) -> None:
        super().__init__(f"Input string conversion failed: {cause}" if message is None else message)
        self.__cause__ = cause
        self.cause = cause

    def equals(self, other: object) -> bool:
        return self is other or (
            isinstance(other, InputStringConversionError)
            and type(self.cause) is type(other.cause)
            and self.args == other.args
        )
