from pathlib import Path
import re

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

            """, re.VERBOSE | re.MULTILINE)

    def search_global_arguments(self, makefile: Path):


        with makefile.open() as make:
            content = make.read()
            res =  self.global_flag_regex.findall(content)
            return res
