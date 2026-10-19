from enum import Enum, auto, unique


@unique
class Position(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTHEAST = auto()
    SOUTHEAST = auto()
    SOUTHWEST = auto()
    NORTHWEST = auto()
    CENTER = auto()
