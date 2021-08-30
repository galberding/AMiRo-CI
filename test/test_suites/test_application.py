from unittest.case import SkipTest, skip
from amirotest.controller.build_controller import BuildController
from amirotest.controller.build_executer import ParallelExecutor, SerialExecutor
from .test_utils.test_helper import PathHelper
import unittest

from amirotest.tools.config_path_finder import AosModuleConfigFinder, AosPathManager


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.path_helper = PathHelper()
        self.finder = AosPathManager(self.path_helper.aos_path)
        self.bc = BuildController(self.finder, ParallelExecutor(self.finder), None)

    # @SkipTest
    def test_compile_pipeline(self):
        modules = self.bc.execute_build_modules()
        print(modules[0].build_info)
