from ..test_utils.module_creation_helper import AosModuleHelper
import unittest
from pathlib import Path
from amirotest.controller.build_controller import BuildController
from amirotest.controller.build_executer import SerialExecutor
from amirotest.model.aos_module import AosModule
from amirotest.tools.config_path_finder import AosPathManager
from amirotest.tools.replace_config_builder import YamlReplConf


class TestBuildController(unittest.TestCase):
    def setUp(self) -> None:
        self.module_helper = AosModuleHelper()
        self.config = {"Module": ["Name1", "Name2"],
                       "Config":{
                       "Aosconf":{
                           "Opt1": [1,2],
                           "Opt2": [1,2]},
                       "AnotherConf":{
                           "OS_OPT": ["true", "false"],
                           "OS_SHELL": ["on", "off"]}}}
        # self.repl_conf = YamlReplConf(Path("/home/schorschi/hiwi/amiroci/assets/repl_conf.yml"))
        self.finder = AosPathManager(self.module_helper.helper.aos_path)
        self.bc = BuildController(self.finder, SerialExecutor)

    def test_build_generate_conf_matrix(self):
        config_mat = self.bc.generate_config_matrix()
        self.assertEqual(6, config_mat.shape[1])

    def test_generate_template_modules(self):
        modules = self.bc.generate_template_modules_from_repl_conf()
        self.assertEqual(12, len(modules))
        [self.assertTrue(isinstance(module, AosModule)) for module in modules]
        [self.assertFalse(module.is_resolved()) for module in modules]
        # for opt in modules[0].options:
            # print(opt.get_build_option())

    def test_generate_configured_modules(self):
        modules = self.bc.generate_template_modules_from_repl_conf()
        c_modules = self.bc.generate_configured_modules_from_template(modules[0])
        # 6 Option with 2 arguments each
        self.assertEqual(2**6, len(c_modules))
        [self.assertTrue(module.is_resolved()) for module in c_modules]
