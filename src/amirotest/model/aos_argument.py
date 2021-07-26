from dataclasses import dataclass
import re
from typing import Optional

@dataclass(unsafe_hash=True)
class AosArgument:
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
