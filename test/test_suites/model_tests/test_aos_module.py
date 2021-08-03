from amirotest.model.option.aos_opt import GlobalOption, AosOption
from amirotest.model.search_result.search_results import SearchResult
from amirotest.tools import MakefileGlobalOptSearcher
from amirotest.model import OptionNotFoundException

from ..test_utils import AosModuleHelper, PathHelper
import unittest


class TestAosModel(unittest.TestCase):

    def setUp(self) -> None:
        self.searcher = MakefileGlobalOptSearcher()
        self.helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()
        self.module_name = "NUCLEO-L476RG"
        self.search_results = self.module_helper.nucleo_search_results

    def test_create_module(self):
        self.assertEqual(self.aos_module.name, self.module_name)

    def test_module_get_makefile(self):
        makefile = self.aos_module.get_makefile()
        self.assertTrue(makefile.exists())

    def test_module_with_flags_is_resolved(self):
        result = SearchResult([
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfpu=fpv4-sp-d16')
        ], GlobalOption)
        self.aos_module.add_options(result)
        self.assertTrue(self.aos_module.is_resolved())

    def test_module_with_flags_is_unresolved(self):
        result = SearchResult([
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        ], GlobalOption)
        self.aos_module.add_options(result)
        self.assertFalse(self.aos_module.is_resolved())

    def test_module_with_no_flags_is_resolved(self):
        self.assertTrue(self.aos_module.is_resolved())

    def test_get_substitution_flag_name_from_argument(self):
        unresolved_flag = AosOption(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        sub_flag_names = unresolved_flag.get_substitution_opt_names()
        self.assertEqual(len(sub_flag_names), 1)
        self.assertEqual(sub_flag_names[0], 'USE_FPU')

    def test_module_find_flag_by_name_not_found_exception(self):
        self.assertRaises(
            OptionNotFoundException,
            self.aos_module.find_option_by_name,
            'USE_FPU')

    def test_module_resolve_module(self):
        self.aos_module.add_options(SearchResult(self.search_results, GlobalOption))
        self.assertFalse(self.aos_module.is_resolved())
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
        self.assertEqual(
            self.aos_module.find_option_by_name("USE_FPU_OPT").args[0].name,
            "-mfloat-abi=softfp"
        )

    def test_module_resolve_multiple_flags(self):
        self.search_results.append(("USE_FANCY_EXCEPTIONS_STACK", "-stack-usage=$(USE_EXCEPTIONS_STACKSIZE)"))
        self.search_results.append(("USE_RANDOM_VALUE", "-set-seed=$(RAND_SEED)"))
        self.search_results.append(("RAND_SEED", "42"))
        self.aos_module.add_options(SearchResult(self.search_results, GlobalOption))
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
        exc_flag = self.aos_module.find_option_by_name("USE_FANCY_EXCEPTIONS_STACK")
        rval_flag = self.aos_module.find_option_by_name("USE_RANDOM_VALUE")
        self.assertEqual(exc_flag.args[0].name, "-stack-usage=0x400")
        self.assertEqual(rval_flag.args[0].name, "-set-seed=42")

    def test_module_cannot_resolve_all_flags(self):
        # TODO: not sure yet what's the best approach
        # therefore raise exception if resolution fails
        self.search_results.append(("USE_RANDOM_VALUE", "-set-seed=$(USE_UNKNOWN_FLAG)"))
        self.aos_module.add_options(SearchResult(self.search_results, GlobalOption))
        self.assertRaises(OptionNotFoundException, self.aos_module.resolve)

    def test_module_resolve_multiple_args_with_same_sub_flag(self):
        self.search_results.append(("USE_THIS_SUB", "42"))
        self.search_results.append(("USE_CASE1", "-case1=$(USE_THIS_SUB)"))
        self.search_results.append(("USE_CASE2", "-case2=$(USE_THIS_SUB)"))
        self.search_results.append(("USE_CASE3", "-case3=$(USE_THIS_SUB)"))
        self.aos_module.add_options(SearchResult(self.search_results, GlobalOption))
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
