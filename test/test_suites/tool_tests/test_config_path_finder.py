from pathlib import Path

from amirotest.tools.config_path_finder import CannotFindConfigError
from ..test_utils import PathHelper, AosModuleHelper
import unittest

from amirotest.tools import AosModuleConfigFinder, CannotFindModuleError



class TestConfigPathFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.nucleo = self.module_helper.get_aos_module()
        self.aos_finder = AosModuleConfigFinder(self.nucleo.path)


    def test_create_aos_connfig_finder(self):
        c_finder = AosModuleConfigFinder(self.path_helper.get_aos_module_path())
        self.assertEqual(self.path_helper.aos_path, c_finder.aos_root)

    def test_create_finde_unknown_module_raise_exception(self):
        self.assertRaises(CannotFindModuleError, AosModuleConfigFinder, Path("non/existent/"))

    def test_aos_get_mod_by_name(self):
        makefile = self.aos_finder._get_module_config_by_name("Makefile")
        self.assertEqual("Makefile", makefile.name)

    def test_get_non_existent_config_raise_exception(self):
        self.assertRaises(CannotFindConfigError, self.aos_finder._get_module_config_by_name, "Unknown_config.h")

    # def test_aos_get_makefile(self):
    #     self.assertEqual("Makefile", self.aos_finder.get_module_makefile().name)

    def test_aos_get_aosconf(self):
        self.assertEqual("aosconf.h", self.aos_finder.get_aosconf("").name)
