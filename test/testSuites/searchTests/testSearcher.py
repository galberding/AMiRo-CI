# from amirotest import FLAG_REGEX
# from ..testUtils.pathHelper import PathHelper
import unittest
from amirotest.model.aos_module import AOSModule

from amirotest.tools.searcher import Searcher, FLAG_REGEX

from ..testUtils.pathHelper import PathHelper

# @unittest.skip("")
class TestSearcher(unittest.TestCase):
    def setUp(self):
        self.helper = PathHelper()
        self.search = Searcher()
        self.modulePath = self.helper.selectAosModule()

    def test_search_for_basic_defines(self):
        # Search pattern:
        # #if define(FLAG)
        res = self.search.search_if_defined_flags(self.modulePath)
        # print(res)
        self.assertGreater(len(res), 0)

    def test_get_flags_from_results(self):
        results = self.search.search_if_defined_flags(self.modulePath)
        for res in results:
            # print("File:", res.filepath.name)
            for flag in res.flags:
                # print(flag)
                self.assertRegex(flag, FLAG_REGEX)
