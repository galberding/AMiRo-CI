from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import uuid

from amirotest.model.option import AosOption
from amirotest.model.option.aos_opt import DefaultOpiton

class OptionNotFoundException(Exception):
    pass

class AmbigousOptionError(Exception):
    pass

@dataclass
class BuildInfo:
    comp_proc: subprocess.CompletedProcess
    duration: float
    cpu_time: float
    def dump(self, builddir: Path):
        """!Dump content to csv in build dir.
        """
        file = builddir.joinpath()
        with file.open('w') as f:

            f.write(f'Duration: {self.duration}\n')
            # f.writelines(self.comp_proc.args)
            # f.write(self.comp_proc.stdout.decode('utf-8'))
            f.write(self.comp_proc.stderr.decode('utf-8'))

@dataclass(unsafe_hash=True)
class AosModule:
    name: str = field(init=False)
    _build_info: BuildInfo = field(init=False)
    uid: str = field(init=False, default="")
    path: Path
    options: list[AosOption] = field(init=False)

    def __post_init__(self):
        self.name = self.path.name
        self.options = []
        self.uid = str(uuid.uuid1())

    def copy(self):
        """!Create copy.
        """
        module = AosModule(self.path)
        module.add_options(self.get_option_copy())
        return module

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

    @property
    def build_info(self) -> BuildInfo:
        return self._build_info

    @build_info.setter
    def build_info(self, build_info: BuildInfo):
        self._build_info = build_info

    def resolve(self):
        """!Check if there are unresolved options and resolve it.

        Try to resolve all containing options.
        All substitution options needs to be provided
        in order to fully resolve all options.
        """
        if self.is_resolved():
            return

        u_opts = self.get_unresolved_options()
        sub_opts = self.get_substitution_options()
        for u_opt in u_opts:
            for s_opt in sub_opts:
                u_opt.resolve(s_opt)

    def is_resolved(self) -> bool:
        """!Check whether all options in the module are resolved.
        An option is unresolved if at least one of its arguments
        contains a `$(OPTION_NAME)` pattern.
        With resolve() the module searches in its options
        for `OPTION_NAME` and places its content in the unresolved option argument.
        """
        if not self.options:
            return True

        for option in self.options:
            if not option.is_resolved():
                return False
        return True

    def get_substitution_options(self) -> list[AosOption]:
        """!Get Option contained in unresolved arguments.
        Also referred to as substitution option because their
        content is substituted into the argument"""
        sub_option_names = []
        u_options = self.get_unresolved_options()
        for u_option in u_options:
            sub_option_names += u_option.get_substitution_opt_names()
        sub_options = self.find_options_by_names(sub_option_names)
        return sub_options

    def get_unresolved_options(self) -> list[AosOption]:
        """Get all options with unresolved arguments"""
        u_options = []
        for option in self.options:
            if not option.is_resolved():
                u_options.append(option)
        return u_options

    def find_options_by_names(self, option_names: list[str]) -> list[AosOption]:
        """!Find all options to the given option names.
        """
        options = []
        for option_name in option_names:
            options.append(self.find_option_by_name(option_name))
        return options

    def find_option_by_name(self, option_name: str) -> AosOption:
        """!Find option that matches the option_name.
        The first match is returned.
        @note it is save to return the first option because
        no duplicate options are allowed.
        @param option_name
        """
        for option in self.options:
            if option.name == option_name:
                return option
        raise OptionNotFoundException(f"Cannot find {option_name}!")

    def __str__(self) -> str:
        return f'{self.name}: {self.options}'
    __repr__ = __str__
