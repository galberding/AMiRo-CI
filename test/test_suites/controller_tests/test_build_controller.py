from pathlib import Path

import unittest
from unittest.mock import MagicMock
from amiroci.controller.build_controller import BuildController
from amiroci.model.aos_module import AosModule
from amiroci.model.option.aos_opt import MakeOption
from amiroci.tools.config.config_tags import ConfTag
from amiroci.tools.path_manager import AosPathManager

from ..test_utils.replace_conf_stub import ReplacementConfWithAppsStub, ReplacementConfWithSubgroupsStub
import logging

class TestBuildController(unittest.TestCase):
    def setUp(self) -> None:
        self.p_man = AosPathManager()
        self.executer_mock = MagicMock()
        self.executer_mock.build = MagicMock()
        self.bc = BuildController(
            ReplacementConfWithAppsStub(list_apps=False))
        self.bc.log.setLevel(logging.WARN)

    def test_build_generate_conf_matrix(self):
        config_mat = self.bc.generate_config_matrix()
        # 4 option are provided
        self.assertEqual(4, config_mat.shape[1])

    def test_generate_template_modules(self):
        modules = self.bc.generate_template_modules_from_repl_conf()
        self.assertEqual(1, len(modules))
        [self.assertTrue(isinstance(module, AosModule)) for module in modules]
        [self.assertFalse(module.is_resolved()) for module in modules]

    def test_generate_configured_modules(self):
        c_modules = self.bc.c_modules
        # 4 Options with 2 arguments each
        self.assertEqual(16, len(c_modules))
        [self.assertTrue(module.is_resolved()) for module in c_modules]

    # def test_pass_configured_modules_to_build_exe(self):
    #     exe_modules = self.bc.execute_build_modules()
    #     self.assertGreater(len(exe_modules), 0)
    #     self.executer_mock.build.assert_called()

    def test_module_name_generation_for_aos(self):
        t_modules = self.bc.generate_template_modules_from_repl_conf()
        self.assertEqual(1, len(t_modules))

    def test_module_name_generation_for_apps(self):
        self.set_replace_conf_apps(True)
        t_modules = self.bc.generate_template_modules_from_repl_conf()
        self.assertEqual(2, len(t_modules))

    def set_replace_conf_apps(self, list_apps):
        self.bc.repl_conf.list_apps = list_apps
        self.bc.repl_conf.load(Path())

    # test external conf matrix and what happens if it is misconfigured
    # test module name generation for aos and for apps


class TestMakeOptionCreation(unittest.TestCase):
    def setUp(self) -> None:
        repl_conf = ReplacementConfWithSubgroupsStub()
        self.bc = BuildController(repl_conf, None) # type: ignore

    def test_make_option_generation(self):
        opts = self.bc._generate_template_options()
        self.assertIn(MakeOption('USE_OPT', ['-1', '-2', '-3=4']), opts)
