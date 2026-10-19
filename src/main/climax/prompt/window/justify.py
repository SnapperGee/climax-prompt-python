from enum import Enum, auto, unique


@unique
class Justify(Enum):
    START = auto()
    CENTER = auto()
    END = auto()
