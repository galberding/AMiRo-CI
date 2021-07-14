from pathlib import Path
from amirotest.tools.searcher import SearchResult, Searcher

class CompileFlag():
    def __init__(self, path: Path, name: str, value=None) -> None:
        self.path = path
        self.name = name
        self.value = value

    def __eq__(self, o) -> bool:
        return self.path == o.path and self.name == o.name and self.value == o.value

    def __ne__(self, o) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.path, self.name, self.value))


class AOSModule():
    def __init__(self, path: Path):
        self.path = path
        self.flags = set()

    def setFlags(self, flags: set[CompileFlag]):
        self.flags |= flags


class AOSModuleFactory():
    def __init__(self) -> None:
        self.searcher = Searcher()

    def buildModule(self, path: Path) -> AOSModule:
        module = AOSModule(path)
        self._add_module_flags(module)

        return module

    def _add_module_flags(self, module: AOSModule):
        results = self.searcher.search_if_defined_flags(module.path)
        flags = self._generate_compile_flags(results)
        module.setFlags(flags)

    def _generate_compile_flags(self, results: list[SearchResult]) -> set[CompileFlag]:
        flags = set()
        for result in results:
            for flag in result.flags:
                flags.add(CompileFlag(result.filepath, flag))
        return flags
