from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.model.aos_model import Argument, Flag, Module
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
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16') # Needs to be substituted
        ]
        self.aos_module.create_flags(search_results)
        self.assertFalse(self.aos_module.is_resolved())
