from pathlib import Path
import re
from typing import Any, Optional


class MultipelUserFlagsException(Exception):
    pass

class MakefileSearch:
    def __init__(self) -> None:
        self.regex_options = re.VERBOSE | re.MULTILINE
        self.global_flag_regex = re.compile(
            r"""
            ^ifeq\s*\(\$\((?P<flag>[A-Z\d_]*)\),\)\n # ifeq (GLOBAL_FLAG,)
            \s*(?P=flag)\s*=\s*(?P<options>.*)\n     # GLOBAL__FLAG = ARGS
            endif                                    # endif
            """, self.regex_options)

        self.user_flag_regex = re.compile(
            r"""
            ^ifneq\s*\(\$\((?P<user_flag>.*)\),\).*\n          # ifneq ($(USER_FLAG),)
            \s*override\s*UDEFS\s*\+=\s*(?P<arguments>.*)\n  # override UDEFS += ARGS
            endif                                            # endif
            """, self.regex_options)

    def search_global_options(self, makefile: Path) -> list[tuple[str, str]]:
        return self._search_file_with_regex(makefile, self.global_flag_regex)

    def search_user_options(self, makefile: Path) -> list[tuple[str, str]]:
        return self._search_file_with_regex(makefile, self.user_flag_regex)

    def search_user_default_argument(self, makefile: Path, argument_name: str)-> Optional[str]:
        """Return """
        regex = re.compile(
            fr"""
            ^{argument_name}\s*\?=\s*(?P<value>.*)\n # ARGUMENT ?= VALUE
            """, self.regex_options)

        res = self._search_file_with_regex(makefile, regex)
        if len(res) > 1:
            raise MultipelUserFlagsException("Multiple user default values are provided!")

        return res[0] if len(res) == 1 else None


    def _search_file_with_regex(self, file: Path, regex: re.Pattern) -> list[Any]:
        with file.open() as make:
            content = make.read()
            res =  regex.findall(content)
            return res
