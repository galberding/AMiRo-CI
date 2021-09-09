import shutil
import unittest

from ..test_utils.build_executer_fake import SerialExecutorFake
from amirotest.controller.build_controller import BuildController
from amirotest.model.aos_module import AosModule
from amirotest.tools.config_path_finder import AosPathManager
from amirotest.tools.replace_config_builder import YamlReplConf



# @unittest.SkipTest
class TestExecutor(unittest.TestCase):
    def setUp(self) -> None:
        self.p_man = AosPathManager()
        self.bc = BuildController(
            self.p_man,
            YamlReplConf(self.p_man.get_repl_conf_path()), SerialExecutorFake(self.p_man))

    def tearDown(self) -> None:
        shutil.rmtree(self.p_man.get_build_dir())
        # pass

    def test_execution_results_passed_to_module(self):
        exe = SerialExecutorFake(self.p_man)
        modules = self.get_configured_modules()
        exe.build(modules)
        for module in modules:
            self.assertTrue(module.build_info)

    def get_configured_modules(self) -> list[AosModule]:
        tmpl = self.bc.generate_template_modules_from_repl_conf()
        return self.bc.generate_configured_modules_from_template(tmpl[0])
