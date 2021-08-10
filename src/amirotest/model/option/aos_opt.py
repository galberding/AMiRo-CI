from abc import ABC
from dataclasses import dataclass
from typing import Any

from amirotest.model.argument import UserArgument, AosArgument

class WrongArgumentCount(Exception):
    pass

@dataclass
class AosOption():
    name: str
    argument_str: str

    def __post_init__(self):
        self.args = []
        self._reset_args_from_argumnet_str()

    def reset_resolution(self):
        """Perform new argument initialization and variable extraction.
        """
        self._reset_args_from_argumnet_str()
        self.extract_variables()

    def _reset_args_from_argumnet_str(self):
        self.args.clear()       # TODO: Is it required?
        splitted_args = self.argument_str.split(" ")
        self.args = [AosArgument(arg) for arg in splitted_args]

    def resolve(self, flag: 'AosOption') -> bool:
        for arg in self.args:
            arg.resolve(flag.name, flag.argument_str)
        return self.is_resolved()

    def is_resolved(self) -> bool:
        return len(self.get_substitution_opt_names()) == 0

    def get_substitution_opt_names(self) -> list[str]:
        """Returns all substitution option names that are found in the arguments."""
        return self._get_substitution_option_names(self.args)

    def _get_substitution_option_names(self, args: list[AosArgument]) -> list[str]:
        flags = []
        for arg in args:
            if not arg.is_resolved():
                flags.append(arg.search_substitution_option())
        return flags

    def extract_variables(self) -> list['AosVariable']:
        aos_vars = []
        for arg in self.args:
            variable_description = arg.extract_variable(self.name)
            if variable_description:
                aos_vars.append(AosVariable(variable_description[0], variable_description[1]))
        return aos_vars

    def get_build_option(self) -> str:
        if len(self.args) == 1:
            return f"-D{self.name}={self.args[0]}"
        else:
            raise NotImplementedError()

    def get_type(self) -> str:
        """Retrun type description for listing in config"""
        return type(self).__name__

    def __str__(self) -> str:
        return f'{self.name}: {self.args}'
    __repr__ = __str__


class AosVariable(AosOption):
    pass

class ConfVariable(AosOption):
    def __init__(self, flag_name, arg_str):
        flag_name = f"{flag_name}_VAR"
        super().__init__(flag_name, arg_str)

class MakeGlobalOption(AosOption):
    pass


class MakeUserOption(AosOption):
    def __init__(self, flag_name, arg_str):
        """Add substitution flag to argument"""
        flag_args = arg_str.split(" ")
        if len(flag_args) != 1:
            raise WrongArgumentCount(f"Cannot process {len(flag_args)} arguments!\nGiven arguments:{flag_args}")
        u_arg = UserArgument(arg_str)
        super().__init__(flag_name, u_arg.name)

class DefaultOpiton(AosOption):
    def __init__(self, name: str, arg_str: str, default: Any):
        self.default = default
        super().__init__(name, arg_str)