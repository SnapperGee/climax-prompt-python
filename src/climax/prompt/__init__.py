from collections.abc import Callable
from dataclasses import dataclass, field
from typing import final

from .stringprompt import StringPrompt


@final
@dataclass(frozen=True)
class Prompt[ValueType](StringPrompt):
    converter: Callable[[str], ValueType]
    validator: Callable[[ValueType], bool] | None
    invalid_value_message_generator: Callable[[ValueType], str] | None
    normalizer: Callable[[ValueType], ValueType] | None = field(
        kw_only=True, default=None
    )
