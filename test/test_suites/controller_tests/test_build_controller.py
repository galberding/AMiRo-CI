import unittest
from pathlib import Path
from amirotest.controller.build_controller import BuildController
from amirotest.model.aos_module import AosModule
from amirotest.tools.replace_config_builder import YamlReplConf

class TestBuildController(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {"Module": ["Name1", "Name2"],
                       "Config":{
                       "Aosconf":{
                           "Opt1": [1,2],
                           "Opt2": [1,2]},
                       "AnotherConf":{
                           "OS_OPT": ["true", "false"],
                           "OS_SHELL": ["on", "off"]}}}
        self.repl_conf = YamlReplConf()
        self.repl_conf.load(
            Path("/home/schorschi/hiwi/amiroci/assets/repl_conf.yml"))
        self.bc = BuildController(self.repl_conf)

    def test_build_generate_conf_matrix(self):
        config_mat = self.bc.generate_config_matrix()
        self.assertEqual(16, config_mat.shape[1])

    def test_generate_template_modules(self):
        modules = self.bc.generate_template_modules_from_repl_conf()
        self.assertEqual(12, len(modules))
        [self.assertTrue(isinstance(module, AosModule)) for module in modules]
        [self.assertFalse(module.is_resolved()) for module in modules]
        for opt in modules[0].options:
            print(opt.get_build_option())
