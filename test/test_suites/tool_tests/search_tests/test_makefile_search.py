from amirotest.model.argument import AosArgument
from amirotest.tools.search.search_result import GenericSearchResult
from amirotest.tools.config_path_finder import AosConfigFinder, ConfigFinder
from amirotest.tools.search import MakefileUserOptSearcher, MakefileGlobalOptSearcher
from amirotest.tools.search import Searcher
from ...test_utils import AosModuleHelper
import unittest





class TestMakefileSearch(unittest.TestCase):

    def setUp(self):
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()
        self.searcher = MakefileGlobalOptSearcher()

    def test_makefile_search_global_options_in_module(self):
        res = self.search_current_module(
            MakefileGlobalOptSearcher())
        res = res.get_options()
        # 12 Global options are used in NUCLEO-L476RG (and usually in the other modules)
        self.assertEqual(len(res), 12)

    def test_search_user_options_in_module(self):
        res = self.search_current_module(
            MakefileUserOptSearcher())
        res = res.get_options()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, 'UDEFS')
        self.assertEqual(
            res[0].args[0],
            AosArgument('-DBOARD_MPU6050_CONNECTED=$(BOARD_MPU6050_CONNECTED)'))

    def search_current_module(self, searcher: Searcher) -> GenericSearchResult:
        return searcher.search_options(
            AosConfigFinder(self.aos_module.path))

    def test_search_user_flag_default_argument_non_existent(self):
        # Default module (NUCLEO-L476RG) has no default argument for its flag
        results = self.searcher.search_user_default_argument(self.aos_module.get_makefile(), 'BOARD_MPU6050_CONNECTED')
        self.assertEqual(results, None)

    def test_search_user_flag_multiple_default_flags(self):
        # Powermanagement hast a default value for its sensor ring
        pm_module = self.module_helper.get_aos_module(module_name="PowerManagement_1-2")
        results = self.searcher.search_user_default_argument(pm_module.get_makefile(), 'BOARD_SENSORRING')
        self.assertEqual(results, 'BOARD_PROXIMITYSENSOR')
