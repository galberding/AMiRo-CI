from unittest.case import SkipTest, skip
from amirotest.controller.build_controller import BuildController
from amirotest.controller.build_executer import ParallelExecutor, SerialExecutor
from amirotest.tools.replace_config_builder import YamlReplConf
from .test_utils.test_helper import PathHelper
import unittest

from amirotest.tools.config_path_finder import  AosPathManager


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.path_helper = PathHelper()
        self.finder = AosPathManager(self.path_helper.aos_path)
        self.bc = BuildController(self.finder,YamlReplConf(self.finder.get_repl_conf_path()), ParallelExecutor(self.finder))

    @skip('Takes up to am hour to complete')
    def test_compile_pipeline(self):
        modules = self.bc.execute_build_modules()
        # print(modules[0].build_info)
