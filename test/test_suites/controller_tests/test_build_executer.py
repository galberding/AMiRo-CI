from amirotest.controller.build_controller import BuildController
from amirotest.model.aos_module import AosModule
from amirotest.tools.config_path_finder import AosConfigFinder
from amirotest.tools.replace_config_builder import ReplaceConfig, YamlReplConf
from ..test_utils.module_creation_helper import AosModuleHelper
import unittest

from amirotest.controller.build_executer import SerialExecutor
from amirotest.tools.aos_module_default_config_creatro import AosModuleLoader


class TestExecutor(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = AosModuleHelper()
        self.finder = AosConfigFinder(self.helper.helper.aos_path)
        self.repl_conf = YamlReplConf(self.finder.get_repl_conf_path())
        self.bc = BuildController(self.repl_conf, SerialExecutor)

    def test_executer_init(self):
        exe = SerialExecutor(self.finder.b_dir)
        exe.build(self.get_configured_modules())


    def get_configured_modules(self) -> list[AosModule]:
        tmpl = self.bc.generate_template_modules_from_repl_conf()
        return self.bc.generate_configured_modules_from_template(tmpl[0])
