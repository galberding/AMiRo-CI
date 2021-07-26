from ..test_utils.module_creation_helper import AosModuleHelper
from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.model import AosFlag, FlagNotFoundException
from amirotest.tools.makefile_search import MakefileSearch

class TestAosModel(unittest.TestCase):

    def setUp(self) -> None:
        self.searcher = MakefileSearch()
        self.helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.aos_module = self.module_helper.get_aos_module()
        self.module_name = "NUCLEO-L476RG"
        self.search_results = [
            ('USE_OPT', '-O2 -fstack-usage -Wl,--print-memory-usage'), # Has option for preprocessor (-Wl,)
            ('USE_COPT', '-std=c99 -fshort-enums'),
            ('USE_CPPOPT', '-fno-rtti -std=c++17'),
            ('USE_LINK_GC', 'yes'),
            ('USE_LDOPT', '-lm'),
            ('USE_LTO', 'yes'),
            ('USE_VERBOSE_COMPILE', 'no'),
            ('USE_SMART_BUILD', 'no'),
            ('USE_PROCESS_STACKSIZE', '0x400'),
            ('USE_EXCEPTIONS_STACKSIZE', '0x400'),
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16') # Needs to be substituted
        ]

    def test_create_module(self):
        self.assertEqual(self.aos_module.name, self.module_name)

    def test_module_get_makefile(self):
        makefile = self.aos_module.get_makefile()
        self.assertTrue(makefile.exists())

    def test_module_create_flags(self):
        self.aos_module.create_flags(self.search_results)
        self.assertEqual(len(self.aos_module.flags), len(self.search_results))

    def test_module_with_no_flags_is_resolved(self):
        self.assertTrue(self.aos_module.is_resolved())

    def test_module_with_flags_is_resolved(self):
        search_results = [
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfpu=fpv4-sp-d16')
        ]
        self.aos_module.create_flags(search_results)
        self.assertTrue(self.aos_module.is_resolved())

    def test_module_with_flags_is_unresolved(self):
        search_results = [
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        ]
        self.aos_module.create_flags(search_results)
        self.assertFalse(self.aos_module.is_resolved())

    def test_get_substitution_flag_name_from_argument(self):
        unresolved_flag = AosFlag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        sub_flag_names = unresolved_flag.get_substitution_flag_names()
        self.assertEqual(len(sub_flag_names), 1)
        self.assertEqual(sub_flag_names[0], 'USE_FPU')

    def test_module_substitute_unresolved_flag(self):
        self.aos_module.create_flags(self.search_results)
        u_flags = self.aos_module.get_unresolved_flags()
        self.assertEqual(len(u_flags), 1)
        # get only flag that needs to be substituted
        self.assertEqual(u_flags[0].name, "USE_FPU_OPT")


    def test_module_find_flag_by_name(self):
        self.aos_module.create_flags(self.search_results)
        flag = self.aos_module.find_flag_by_name('USE_FPU')
        self.assertEqual(flag.name, "USE_FPU")
        self.assertEqual(flag.argument_str, "softfp")

    def test_module_find_flag_by_name_not_found_exception(self):
        self.assertRaises(
            FlagNotFoundException,
            self.aos_module.find_flag_by_name,
            'USE_FPU')

    def test_module_resolve_module(self):
        self.aos_module.create_global_flags(self.search_results)
        self.assertFalse(self.aos_module.is_resolved())
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
        self.assertEqual(
            self.aos_module.find_flag_by_name("USE_FPU_OPT").args[0].name,
            "-mfloat-abi=softfp"
        )

    def test_module_resolve_multiple_flags(self):
        self.search_results.append(("USE_FANCY_EXCEPTIONS_STACK", "-stack-usage=$(USE_EXCEPTIONS_STACKSIZE)"))
        self.search_results.append(("USE_RANDOM_VALUE", "-set-seed=$(RAND_SEED)"))
        self.search_results.append(("RAND_SEED", "42"))
        self.aos_module.create_global_flags(self.search_results)
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
        exc_flag = self.aos_module.find_flag_by_name("USE_FANCY_EXCEPTIONS_STACK")
        rval_flag = self.aos_module.find_flag_by_name("USE_RANDOM_VALUE")
        self.assertEqual(exc_flag.args[0].name, "-stack-usage=0x400")
        self.assertEqual(rval_flag.args[0].name, "-set-seed=42")

    def test_module_cannot_resolve_all_flags(self):
        # TODO: not sure yet what's the best approach
        # therefore raise exception if resolution fails
        self.search_results.append(("USE_RANDOM_VALUE", "-set-seed=$(USE_UNKNOWN_FLAG)"))
        self.aos_module.create_global_flags(self.search_results)
        self.assertRaises(FlagNotFoundException, self.aos_module.resolve)

    def test_module_resolve_multiple_args_with_same_sub_flag(self):
        self.search_results.append(("USE_THIS_SUB", "42"))
        self.search_results.append(("USE_CASE1", "-case1=$(USE_THIS_SUB)"))
        self.search_results.append(("USE_CASE2", "-case2=$(USE_THIS_SUB)"))
        self.search_results.append(("USE_CASE3", "-case3=$(USE_THIS_SUB)"))
        self.aos_module.create_global_flags(self.search_results)
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
