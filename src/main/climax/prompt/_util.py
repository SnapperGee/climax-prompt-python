def identity[T](arg: T) -> T:
    r"""Function that returns the argument passed to it."""
    return arg


def always_none_returning_function(_: object) -> None:
    r"""Consumes an ``object`` and returns ``None``."""
    return
