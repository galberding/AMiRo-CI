from pathlib import Path
import re
from typing import Any, Optional
from amirotest.tools import Searcher
from amirotest.model import AosModule
from amirotest.tools.config_path_finder import ConfigFinder
class MultipelUserOptionsException(Exception):
    pass



class MakefileSearcher(Searcher):
    def __init__(self) -> None:
        super().__init__()
        self.global_option_regex = re.compile(
            r"""
            ^ifeq\s*\(\$\((?P<flag>[A-Z\d_]*)\),\)\n # ifeq (GLOBAL_FLAG,)
            \s*(?P=flag)\s*=\s*(?P<options>.*)\n     # GLOBAL__FLAG = ARGS
            endif                                    # endif
            """, self.regex_options)

        self.user_option_regex = re.compile(
            r"""
            ^ifneq.*\n          # ifneq ($(USER_FLAG),)
            \s*override\s*(?P<flag>[\dA-Z_]*)\s*\+=\s*(?P<user_arg>.*)\n  # override UDEFS += ARGS
            endif                                            # endif
            """, self.regex_options)

    def search_global_options(self, makefile: Path) -> list[tuple[str, str]]:
        return self._search_with_regex(makefile, self.global_option_regex)

    def search_user_options(self, makefile: Path) -> list[tuple[str, str]]:
        return self._search_with_regex(makefile, self.user_option_regex)

    def search_options(self, finder : ConfigFinder):
        return self._search_with_regex(finder.get_makefile(), self.global_option_regex)

    def search_user_default_argument(self, makefile: Path, argument_name: str)-> Optional[str]:
        """Return default for user argument if it is set."""
        regex = re.compile(
            fr"""
            ^{argument_name}\s*\?=\s*(?P<value>.*)\n # ARGUMENT ?= VALUE
            """, self.regex_options)

        res = self._search_with_regex(makefile, regex)
        if len(res) > 1:
            raise MultipelUserOptionsException("Multiple user default values are provided!")

        return res[0] if len(res) == 1 else None
