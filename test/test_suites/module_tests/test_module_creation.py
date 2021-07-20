from amirotest.tools.searcher import Searcher
from ..test_utils.path_helper import PathHelper
import unittest

from amirotest.model.aos_module import AOSModule, AOSModuleFactory


@unittest.SkipTest
class TestAosModuleCreation(unittest.TestCase):
    def setUp(self):
        self.searcher = Searcher()
        self.helper = PathHelper()
        self.factory = AOSModuleFactory()
        self.module_path = self.helper.get_aos_module_path(module_name="NUCLEO-L476RG")

    def test_nucleo_creation_with_factory(self):
        aos_module = self.factory.buildModule(self.module_path)
        self.assertEqual(aos_module.path.name, self.module_path.name)

    def test_factory_compile_flag_creation(self):
        results = self.searcher.search_if_defined_flags(self.module_path)
        compile_flags = self.factory._generate_compile_flags(results)
        count_result_flags = 0
        for res in results:
            count_result_flags += len(res.flags)
        self.assertLessEqual(len(compile_flags), count_result_flags)

    def test_factory_flags_set_in_module(self):
        module = self.factory.buildModule(self.module_path)
        for flag in module.flags:
            print(flag.name)
        compile_flags = self.factory._generate_compile_flags(
            self.searcher.search_if_defined_flags(
                self.module_path))
        self.assertTrue(module.flags.issubset(compile_flags))
