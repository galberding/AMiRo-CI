import os
from pathlib import Path
import shutil
from ..test_utils.build_executer_fake import SerialExecutorFake
from amirotest.controller.build_controller import BuildController
from amirotest.model.aos_module import AosModule
from amirotest.model.option.aos_opt import AosOption
from amirotest.tools.config_path_finder import AosPathManager
from amirotest.tools.replace_config_builder import YamlReplConf
from ..test_utils.module_creation_helper import AosModuleHelper
import unittest

from amirotest.controller.build_executer import SerialExecutor

# @unittest.SkipTest
class TestExecutor(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = AosModuleHelper()
        self.finder = AosPathManager(self.helper.helper.aos_path)
        self.repl_conf = YamlReplConf(self.finder.get_repl_conf_path())
        self.bc = BuildController(self.finder, YamlReplConf(self.finder.get_repl_conf_path()), SerialExecutorFake(self.finder))
    def tearDown(self) -> None:
        shutil.rmtree(self.finder.get_build_dir())
        # pass

    def test_execution_results_passed_to_module(self):
        exe = SerialExecutorFake(self.finder)
        modules = self.get_configured_modules()
        exe.build(modules)
        for module in modules:
            # print(module.build_info.duration)
            self.assertTrue(module.build_info)

    def get_configured_modules(self) -> list[AosModule]:
        tmpl = self.bc.generate_template_modules_from_repl_conf()
        return self.bc.generate_configured_modules_from_template(tmpl[0])
