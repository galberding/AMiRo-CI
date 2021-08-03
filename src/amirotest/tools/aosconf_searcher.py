from enum import Enum
# from amirotest.model.aos_opt import DefaultOpiton
# from amirotest.model.search_results import GenericSearchResult
import amirotest.model.aos_module as aos_module
# from amirotest.model.aos_opt import DefaultOpiton
import amirotest.model.option as aos_opt
import amirotest.model.search_result as aos_search_res
import amirotest.tools as aos_tools
# from amirotest.tools import ConfigFinder
# from . import Searcher
import re

Searcher = aos_tools.Searcher
GenericSearchResult = aos_search_res.GenericSearchResult
ConfigFinder = aos_tools.ConfigFinder

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
        res = self._search_with_regex(finder.get_aosconf(), self.regex)
        return
