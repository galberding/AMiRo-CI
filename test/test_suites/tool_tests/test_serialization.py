from amirotest.tools.aos_serialization import YamlDumper, yml_load, Loader
from ..test_utils.module_creation_helper import AosModuleHelper
from ..test_utils.path_helper import PathHelper
import unittest

class TestModuleDumping(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.path_helper.create_test_env()
        self.module_helper = AosModuleHelper()
        self.nucleo_module = self.module_helper.get_nucleo_with_flags()
        self.config_path = self.path_helper.get_default_config_yml_path()

    def test_yaml_dumper_create_if_not_exists(self):
        dumper = YamlDumper()
        dumper.dump(self.nucleo_module, self.path_helper.get_default_config_yml_path())
        self.assertTrue(self.config_path.exists())

    def test_yaml_write_module_to_file(self):
        dumper = YamlDumper()
        dumper.dump(self.nucleo_module, self.path_helper.get_default_config_yml_path())
        with self.path_helper.get_default_config_yml_path().open() as f:
            module = yml_load(f, Loader=Loader)
            print(module)
            self.assertIn("NUCLEO-L476RG", module)

    def tearDown(self) -> None:
        # self.path_helper.clear_test_env()
        pass
