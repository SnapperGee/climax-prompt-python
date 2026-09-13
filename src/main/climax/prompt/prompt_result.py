from dataclasses import dataclass
from typing import final


def _exception_key(exception: Exception | None) -> tuple[type[Exception], tuple[object, ...]] | None:
    if exception is None:
        return None

    return (type(exception), exception.args)


@final
@dataclass(frozen=True)
class PromptResult[ValueType]:
    original_input_string: str
    value: ValueType | None
    conversion_exception: Exception | None = None

    def __post_init__(self) -> None:
        if self.conversion_exception and self.value is not None:
            raise ValueError(
                f"{type(self).__name__}: truthy `conversion_exception` with "
                f"non-None `value`:\n{self.value=}\n\n{self.conversion_exception!r}"
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PromptResult):
            return NotImplemented

        if self.original_input_string != other.original_input_string or self.value != other.value:
            return False

        return _exception_key(self.conversion_exception) == _exception_key(other.conversion_exception)

    def __hash__(self) -> int:
        return hash((self.original_input_string, self.value, _exception_key(self.conversion_exception)))
