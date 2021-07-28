from dataclasses import dataclass
import re
from typing import Optional, Union
from enum import Enum, auto

class MalformatedUserArgument(Exception):
    pass


class RegexGroupID(Enum):
    STANDARD_OPTION = auto()
    ASSIGNMENT_LEFT = auto()
    ASSIGNMENT_VALUE = auto()
    STANDARD_ARG = auto()


@dataclass(unsafe_hash=True)
class AosArgument:
    name: str
    def __post_init__(self):
        self.option_substitution_regex: re.Pattern = re.compile(
            fr'\$\((?P<{RegexGroupID.STANDARD_OPTION.name}>.*)\)')
        self.variable_extraction_regex = re.compile(
            fr"""
            -((?P<{RegexGroupID.ASSIGNMENT_LEFT.name}>.*)        # -std
            =(?P<{RegexGroupID.ASSIGNMENT_VALUE.name}>.*)        # =c99 --> -std=c99
            |(?P<{RegexGroupID.STANDARD_ARG.name}>[\dA-Za-z-,]*)) # -fsth-else
            """, re.VERBOSE)
        self.resolved = False

    def extract_variable(self, prefix) -> Optional[tuple[str, str]]:
        if not self.is_resolved():
            return
        arg, a_left, a_value = self._search_variable_pattern()
        print(arg)
        if arg:
            var_name = self._append_allcaps_to_prefix(prefix, arg)
            self.name = f"-$({var_name})"
            return var_name, arg
        elif a_left and a_value:
            var_name = self._append_allcaps_to_prefix(prefix, a_left)
            self.name = f"-{a_left}=$({var_name})"
            return var_name, a_value

    def _search_variable_pattern(self) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Search for different argument patterns:
        1. Assignment pattern: -std=c99, -mfpu=fpv4-sp-d16
        2. Standard argument: -fshort-enums, -O2, -Wl,--print-memory-usage ..."""
        res = self.variable_extraction_regex.search(self.name)
        arg = res.group(RegexGroupID.STANDARD_ARG.name)
        a_left = res.group(RegexGroupID.ASSIGNMENT_LEFT.name)
        a_value = res.group(RegexGroupID.ASSIGNMENT_VALUE.name)
        return arg, a_left, a_value

    def _append_allcaps_to_prefix(self, prefix: str, raw_suffix: str) -> str:
        """Convert raw_suffix to allcaps, remove other special characters and append to prefix."""
        suffix = raw_suffix.replace(",", "")
        # Collapse multiple occurances of '--' e.g. -Wl,--print-memory-usage
        suffix = suffix.replace("--", "_")
        suffix = suffix.replace("-", "_")
        suffix = suffix.upper()
        return f"{prefix}_{suffix}"


    def is_resolved(self) -> bool:
        """If no substitution option is found the arg is considered resolved."""
        return not self.search_substitution_option()

    def resolve(self, option_name: str, option_value: str):
        """Resolve option name, ensure that the provided option is suited for substitution."""
        if option_name != self.search_substitution_option():
            # Not the matching sub_flag
            return
        self._substitute_option_value_in_name(option_value)
        # arg_name = re.sub(self.option_substitution_regex,
        #        flag_value,
        #        self.name)
        # self.name = arg_name

    def _substitute_option_value_in_name(self, option_value):
        """Replace name attribute with substituted option_value."""
        arg_name = re.sub(self.option_substitution_regex,
               option_value,
               self.name)
        self.name = arg_name

    def search_substitution_option(self) -> Optional[re.Match]:
        res = self.option_substitution_regex.search(self.name)
        return res.group(RegexGroupID.STANDARD_OPTION.name) if res else None


    def __str__(self) -> str:
        return f'{self.name}'
    __repr__ = __str__


class UserArgument(AosArgument):
    def __init__(self, user_arg_name):
        self.user_flag_substitution_regex = re.compile(
            fr"""
            -D(?P<{RegexGroupID.STANDARD_ARG.name}>[\dA-Z_]*)      # -D<ARG_NAME>
            (=\$\((?P<{RegexGroupID.STANDARD_OPTION.name}>.*)\)|$) # =$(<OPTION_NAME>) or None
            """, re.VERBOSE)
        res = self.user_flag_substitution_regex.search(user_arg_name)
        extracted_arg_name = res.group(RegexGroupID.STANDARD_ARG.name)
        option = res.group(RegexGroupID.STANDARD_OPTION.name)
        if not extracted_arg_name:
            raise MalformatedUserArgument(f"Cannot process user argument: {user_arg_name}")
        if not option:
            user_arg_name = self.append_substitution_to_arg(user_arg_name, extracted_arg_name)
        super().__init__(user_arg_name)

    def append_substitution_to_arg(self, arg, sub_flag) -> str:
        return f"{arg}=$({sub_flag})"
