import unittest
from amirotest.tools import YamlDumper, yml_load, Loader
from amirotest.tools import YamlDumper
from ..test_utils.module_creation_helper import AosModuleHelper
from ..test_utils.path_helper import PathHelper

class TestReplacementConfigCreation(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()

    def test_check_if_config_exists(self):
        pass

    # Check if default config exists
    # load default config
    # dump defaults to replace config
    # how should they be build??
