from amirotest.model.option import GlobalOption
from amirotest.model.search_result import SearchResult
from ..test_utils import PathHelper, AosModuleHelper
import unittest

class TestSearchResult(unittest.TestCase):

    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()

    def test_options_with_default(self):
        pass
