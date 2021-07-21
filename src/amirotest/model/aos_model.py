from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Optional

class FlagNotFoundException(Exception):
    pass



@dataclass
class Module:
    # name: str
    path: Path
    name: str = field(init=False)
    flags: list['Flag'] = field(init=False)

    def __post_init__(self):
        self.name = self.path.name
        self.flags = []

    def create_flags(self, search_results: list[tuple[str, str]]):
        for flag_name, flag_args in search_results:
            self.flags.append(Flag(flag_name, flag_args))

    def get_makefile(self) -> Path:
        return self.path.joinpath("Makefile")

    def is_resolved(self) -> bool:
        """Check if all flags are resolved."""
        if not self.flags:
            return True

        for flag in self.flags:
            if not flag.is_resolved():
                return False
        return True

    def resolve(self):
        u_flags = self.get_unresolved_flags()
        sub_flag_names = []
        # get substitution flags
        for u_flag in u_flags:
            sub_flag_names += u_flag.get_substitution_flags()
        sub_flags = self.find_flags_by_names(sub_flag_names)
        for u_flag in u_flags:
            for s_flag in sub_flags:
                u_flag.resolve(s_flag)

    def get_unresolved_flags(self) -> list['Flag']:
        u_flags = []
        for flag in self.flags:
            if not flag.is_resolved():
                u_flags.append(flag)
                # pass
        return u_flags

    def find_flags_by_names(self, flag_names: list[str]) -> list['Flag']:
        flags = []
        for flag_name in flag_names:
            flags.append(self.find_flag_by_name(flag_name))
        return flags

    def find_flag_by_name(self, flag_name: str) -> 'Flag':
        for flag in self.flags:
            if flag.name == flag_name:
                return flag
        raise FlagNotFoundException(f"Cannot find {flag_name}!")

    def __str__(self) -> str:
        return f'{self.name}: {self.flags}'
    __repr__ = __str__


@dataclass
class Flag:
    name: str
    argument_str: str

    def __post_init__(self):
        splitted_args = self.argument_str.split(" ")
        self.args = [Argument(arg) for arg in splitted_args]

    def is_resolved(self) -> bool:
        return len(self.get_substitution_flags()) == 0

    def get_substitution_flags(self) -> list[str]:
        """Returns all substitution flags that are found in the arguments."""
        flags = []
        for arg in self.args:
            if not arg.is_resolved():
                flags.append(arg.get_substitution_flag())
        return flags

    def resolve(self, flag: 'Flag') -> bool:
        for arg in self.args:
            arg.resolve(flag.name, flag.argument_str)
        return self.is_resolved()

    def __str__(self) -> str:
        return f'{self.name}: {self.args}'
    __repr__ = __str__


@dataclass(unsafe_hash=True)
class Argument:
    name: str
    def __post_init__(self):
        self.substitution_flag_regex: re.Pattern = re.compile(r'\$\((?P<flag>.*)\)')
        self.resolved = False

    def is_resolved(self) -> bool:
        if self.resolved:
            return True
        # If no substitution flag is returned
        # the Argument is considered resolved
        if not self.get_substitution_flag():
            self.resolved = True
        return self.resolved

    def resolve(self, sub_flag_name: str, flag_value: str):
        """Replace name attribute with substituted flag_value."""
        if sub_flag_name != self.get_substitution_flag():
            # Not the matching sub_flag
            return
        arg_name = re.sub(self.substitution_flag_regex,
               flag_value,
               self.name)
        self.name = arg_name

    def get_substitution_flag(self) -> Optional[re.Match]:
        res = self.substitution_flag_regex.search(self.name)
        return res.group('flag') if res else None


    def __str__(self) -> str:
        return f'{self.name}'
    __repr__ = __str__
