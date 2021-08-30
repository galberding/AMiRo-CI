from ..test_utils.test_helper import PathHelper
import unittest

from amirotest.tools.config_path_finder import AosModuleConfigFinder


class TestReporter(unittest.TestCase):
    def setUp(self):
        self.path_helper = PathHelper()
        self.finder = AosModuleConfigFinder(self.path_helper.aos_path)
        # self.rep = Reporter(self.finder)

    def test_compile_pipeline(self):
        pass
