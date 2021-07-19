from dataclasses import dataclass, field
import re
@dataclass
class Module:
    name: str
    flags: list['Flag'] = field(init=False)
    def __post_init__(self):
        # In case a flag depends on an other flag the regex is used to detect
        # such a pattern: -flag=$(OTHER_FLAG)
        self.inferece_regex = re.compile(r'.*\$\((?P<flag>.*)\).*')
        self.flags = []

    def create_flags(self, search_results: list[tuple[str, str]]):
        for flag_name, flag_args in search_results:
            self.flags.append(Flag(flag_name, flag_args))


@dataclass
class Flag:
    name: str
    argument_str: str
    def __post_init__(self):
        splitted_args = self.argument_str.split(" ")
        self.args = [Argument(arg) for arg in splitted_args]

    def __str__(self) -> str:
        return f'{self.name}: {self.args}'
    __repr__ = __str__          # Better visualization

@dataclass(frozen=True)
class Argument:
    name: str
    def __str__(self) -> str:
        return f'{self.name}'
    __repr__ = __str__ # Better visualization
