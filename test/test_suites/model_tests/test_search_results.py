from amirotest.model.aos_opt import GlobalOption
from amirotest.model.search_results import SearchResult
from ..test_utils import PathHelper, AosModuleHelper
import unittest

class TestSearchResult(unittest.TestCase):

    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()

    def test_module_create_flags(self):
        pass
