from dataclasses import dataclass, field
from pathlib import Path
from typing import Type

from amirotest.model import GlobalOption, UserOption, AosOption


class OptionNotFoundException(Exception):
    pass


@dataclass
class AOSModule:
    name: str = field(init=False)
    path: Path
    flags: list[AosOption] = field(init=False)

    def __post_init__(self):
        self.name = self.path.name
        self.flags = []

    def get_makefile(self) -> Path:
        return self.path.joinpath("Makefile")

    def create_global_flags(self, search_results: list[tuple[str, str]]):
        self.create_flags(search_results, GlobalOption)

    def create_user_flags(self, search_results: list[tuple[str, str]]):
        self.create_flags(search_results, UserOption)

    def create_flags(self, search_results: list[tuple[str, str]],
                     flag_type: Type[AosOption]=AosOption):
        """Create flags from given search results.
        Example:
        > create_flags([('USE_COPT', '-std=c99 -fshort-enums')])
        Refer to the tests to get a deeper understanding.
        """
        for flag_name, flag_args in search_results:
            self.flags.append(flag_type(flag_name, flag_args))


    def is_resolved(self) -> bool:
        """Check if all flags are resolved."""
        if not self.flags:
            return True

        for flag in self.flags:
            if not flag.is_resolved():
                return False
        return True

    def resolve(self):
        """Try to resolve all containing flags.
        All substitution flags needs to be provided
        in order to fully resolve all flags.
        """
        if self.is_resolved():
            return

        u_flags = self.get_unresolved_flags()
        sub_flags = self.get_substitution_flags()
        # get substitution flags

        for u_flag in u_flags:
            for s_flag in sub_flags:
                u_flag.resolve(s_flag)

    def get_unresolved_flags(self) -> list[AosOption]:
        """Get all flags with unresolved arguments"""
        u_flags = []
        for flag in self.flags:
            if not flag.is_resolved():
                u_flags.append(flag)
        return u_flags

    def get_substitution_flags(self) -> list[AosOption]:
        """Get Flag contained in unresolved arguments.
        Also referred to as substitution flag because their
        content is substituted into the argument"""
        sub_flag_names = []
        u_flags = self.get_unresolved_flags()
        for u_flag in u_flags:
            sub_flag_names += u_flag.get_substitution_opt_names()
        sub_flags = self.find_flags_by_names(sub_flag_names)
        return sub_flags

    def find_flags_by_names(self, flag_names: list[str]) -> list[AosOption]:
        flags = []
        for flag_name in flag_names:
            flags.append(self.find_flag_by_name(flag_name))
        return flags

    def find_flag_by_name(self, flag_name: str) -> AosOption:
        for flag in self.flags:
            if flag.name == flag_name:
                return flag
        raise OptionNotFoundException(f"Cannot find {flag_name}!")

    def dict_factory(self):
        return {self.name: 42}

    def to_dict(self) -> dict:
        conf = {}
        conf[self.name] = {}
        # conf[self.name]["path"] = self.path

        conf[self.name] = {}
        conf[self.name][GlobalOption.__name__] = {}
        conf[self.name][UserOption.__name__] = {}

        for flag in self.flags:
            conf[self.name][flag.get_type()][flag.name] = [arg.name for arg in flag.args]
        return conf


    def __str__(self) -> str:
        return f'{self.name}: {self.flags}'
    __repr__ = __str__
