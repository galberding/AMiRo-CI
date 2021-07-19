from typing import Callable, Optional
import unittest
from pathlib import Path
import re
from ..test_utils.path_helper import PathHelper

@unittest.SkipTest
class TestExploreRegexes(unittest.TestCase):

    def setUp(self):
        self.helper = PathHelper()
        self.module_path = self.helper.getPathToAosModules()
        self.aos_module = self.helper.select_aos_module()

    def get_content(self, path: Path) -> tuple[bool, str]:
        if path.is_file():
            with path.open() as f:
                try:
                    content = f.read()
                    return (True, content)
                except:
                    pass
        return (False, '')

    def get_module(self, module="NUCLEO-L476RG") -> Optional[Path]:
        for path_obj in self.module_path.glob("**/*"):
            if path_obj.is_dir() and path_obj.name == module:
                return path_obj
        raise FileNotFoundError()

    def search_module(self, regex: re.Pattern, fun: Callable):
        print(f"Search in module: {self.aos_module.name}")
        for f in self.aos_module.glob("**/*"):
            has_content, content = self.get_content(f)
            if has_content:
                res = regex.findall(content)
                if res:
                    print(f"=> {f.name}")
                    fun(res)

    def print_basic_defines(self, res):
        print(type(res))
        for r in res:
            print(type(r))
            if r[1]:
                print(f"---> {r[1]}")
            else:
                print(f"---> {r[2]}")

    # @unittest.SkipTest("")
    def test_search_for_basic_defines(self):
        regex: re.Pattern = re.compile(
            r'''^\#if\s                                # Match beginning #if
            (defined\((?P<flag>[A-Z,\d,_]+)\)                    # Match defined((FLAG))
            |\(([A-Z,0-9,_]+)\s==\s(TRUE|True|true)\) # Match ((FLAG) == true)
            )
            .*$
            ''',
            re.VERBOSE | re.MULTILINE)
        self.search_module(regex, self.print_basic_defines)


    def print_named_group_regex(self, res):
        # print(res)
        for r in res:
            print(f"--> {r}")

    # @unittest.SkipTest
    def test_search_module_named_group_regex(self):
        """ Search for #if defined(FLAG)|(FLAG==true) with named groups
        """
        regex = re.compile(
            r'''^\#if(.*)\n #Match start directive
            (.*)\n
            \#endif
            ''',  re.VERBOSE | re.MULTILINE)
        self.search_module(regex, self.print_named_group_regex)


if __name__ == '__main__':
    unittest.main()
