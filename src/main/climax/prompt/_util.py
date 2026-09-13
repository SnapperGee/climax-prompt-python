from typing import Literal


def string_identity_function(string: str) -> str:
    r"""An identity function that consumes a ``string`` and returns the same ``string``."""
    return string


def always_none_returning_function(_: object) -> None:
    r"""A function that consumes an ``object`` and returns ``None``."""
    return


def always_true_returning_function(_: object) -> Literal[True]:
    return True
