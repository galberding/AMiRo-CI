from pathlib import Path
from typing import Type
from amirotest.model.aos_module import AosModule, AmbigousOptionError
import unittest

from amirotest.model.option.aos_opt import CfgOption

from ..test_utils import AosModuleHelper
from amirotest.tools.search.search_result.search_results import SearchResult
from amirotest.model.option import MakeOption, AosOption
from amirotest.model import OptionNotFoundException


class TestAosModel(unittest.TestCase):

    def setUp(self) -> None:
        self.module_helper = AosModuleHelper()
        self.module_name = "NUCLEO-L476RG"
        self.aos_module = AosModule(Path(self.module_name))
        self.search_results = self.module_helper.nucleo_search_results

    def test_create_module(self):
        self.assertEqual(self.aos_module.name, self.module_name)

    def test_ensure_different_id_at_creation(self):
        self.assertNotEqual(AosModule(Path("Hello")).uid,
                            AosModule(Path("Hello")).uid)

    def test_module_with_options_is_resolved(self):
        result = SearchResult([
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfpu=fpv4-sp-d16')
        ], MakeOption)
        self.aos_module.add_options(result.get_options())
        self.assertTrue(self.aos_module.is_resolved())

    def test_module_with_options_is_unresolved(self):
        result = SearchResult([
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        ], CfgOption)
        self.aos_module.add_options(result.get_options())
        self.assertFalse(self.aos_module.is_resolved())

    def test_module_with_no_options_is_resolved(self):
        self.assertTrue(self.aos_module.is_resolved())

    def test_get_substitution_option_name_from_argument(self):
        unresolved_option = AosOption(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        sub_option_names = unresolved_option.get_substitution_opt_names()
        self.assertEqual(len(sub_option_names), 1)
        self.assertEqual(sub_option_names[0], 'USE_FPU')

    def test_module_find_option_by_name_not_found_exception(self):
        self.assertRaises(
            OptionNotFoundException,
            self.aos_module.find_option_by_name,
            'USE_FPU')

    def test_module_resolve_module(self):
        self.build_options_and_resolve_module([], self.aos_module)
        self.assertTrue(self.aos_module.is_resolved())
        self.assertEqual(
            self.aos_module.find_option_by_name("USE_FPU_OPT").args[0].name,
            "-mfloat-abi=softfp"
        )

    def test_module_resolve_multiple_options(self):
        search_res = [
            (("USE_FANCY_EXCEPTIONS_STACK", "-stack-usage=$(USE_EXCEPTIONS_STACKSIZE)")),
            (("USE_RANDOM_VALUE", "-set-seed=$(RAND_SEED)")),
            (("RAND_SEED", "42"))
        ]
        self.build_options_and_resolve_module(search_res, self.aos_module)
        self.assertTrue(self.aos_module.is_resolved())
        exc_option = self.aos_module.find_option_by_name("USE_FANCY_EXCEPTIONS_STACK")
        rval_option = self.aos_module.find_option_by_name("USE_RANDOM_VALUE")
        self.assertEqual(exc_option.args[0].name, "-stack-usage=0x400")
        self.assertEqual(rval_option.args[0].name, "-set-seed=42")

    def test_module_cannot_resolve_all_options(self):
        # TODO: not sure yet what's the best approach
        # therefore raise exception if resolution fails
        self.search_results.append(("USE_RANDOM_VALUE", "-set-seed=$(USE_UNKNOWN_OPTION)"))
        self.aos_module.add_options(
            SearchResult(self.search_results, CfgOption).get_options())
        self.assertRaises(OptionNotFoundException, self.aos_module.resolve)

    def test_module_resolve_multiple_args_with_same_sub_option(self):
        search_res = [
            (("USE_THIS_SUB", "42")),
            (("USE_CASE1", "-case1=$(USE_THIS_SUB)")),
            (("USE_CASE2", "-case2=$(USE_THIS_SUB)")),
            (("USE_CASE3", "-case3=$(USE_THIS_SUB)"))
        ]
        self.build_options_and_resolve_module(search_res, self.aos_module, opt_type=CfgOption)
        self.assertTrue(self.aos_module.is_resolved())


    def test_several_options_for_substitution(self):
        search_res = [
            (("USE_THIS_SUB", "42")),
            (("USE_THIS_SUB", "41")),
            (("USE_THIS_SUB", "39")),
            (("USE_CASE1", "-case1=$(USE_THIS_SUB)")),
        ]
        # self.build_options_and_resolve_module(search_res, self.aos_module, opt_type=MakeGlobalOption)
        # self.assertTrue(self.aos_module.is_resolved())
        self.assertRaises(AmbigousOptionError, self.build_options_and_resolve_module, search_res, self.aos_module, opt_type=CfgOption)


    def build_options_and_resolve_module(self, search_res,
                                         module: AosModule,
                                         result_type=SearchResult,
                                         opt_type: Type[AosOption]=AosOption):
        self.search_results += search_res
        s_res = result_type(self.search_results, opt_type)
        module.add_options(s_res.get_options())
        module.resolve()
