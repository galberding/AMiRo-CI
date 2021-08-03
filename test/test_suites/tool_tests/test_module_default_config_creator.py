from amirotest.model.option import GlobalOption, UserOption
from amirotest.tools import YamlDumper, yml_load, Loader
from amirotest.tools import YamlDumper, YamlLoader
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

class TestModuleLoading(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        # self.path_helper.create_test_env()
        self.module_helper = AosModuleHelper()
        self.nucleo_module = self.module_helper.get_nucleo_with_options()
        self.config_path = self.path_helper.get_assets_default_config_path()

    def test_load_modules_from_asset_config(self):
        loader = YamlLoader()
        config = loader.get_config(self.config_path)
        modules = loader.load(self.config_path)
        self.assertEqual(len(modules), len(self.module_helper.module_names))
        for module in modules:
            self.assertIn(module.name, self.module_helper.module_names)
            self.assertGreater(len(module.options), 0)
            # Check global options
            for option, args in config[module.name][GlobalOption.__name__].items():
                self.assertTrue(module.find_option_by_name(option))
            if UserOption.__name__ in config[module.name]:
                for option, args in config[module.name][UserOption.__name__].items():
                    mod_opt = module.find_option_by_name(option)
                    self.assertTrue(mod_opt)
                    for mod_args in mod_opt.args:
                        self.assertIn(mod_args.name, args)
