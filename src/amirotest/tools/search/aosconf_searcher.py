from enum import Enum
import re

from amirotest.tools.search.search_result import GenericSearchResult
from amirotest.tools.config_path_finder import ConfigFinder
from amirotest.tools.search import Searcher

class SearchGroupIdx(Enum):
    OS_CFG = 0
    AMIROOS_CFG = 1
    DEFAULT_ARG = 2


class AosConfSearcher(Searcher):
    def __init__(self) -> None:
        super().__init__()
        self.regex = re.compile(fr"""
        \#if\s* !defined\((?P<{SearchGroupIdx.OS_CFG.name}>\w*)\)\n                  # Extract OS option
        \s*\#define\s*(?P<{SearchGroupIdx.AMIROOS_CFG.name}>\w*)\s*(?P<{SearchGroupIdx.DEFAULT_ARG.name}>\w*)\n # Extract aos opt and default value
        \s*\#else.*\n
        \s*\#define\s(?P={SearchGroupIdx.AMIROOS_CFG.name})\s*(?P={SearchGroupIdx.OS_CFG.name}) # Ensure config is valid
        """, self.regex_options)

    def search_options(self, finder: ConfigFinder) -> GenericSearchResult:
        # TODO:
        res = self._search_with_regex(finder.get_aosconf(), self.regex)

        # return AosconfResult(res)
