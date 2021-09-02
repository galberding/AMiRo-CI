from typing import Type
from unittest.case import skip
from ..test_utils.module_creation_helper import AosModuleHelper
import unittest
from unittest.mock import MagicMock
from pathlib import Path
from amirotest.controller.build_controller import BuildController
from amirotest.controller.build_executer import SerialExecutor
from amirotest.model.aos_module import AosModule
from amirotest.tools.config_path_finder import AosPathManager
from amirotest.tools.replace_config_builder import YamlReplConf


class TestBuildController(unittest.TestCase):
    def setUp(self) -> None:
        self.module_helper = AosModuleHelper()
        self.finder = AosPathManager(self.module_helper.helper.aos_path)
        self.bc = BuildController(self.finder, YamlReplConf(self.finder.get_repl_conf_path()), SerialExecutor(self.finder))

    @skip('poor test design')
    def test_build_generate_conf_matrix(self):
        config_mat = self.bc.generate_config_matrix()
        self.assertEqual(6, config_mat.shape[1])

    def test_generate_template_modules(self):
        modules = self.bc.generate_template_modules_from_repl_conf()
        self.assertEqual(12, len(modules))
        [self.assertTrue(isinstance(module, AosModule)) for module in modules]
        [self.assertFalse(module.is_resolved()) for module in modules]

    def test_generate_configured_modules(self):
        c_modules = self.get_configured_modules(self.bc)
        # 6 Options with 2 arguments each
        self.assertEqual(2**6, len(c_modules))
        [self.assertTrue(module.is_resolved()) for module in c_modules]

    def test_pass_configured_modules_to_build_exe(self):
        executer_mock = MagicMock()
        executer_mock.build = MagicMock()
        bc = BuildController(self.finder, YamlReplConf(self.finder.get_repl_conf_path()), executer_mock)
        # c_modules = self.get_configured_modules(bc)
        exe_modules = bc.execute_build_modules()

        self.assertGreater(len(exe_modules), 0)
        executer_mock.build.assert_called()


    def get_configured_modules(self, bc) -> list[AosModule]:
        """Create template modules and configure them.
        """
        modules = bc.generate_template_modules_from_repl_conf()
        return bc.generate_configured_modules_from_template(modules[0])
