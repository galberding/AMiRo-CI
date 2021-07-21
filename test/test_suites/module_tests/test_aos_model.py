from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.model.aos_model import Argument, Flag, FlagNotFoundException, Module
from amirotest.tools.makefile_search import MakefileSearch

class TestAosModel(unittest.TestCase):

    def setUp(self) -> None:
        self.searcher = MakefileSearch()
        self.helper = PathHelper()
        self.aos_module = self.helper.get_aos_module()
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


    def test_create_arguments(self):
        arg = Argument("-WALL")
        self.assertEqual(arg.name, "-WALL")

    def test_create_flag(self):
        name = "flag"
        wall = "-WALL"
        dtest = "-Dtest"
        arg_string = " ".join([wall, dtest])
        args = [Argument(wall), Argument(dtest)]
        flag = Flag(name, arg_string)
        self.assertEqual(flag.name, name)
        self.assertEqual(set(flag.args),set(args))

    def test_flag_has_unresolved_arguments(self):
        # example: -mfloat-abi=$(USE_FPU)
        unresolved_flag = Flag('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        self.assertFalse(unresolved_flag.is_resolved())

    def test_create_module(self):
        self.assertEqual(self.aos_module.name, self.module_name)

    def test_module_get_makefile(self):
        makefile = self.aos_module.get_makefile()
        self.assertTrue(makefile.exists())

    def test_module_build_flags(self):
        self.aos_module.create_flags(self.search_results)
        self.assertEqual(len(self.aos_module.flags), len(self.search_results))

    def test_module_has_no_flags_is_resolved(self):
        self.assertTrue(self.aos_module.is_resolved())

    def test_module_has_flags_is_resolved(self):
        search_results = [
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfpu=fpv4-sp-d16')
        ]
        self.aos_module.create_flags(search_results)
        self.assertTrue(self.aos_module.is_resolved())

    def test_module_has_flags_is_unresolved(self):
        search_results = [
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        ]
        self.aos_module.create_flags(search_results)
        self.assertFalse(self.aos_module.is_resolved())

    def test_get_substitution_flag_from_argument(self):
        unresolved_flag = Flag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        sub_flags = unresolved_flag.get_substitution_flags()
        self.assertEqual(len(sub_flags), 1)
        self.assertEqual(sub_flags[0], 'USE_FPU')

    def test_get_substitution_flag_from_argument_no_sub_flag(self):
        resolved_flag = Flag(
            'USE_FPU_OPT',
            '-mfloat-abi=no -mfpu=fpv4-sp-d16')
        self.assertTrue(resolved_flag.is_resolved())

        # Accessing substitution flags from resolved arguments
        # results in an empty list
        sub_flags = resolved_flag.get_substitution_flags()
        self.assertEqual(sub_flags, list())

    def test_get_substitution_flag_from_argument_multiple_sub_flag(self):
        unresolved_flag = Flag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=$(USE_MPU_TYPE)')
        sub_flags = unresolved_flag.get_substitution_flags()
        self.assertEqual(sub_flags, ['USE_FPU', 'USE_MPU_TYPE'])

    def test_model_substitute_unresolved_flag(self):
        self.aos_module.create_flags(self.search_results)
        u_flags = self.aos_module.get_unresolved_flags()
        self.assertEqual(len(u_flags), 1)
        # get only flag that needs to be substituted
        self.assertEqual(u_flags[0].name, "USE_FPU_OPT")


    def test_model_search_flag(self):
        self.aos_module.create_flags(self.search_results)
        flag = self.aos_module.find_flag_by_name('USE_FPU')
        self.assertEqual(flag.name, "USE_FPU")
        self.assertEqual(flag.argument_str, "softfp")

    def test_module_search_flag_not_found_exception(self):
        self.assertRaises(
            FlagNotFoundException,
            self.aos_module.find_flag_by_name,
            'USE_FPU')

    def test_resolve_unresolved_flag(self):
        unresolved_flag = Flag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU)')
        self.assertFalse(unresolved_flag.is_resolved())
        self.assertTrue(unresolved_flag.resolve(
            Flag("USE_FPU", "fpu_value")))
        self.assertTrue(unresolved_flag.is_resolved())
        self.assertEqual(
            unresolved_flag.args[0].name,
            '-mfloat-abi=fpu_value'
        )

    def test_resolve_module(self):
        self.aos_module.create_flags(self.search_results)
        self.assertFalse(self.aos_module.is_resolved())
        self.aos_module.resolve()
        self.assertTrue(self.aos_module.is_resolved())
        self.assertEqual(
            self.aos_module.find_flag_by_name("USE_FPU_OPT").args[0].name,
            "-mfloat-abi=softfp"
        )

    # Flag substitute value
