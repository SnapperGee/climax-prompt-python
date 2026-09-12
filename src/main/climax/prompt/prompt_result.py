from dataclasses import dataclass
from typing import final


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
