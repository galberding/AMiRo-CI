from amirotest.tools import YamlDumper, yml_load, Loader
from amirotest.tools import YamlDumper
from ..test_utils import AosModuleHelper, PathHelper
import unittest

class TestModuleDumping(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.path_helper.create_test_env()
        self.module_helper = AosModuleHelper()
        self.nucleo_module = self.module_helper.get_nucleo_with_options()
        self.config_path = self.path_helper.get_default_config_yml_path()

    def test_yaml_dumper_create_if_not_exists(self):
        dumper = YamlDumper()
        dumper.dump(self.nucleo_module, self.config_path)
        self.assertTrue(self.config_path.exists())

    def test_yaml_write_module_to_file(self):
        dumper = YamlDumper()
        dumper.dump(self.nucleo_module, self.config_path)
        conf = self.load_config()
        self.assertIn("NUCLEO-L476RG", conf)

    def test_dump_several_modules(self):
        modules = self.module_helper.get_modules_with_options(self.module_helper.module_names)
        dumper = YamlDumper()
        dumper.dump_all(modules, self.config_path)
        conf = self.load_config()
        for module_name in self.module_helper.module_names:
            self.assertIn(module_name, conf)

    def load_config(self):
        with self.config_path.open() as f:
            conf = yml_load(f, Loader=Loader)
        return conf

    def tearDown(self) -> None:
        self.path_helper.clear_test_env()
        pass
