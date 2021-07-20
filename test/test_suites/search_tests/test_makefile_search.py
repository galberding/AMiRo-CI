from pathlib import Path
from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.tools.makefile_search import MakefileSearch



class TestMakefileSearch(unittest.TestCase):

    def setUp(self):
        self.helper = PathHelper()
        self.aos_module = self.helper.get_aos_module()
        self.searcher = MakefileSearch()

    def test_makefile_search_global_flags(self):
        flags = self.searcher.search_global_arguments(
            self.aos_module.get_makefile())
        self.assertGreater(len(flags), 0)

    def test_search_user_flags_in_nucleo(self):
        results = self.searcher.search_user_flags(self.aos_module.get_makefile())
        print(results)
        self.assertEqual(len(results), 1)

    def test_search_user_flag_default_argument_non_existent(self):
        # Default module (NUCLEO-L476RG) has no default argument for its flag
        results = self.searcher.search_user_default_argument(self.aos_module.get_makefile(), 'BOARD_MPU6050_CONNECTED')
        # print(results)
        self.assertEqual(results, list())

    def test_search_user_flag_multiple_default_flags(self):
        # Powermanagement hast a default value for its sensor ring
        pm_module = self.helper.get_aos_module(module_name="PowerManagement_1-2")
        results = self.searcher.search_user_default_argument(pm_module.get_makefile(), 'BOARD_SENSORRING')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 'BOARD_PROXIMITYSENSOR')
