from pathlib import Path
from unittest.case import skip

from amirotest.tools.config_path_finder import CannotFindConfigError
from ..test_utils import PathHelper, AosModuleHelper
import unittest

# from amirotest.tools import AosModuleConfigFinder, CannotFindRootDirectoryError



class TestConfigPathFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.nucleo = self.module_helper.get_aos_module()
        # self.aos_finder = AosModuleConfigFinder(self.nucleo.path)


    def test_init_aos_root_provided(self):
        pass

    # needs to check if root is provided
    # root can be provided by environment as fallback or by ARGUMENT
    # check if root exists and make validity check one for aos and one for AppsConfigFinder
    # gather all apps in amiro apps
    # fall back to environment in case the provided root does not exists and do not match the expectations
    # this could be the case if no makefile or module dicectory is found in the root
