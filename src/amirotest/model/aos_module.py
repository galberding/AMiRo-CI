from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
import uuid

from amirotest.model.option import AosOption
from amirotest.model.option.aos_opt import DefaultOpiton

class OptionNotFoundException(Exception):
    pass

class AmbigousOptionError(Exception):
    pass

@dataclass(unsafe_hash=True)
class AosModule:
    name: str = field(init=False)
    uid: str = field(init=False, default="")
    path: Path
    options: list[AosOption] = field(init=False)

    def __post_init__(self):
        self.name = self.path.name
        self.options = []
        self.uid = str(uuid.uuid1())

    def add_options(self, options: list[AosOption]):
        opt_set = set(self.options)
        for opt in options:
            if opt not in opt_set:
                opt_set.add(opt)
            else:
                raise AmbigousOptionError(f"Option: {opt} already exists!")
        self.options += options

    def get_option_copy(self) -> list[AosOption]:
        return deepcopy(self.options)

    def is_resolved(self) -> bool:
        """Check if all options are resolved."""
        if not self.options:
            return True

        for option in self.options:
            if not option.is_resolved():
                return False
        return True

    def resolve(self):
        """Try to resolve all containing options.
        All substitution options needs to be provided
        in order to fully resolve all options.
        """
        if self.is_resolved():
            return

        u_opts = self.get_unresolved_options()
        sub_opts = self.get_substitution_options()
        # get substitution options

        for u_opt in u_opts:
            for s_opt in sub_opts:
                u_opt.resolve(s_opt)

    def get_unresolved_options(self) -> list[AosOption]:
        """Get all options with unresolved arguments"""
        u_options = []
        for option in self.options:
            if not option.is_resolved():
                u_options.append(option)
        return u_options

    def get_substitution_options(self) -> list[AosOption]:
        """Get Option contained in unresolved arguments.
        Also referred to as substitution option because their
        content is substituted into the argument"""
        sub_option_names = []
        u_options = self.get_unresolved_options()
        for u_option in u_options:
            sub_option_names += u_option.get_substitution_opt_names()
        sub_options = self.find_options_by_names(sub_option_names)
        return sub_options

    def find_options_by_names(self, option_names: list[str]) -> list[AosOption]:
        options = []
        for option_name in option_names:
            options.append(self.find_option_by_name(option_name))
        return options

    def find_option_by_name(self, option_name: str) -> AosOption:
        for option in self.options:
            if option.name == option_name:
                return option
        raise OptionNotFoundException(f"Cannot find {option_name}!")

    def dict_factory(self):
        return {self.name: 42}

    def to_default_config_dict(self) -> dict:
        conf = {}
        conf[self.name] = {}
        for option in self.options:
            if option.get_type() not in conf[self.name]:
                conf[self.name][option.get_type()] = {}
            if isinstance(option, DefaultOpiton):
                conf[self.name][option.get_type()][option.name] = \
                    [option.default]
            else:
                conf[self.name][option.get_type()][option.name] = \
                    [arg.name for arg in option.args]
        return conf


    def __str__(self) -> str:
        return f'{self.name}: {self.options}'
    __repr__ = __str__
