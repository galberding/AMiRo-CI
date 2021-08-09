import unittest
from amirotest.tools import YamlDumper, yml_load, Loader
from amirotest.tools import YamlDumper
from amirotest.tools.config_path_finder import AosConfigFinder
from amirotest.tools.replace_config_builder import YamlReplConf
from ..test_utils.module_creation_helper import AosModuleHelper
from ..test_utils import PathHelper

class TestReplacementConfigCreation(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.conf_finder = AosConfigFinder(self.path_helper.aos_path)
        self.repl_conf = YamlReplConf()

    def test_check_if_config_exists(self):
        self.assertFalse(self.repl_conf.is_valid())
        self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertTrue(self.repl_conf.is_valid())

    def test_get_module_names(self):
        self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertEqual(self.repl_conf.get_module_names(),
                         self.module_helper.module_names)

    def test_get_options(self):
        self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertEqual(1, len(self.repl_conf.get_options()))

    def test_get_flatten_config(self):
        self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertAlmostEqual(16, len(self.repl_conf.get_flatten_config()))
