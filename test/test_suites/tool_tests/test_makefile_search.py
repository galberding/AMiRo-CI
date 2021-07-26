from pathlib import Path
from ..test_utils.module_creation_helper import AosModuleHelper
from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.tools.makefile_search import MakefileSearch



class TestMakefileSearch(unittest.TestCase):

    def setUp(self):
        # self.helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()
        self.searcher = MakefileSearch()

    def test_makefile_search_global_options(self):
        flags = self.searcher.search_global_options(
            self.aos_module.get_makefile())
        self.assertGreater(len(flags), 0)

    def test_search_user_flags_in_nucleo(self):
        results = self.searcher.search_user_options(self.aos_module.get_makefile())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 'BOARD_MPU6050_CONNECTED')
        self.assertEqual(results[0][1], '-DBOARD_MPU6050_CONNECTED')

    def test_search_user_flag_default_argument_non_existent(self):
        # Default module (NUCLEO-L476RG) has no default argument for its flag
        results = self.searcher.search_user_default_argument(self.aos_module.get_makefile(), 'BOARD_MPU6050_CONNECTED')
        self.assertEqual(results, None)

    def test_search_user_flag_multiple_default_flags(self):
        # Powermanagement hast a default value for its sensor ring
        pm_module = self.module_helper.get_aos_module(module_name="PowerManagement_1-2")
        results = self.searcher.search_user_default_argument(pm_module.get_makefile(), 'BOARD_SENSORRING')
        self.assertEqual(results, 'BOARD_PROXIMITYSENSOR')
