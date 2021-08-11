from amirotest.tools.search.search_result.aosconf_result import AosconfResult
from ...test_utils import PathHelper
from amirotest.model.option import AosOption, MakeGlobalOption
from amirotest.tools.search.search_result import GenericSearchResult

import unittest
PathHelper
from amirotest.tools.search import AosConfSearcher
from amirotest.tools.config_path_finder import AosModuleConfigFinder


class TestAosSearcher(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.conf_finder = AosModuleConfigFinder(self.path_helper.get_aos_module_path())
        self.searcher = AosConfSearcher()


    def test_get_options_returns_aosconf_result(self):
        res = self.searcher.search_options(self.conf_finder)
        # print(res)
        self.assertEqual(AosconfResult, type(res))

    def test_search_aosconf(self):
        res = self.searcher.search_options(self.conf_finder)
        # Amount of possible options that can be found in NUCLEO-L476RG
        self.assertEqual(len(res.get_options()), 27)

    # def get_options(self) -> list[AosOption]:
    #     res = self.searcher.search_options(self.conf_finder)
    #     res = res.get_options()
    #     return res


    # Ensure default options are returned
    #
