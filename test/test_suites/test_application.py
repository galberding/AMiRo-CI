from unittest.case import skip
import unittest

from amirotest.controller.build_controller import BuildController
from amirotest.controller.build_executer import ParallelExecutor
from amirotest.tools.replace_config_builder import YamlReplConf
from amirotest.tools.config_path_finder import  AosPathManager


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.p_man = AosPathManager()
        self.bc = BuildController(self.p_man,YamlReplConf(self.p_man.get_repl_conf_path()), ParallelExecutor(self.p_man))

    @skip('Takes up to am hour to complete')
    def test_compile_pipeline(self):
        modules = self.bc.execute_build_modules()
        # print(modules[0].build_info)
