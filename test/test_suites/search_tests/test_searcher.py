# from amirotest import FLAG_REGEX
# from ..testUtils.pathHelper import PathHelper
import unittest
from amirotest.model.aos_module import AOSModule

from amirotest.tools.searcher import Searcher, FLAG_REGEX

from ..test_utils.path_helper import PathHelper

@unittest.SkipTest
class TestSearcher(unittest.TestCase):
    def setUp(self):
        # self.skipTest("Not used right now")
        self.helper = PathHelper()
        self.search = Searcher()
        self.modulePath = self.helper.select_aos_module()
    # @unittest.
    def test_search_for_basic_defines(self):
        # Search pattern:
        # #if define(FLAG)
        res = self.search.search_if_defined_flags(self.modulePath)
        # print(res)
        self.assertGreater(len(res), 0)
    # @unittest.skip("Not used right now")
    def test_get_flags_from_results(self):
        results = self.search.search_if_defined_flags(self.modulePath)
        for res in results:
            # print("File:", res.filepath.name)
            for flag in res.flags:
                # print(flag)
                self.assertRegex(flag, FLAG_REGEX)
