from amirotest.tools.aos_serialization import YamlDumper
from ..test_utils.module_creation_helper import AosModuleMockData
from ..test_utils.path_helper import PathHelper
import unittest

class TestModuleDumping(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = PathHelper()
        self.module_helper = AosModuleMockData()
        self.nucleo_module = self.module_helper.get_nucleo_with_flags()
        self.config_path = self.helper.get_default_config_yml_path()

    def test_yaml_dumper(self):
        dumper = YamlDumper()
        # dumper.dump(self.nucleo_module, )

    def tearDown(self) -> None:
        pass
