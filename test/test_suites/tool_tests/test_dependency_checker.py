from pathlib import Path
import unittest

from ..test_utils.build_executer_fake import BuildExecutorDummy
from ..test_utils.replace_conf_stub import ReplaceConfigWithDependenciesStub

from amiroci.model.aos_module import AosModule
from amiroci.model.option.aos_opt import AosOption
from amiroci.controller.build_controller import BuildController
from amiroci.tools.path_manager import AosPathManager
from amiroci.tools.config.dependency_checker import DependencyChecker
import logging


class TestDependencyChecker(unittest.TestCase):
    def setUp(self):
        self.p_man = AosPathManager()
        self.repl_conf = ReplaceConfigWithDependenciesStub(Path())
        self.dep_checker = DependencyChecker(self.repl_conf.get_dependencies())
        self.bc = BuildController(self.repl_conf)
        self.modules = self.bc.c_modules
        self.bc.log.setLevel(logging.DEBUG)

    def test_init(self):
        self.assertTrue(self.dep_checker.has_dependencies())

    def test_dep_all_modules_pass_when_no_dependency_given(self):
        checker = DependencyChecker({})
        self.assertTrue(checker.is_valid(self.create_module()))

    def test_no_dependency_met(self):
        module = self.create_module(dep1=False)
        self.assertTrue(self.dep_checker.is_valid(module))

    def test_module_dep_accepted(self):
        module = self.create_module()
        self.assertTrue(self.dep_checker.is_valid(module))

    def test_dep1_rejected(self):
        module = self.create_module(dep2=False)
        self.assertFalse(self.dep_checker.is_valid(module))

    def test_dep3_rejected(self):
        module = self.create_module(dep3=False, dep4=True)
        self.assertFalse(self.dep_checker.is_valid(module))

    def test_dep5_rejected(self):
        module = self.create_module(dep5=False)
        self.assertFalse(self.dep_checker.is_valid(module))

    def test_dep5_accepted(self):
        module = self.create_module(
            dep5=False, dep6=False, dep7=False, dep8=False
        )
        self.assertTrue(self.dep_checker.is_valid(module))

    def create_module(
        self,
        dep1=True,
        dep2=True,
        dep3=True,
        dep4=True,
        dep5=True,
        dep6=True,
        dep7=True,
        dep8=True
    ) -> AosModule:
        module = AosModule(Path('Test'))
        module.add_options(
            [
                AosOption('dep1', str(dep1)),
                AosOption('dep2', str(dep2)),
                AosOption('dep3', str(dep3)),
                AosOption('dep4', str(dep4)),
                AosOption('dep5', str(dep5)),
                AosOption('dep6', str(dep6)),
                AosOption('dep7', str(dep7)),
                AosOption('dep8', str(dep8)),
            ]
        )
        return module
