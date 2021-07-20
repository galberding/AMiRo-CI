from pathlib import Path
from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.tools.makefile_search import MakefileSearch



class TestMakefileSearch(unittest.TestCase):

    def setUp(self):
        self.makefile_path = Path("/home/schorschi/hiwi/AMiRo-OS/modules/NUCLEO-L476RG/Makefile")
        self.helper = PathHelper()
        self.aos_module = self.helper.get_nucleo_module()

    def test_makefile_search_global_arguments(self):
        self.searcher = MakefileSearch()
        options = self.searcher.search_global_arguments(
            self.aos_module.get_makefile())
        self.assertGreater(len(options), 0)
