from pathlib import Path
import re
from typing import Any, Optional, Union

class MakefileSearch:
    def __init__(self) -> None:
        self.global_flag_regex = re.compile(
            r"""
            ^ifeq\s*\(\$\((?P<flag>[A-Z\d_]*)\),\)\n # Get option name
            \s*(?P=flag)\s*=\s*(?P<options>.*)\n # get option flags
            endif # match end
            """, re.VERBOSE | re.MULTILINE)
        self.user_flag_regex = re.compile(
            r"""
            ^ifneq\s*\(\$\((?P<user_flag>.*),\).*\n           # ifneq ($(FLAG),)
            \s*override\s*UDEFS\s*\+=\s*(?P<arguments>.*)\n  # override UDEFS += -DFLAGXXX
            endif                                            # endif
            """, re.VERBOSE | re.MULTILINE)

    def search_global_arguments(self, makefile: Path) -> list[tuple[str, str]]:
        return self._search_file_with_regex(makefile, self.global_flag_regex)

    def search_user_flags(self, makefile: Path) -> list[tuple[str, str]]:
        return self._search_file_with_regex(makefile, self.user_flag_regex)

    def search_user_default_argument(self, makefile: Path, argument_name: str)-> Optional[str]:
        regex = re.compile(
            fr"""
            ^{argument_name}\s*\?=\s*(?P<value>.*)\n # ARGUMENT ?= VALUE
            """, re.VERBOSE | re.MULTILINE)
        res = self._search_file_with_regex(makefile, regex)

        return res[0] if len(res) == 1 else None


    def _search_file_with_regex(self, file: Path, regex: re.Pattern) -> list[Any]:
        with file.open() as make:
            content = make.read()
            res =  regex.findall(content)
            return res