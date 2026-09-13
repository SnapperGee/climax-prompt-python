from dataclasses import dataclass
from typing import Self, final


@final
@dataclass(frozen=True)
class PromptResult[ValueType]:
    original_input_string: str
    value: ValueType | None = None
    conversion_exception: Exception | None = None

    def __post_init__(self) -> None:
        if self.conversion_exception and self.value is not None:
            raise ValueError(
                f"{type(self).__name__}: truthy `conversion_exception` with "
                f"non-None `value`:\n{self.value=}\n\n{self.conversion_exception!r}"
            )

    @classmethod
    def create(cls, original_input_string: str, value_or_conversion_exception: ValueType | Exception) -> Self:
        return (
            cls(original_input_string, None, value_or_conversion_exception)
            if isinstance(value_or_conversion_exception, Exception)
            else cls(original_input_string, value_or_conversion_exception)
        )
