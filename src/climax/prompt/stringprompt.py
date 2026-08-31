from collections.abc import Callable
from dataclasses import dataclass, field

@dataclass(frozen=True)
class StringPrompt:
    message: str
    string_validator: Callable[[str], bool] | None
    invalid_string_message_generator: Callable[[str], str] | None
    formatter: Callable[[str], str] | None = field(kw_only=True, default=None)
    ps1: str | None = field(kw_only=True, default=None)
