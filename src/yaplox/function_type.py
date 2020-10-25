import enum


class FunctionType(enum.Enum):
    NONE = enum.auto()
    FUNCTION = enum.auto()
    INITIALIZER = enum.auto()
    METHOD = enum.auto()
