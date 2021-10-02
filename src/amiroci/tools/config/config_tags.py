from enum import Enum, auto

class ConfTag(Enum):
    Modules = auto()
    Apps = auto()
    Options = auto()
    Dependencies = auto()
    IncludeOptions = auto()
    ExcludeOptions = auto()
    MakeOptions = auto()
    with_value = auto()
    requires = auto()
    requires_all = auto()
    to_be = auto()
