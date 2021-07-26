from abc import ABC
from dataclasses import dataclass

from amirotest.model.aos_argument import AosArgument, UserArgument


class WrongArgumentCount(Exception):
    pass

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
        return self._get_substitution_flag_names(self.args)

    def _get_substitution_flag_names(self, args: list[AosArgument]) -> list[str]:
        flags = []
        for arg in args:
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


class GlobalFlag(AosFlag):
    pass


class UserFlag(AosFlag):
    pass
    def __init__(self, flag_name, arg_str):
        """Add substitution flag to argument"""
        flag_args = arg_str.split(" ")
        if len(flag_args) != 1:
            raise WrongArgumentCount(f"Cannot process {len(flag_args)} arguments!\nGiven arguments:{flag_args}")
        u_arg = UserArgument(arg_str)
        super().__init__(flag_name, u_arg.name)
