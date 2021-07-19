from pathlib import Path
import re

class MakefileSearch:
    def extract_build_options(self, makefile: Path):
        regex = re.compile(
            r"""
            ^ifeq\s*\(\$\((?P<flag>[A-Z\d_]*)\),\)\n # Get option name
            \s*(?P=flag)\s*=\s*(?P<options>.*)\n # get option flags
            endif # match end
            """, re.VERBOSE | re.MULTILINE)
        with makefile.open() as make:
            content = make.read()
            res =  regex.findall(content)
            print(res)
        return []
