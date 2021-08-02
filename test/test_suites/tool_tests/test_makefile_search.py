from amirotest.model.aos_argument import AosArgument
from amirotest.model.search_results import GenericSearchResult
from amirotest.tools.config_path_finder import AosConfigFinder, ConfigFinder
from amirotest.tools.makefile_search import MakefileUserOptSearcher
from amirotest.tools.searcher import Searcher
from ..test_utils import AosModuleHelper
import unittest

from amirotest.tools import MakefileGlobalOptSearcher



class TestMakefileSearch(unittest.TestCase):

    def setUp(self):
        # self.helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()
        self.searcher = MakefileGlobalOptSearcher()

    def search_current_module(self, searcher: Searcher) -> GenericSearchResult:
        return searcher.search_options(
            AosConfigFinder(self.aos_module.path))

    def test_makefile_search_global_options(self):
        global_searcher = MakefileGlobalOptSearcher()
        res = self.search_current_module(global_searcher)
        self.assertGreater(len(res.get_options()), 0)

    def test_search_user_flags_in_nucleo(self):
        res = self.searcher.search_user_options(self.aos_module.get_makefile())
        user_searcher = MakefileUserOptSearcher()
        res = self.search_current_module(user_searcher)
        res = res.get_options()
        print(res)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, 'UDEFS')
        self.assertEqual(
            res[0].args[0],
            AosArgument('-DBOARD_MPU6050_CONNECTED=$(BOARD_MPU6050_CONNECTED)'))

    def test_search_user_flag_default_argument_non_existent(self):
        # Default module (NUCLEO-L476RG) has no default argument for its flag
        results = self.searcher.search_user_default_argument(self.aos_module.get_makefile(), 'BOARD_MPU6050_CONNECTED')
        self.assertEqual(results, None)

    def test_search_user_flag_multiple_default_flags(self):
        # Powermanagement hast a default value for its sensor ring
        pm_module = self.module_helper.get_aos_module(module_name="PowerManagement_1-2")
        results = self.searcher.search_user_default_argument(pm_module.get_makefile(), 'BOARD_SENSORRING')
        self.assertEqual(results, 'BOARD_PROXIMITYSENSOR')
