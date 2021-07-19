from dataclasses import dataclass, field

@dataclass
class Module:
    name: str
    def __post_init__(self):
        # In case a flag depends on an other flag the regex is used to detect
        # such a pattern: -flag=$(OTHER_FLAG)
        self.inferece_regex = re.compile(r'.*\$\((?P<flag>.*)\).*')
        self.flags: list['Flag'] = []

    def create_flags(self, search_results: dict[str, str]):
        for flag_name, flag_args in search_results:
            self.flags.append(Flag(flag_name, flag_args))


@dataclass
class Flag:
    name: str
    argument_str: str
    def __post_init__(self):
        splitted_args = self.argument_str.split(" ")
        self.args = [Argument(arg) for arg in splitted_args]

@dataclass(frozen=True)
class Argument:
    name: str
