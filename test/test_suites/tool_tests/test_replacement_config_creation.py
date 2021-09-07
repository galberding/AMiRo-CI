from pathlib import Path
from typing import Optional
import unittest
from unittest.case import skip

from overrides.overrides import overrides
from amirotest.tools.config.dependency_checker import ConfTag
from amirotest.tools.config_path_finder import  AosPathManager
from amirotest.tools.replace_config_builder import YamlReplConf
from ..test_utils.module_creation_helper import AosModuleHelper
from ..test_utils import PathHelper


class ReplacementConfStub(YamlReplConf):
    @overrides
    def get_config(self, conf_path: Path) -> Optional[dict]:
        return {
            ConfTag.Modules.name: ['TestModule'],
            ConfTag.Apps.name: ['TestApp'],
            ConfTag.Options.name: {
                'OptionGroup1': {
                    'opt1': ['true', 'false'],
                    'opt2': ['true', 'false']
                },
                'OptionGroup2': {
                    'opt3': ['true', 'false'],
                    'opt4': ['true', 'false']
                }
            }
        }


class TestReplacementConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.conf_finder = AosPathManager()
        self.repl_conf = ReplacementConfStub(self.conf_finder.get_repl_conf_path())

    def test_check_if_config_exists(self):
        self.assertTrue(self.repl_conf.is_valid())

    def test_get_module_names(self):
        self.assertEqual(self.repl_conf.get_module_names(),
                         ['TestModule'])

    def test_get_option_groups(self):
        # self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertEqual(2, len(self.repl_conf.get_option_groups()))


    def test_get_apps(self):
        self.assertEqual(['TestApp'], self.repl_conf.apps)

    def test_get_flatten_config(self):
        self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertAlmostEqual(4, len(self.repl_conf.get_flatten_config()))

    # TODO:
    # - Check malformat exceptions
    # - Check invalid path
