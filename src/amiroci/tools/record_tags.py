from enum import Enum, auto

class RecordEntry(Enum):
    Module = auto()
    Duration = auto()
    CPU_Time = auto()
    Default = '-'
    CompilerState = auto()
    Message = auto()
    Error = 'error'
    Warning = 'warning'
    Info = 'note'
    ErrorMsg  = auto()
    WarnMsg = auto()
    InfoMsg = auto()
