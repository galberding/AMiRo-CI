from pathlib import Path
import unittest

from amirotest.tools.makefile_search import MakefileSearch



class TestMakefileSearch(unittest.TestCase):

    def setUp(self):
        self.makefile_path = Path("/home/schorschi/hiwi/AMiRo-OS/modules/NUCLEO-L476RG/Makefile")

    def test_makefile_extract_raw_options(self):
        self.searcher = MakefileSearch()
        options = self.searcher.extract_build_options(self.makefile_path)
        self.assertGreater(len(options), 0)
