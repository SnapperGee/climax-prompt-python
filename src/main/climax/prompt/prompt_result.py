r"""Provides classes of objects capable of indicating success or failure returned by a prompt.

See Also
--------
:mod:`climax.prompt.prompt` : Module that uses the classes this module exports
    wrap.
"""

from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class PromptResultSuccess[ValueType]:
    r"""Result of an input string that converted successfully.

    Intended for use as part of the return type of
    :meth:`climax.prompt.Prompt.exec_input_loop`.

    See Also
    --------
    :class:`PromptResult`, :meth:`climax.prompt.Prompt.exec_input_loop`
    """

    original_input_string: str
    r"""The raw unformatted original ``string``."""

    value: ValueType
    r"""The value of the converted formatted input string."""


@final
@dataclass(frozen=True, eq=False)
class PromptResultFailure:
    r"""Result of an input string that failed to convert.

    Intended for use as part of the return type of
    :meth:`climax.prompt.Prompt.exec_input_loop`.

    Exceptions compare by identity. To make equality useful, two instances of
    this class are equal if they have the same :attr:`original_input_string`
    and their :attr:`conversion_exception` values have the same type and the
    same ``args``.

    The hash uses only :attr:`original_input_string` and the type of
    :attr:`conversion_exception`. Equal instances always have equal hashes, as
    Python requires. Instances that differ only in the exception ``args`` have
    the same hash but are not equal. This choice also means that the hash does
    not raise ``TypeError`` when the exception ``args`` contain unhashable
    objects.

    See Also
    --------
    :class:`PromptResult`, :meth:`climax.prompt.Prompt.exec_input_loop`
    """

    original_input_string: str
    r"""The raw unformatted original ``string``."""

    conversion_exception: Exception
    r"""The exception thrown during conversion."""

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if not isinstance(other, PromptResultFailure):
            return NotImplemented

        return (
            self.original_input_string == other.original_input_string
            and type(self.conversion_exception) is type(other.conversion_exception)
            and self.conversion_exception.args == other.conversion_exception.args
        )

    def __hash__(self) -> int:
        return hash((self.original_input_string, type(self.conversion_exception)))


type PromptResult[ValueType] = PromptResultSuccess[ValueType] | PromptResultFailure
r"""Result of converting an input string.

Either a :class:`PromptResultSuccess`, which holds the converted value, or a
:class:`PromptResultFailure`, which holds the exception.

Intended for use as the return type of
:meth:`climax.prompt.Prompt.exec_input_loop`.

See Also
--------
:class:`PromptResultSuccess`, :class:`PromptResultFailure`, :meth:`climax.prompt.Prompt.exec_input_loop`
"""
