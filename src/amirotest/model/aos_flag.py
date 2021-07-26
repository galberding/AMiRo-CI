from abc import ABC
from dataclasses import dataclass

from amirotest.model.aos_argument import AosArgument


@dataclass
class AosFlag():
    name: str
    argument_str: str

    def __post_init__(self):
        splitted_args = self.argument_str.split(" ")
        self.args = [AosArgument(arg) for arg in splitted_args]

    def is_resolved(self) -> bool:
        return len(self.get_substitution_flag_names()) == 0

    def get_substitution_flag_names(self) -> list[str]:
        """Returns all substitution flags that are found in the arguments."""
        flags = []
        for arg in self.args:
            if not arg.is_resolved():
                flags.append(arg.get_substitution_flag())
        return flags

    def resolve(self, flag: 'AosFlag') -> bool:
        for arg in self.args:
            arg.resolve(flag.name, flag.argument_str)
        return self.is_resolved()

    def get_type(self) -> str:
        """Retrun type description for listing in config"""
        return type(self).__name__

    def __str__(self) -> str:
        return f'{self.name}: {self.args}'
    __repr__ = __str__

@dataclass
class GlobalFlag(AosFlag):
    pass

@dataclass
class UserFlag(AosFlag):
    pass
