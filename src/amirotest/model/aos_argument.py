from dataclasses import dataclass
import re
from typing import Optional

class MalformatedUserArgument(Exception):
    pass

@dataclass(unsafe_hash=True)
class AosArgument:
    name: str
    def __post_init__(self):
        self.substitution_flag_regex: re.Pattern = re.compile(r'\$\((?P<flag>.*)\)')
        self.variable_extraction_regex = re.compile(
            r"-((?P<assign_left>.*)=(?P<assign_value>.*)|(?P<normal_arg>[\dA-Za-z-]*))")
        self.resolved = False

    def extract_variable(self, prefix) -> Optional[tuple[str, str]]:
        if not self.is_resolved():
            return
        res = self.variable_extraction_regex.search(self.name)
        normal_arg = res.group("normal_arg")
        assign_left = res.group("assign_left")
        assign_value = res.group("assign_value")

        if normal_arg:
            suffix = normal_arg.replace("-", "_").upper()
            var_name = f"{prefix}_{suffix}"
            self.name = f"-$({var_name})"
            return var_name, normal_arg
        elif assign_left and assign_value:
            suffix = assign_left.replace("-", "_").upper()
            var_name = f"{prefix}_{suffix}"
            self.name = f"-{assign_left}=$({var_name})"
            return var_name, assign_value

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


class UserArgument(AosArgument):
    def __init__(self, name):
        self.user_flag_substitution_regex = re.compile(r"-D(?P<flag1>[\dA-Z_]*)(=\$\((?P<flag2>.*)\)|$)")
        res = self.user_flag_substitution_regex.search(name)
        if not res.group("flag1"):
            raise MalformatedUserArgument(f"Cannot process user argument: {name}")
        if not res.group("flag2"):
            name = self.append_substitution_to_arg(name, res.group("flag1"))
        super().__init__(name)

    def append_substitution_to_arg(self, arg, sub_flag) -> str:
        return f"{arg}=$({sub_flag})"
