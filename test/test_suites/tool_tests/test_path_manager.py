import os
from pathlib import Path
from unittest.case import skip

from amirotest.tools.config_path_finder import AosEnv, AosPathManager, CannotFindConfigError
from ..test_utils import PathHelper, AosModuleHelper
import unittest


class TestConfigPathFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_helper = AosModuleHelper()
        self.nucleo = self.module_helper.get_aos_module()
        self.set_env_if_not_existing()
        # self.aos_finder = AosModuleConfigFinder(self.nucleo.path)


    def set_env_if_not_existing(self):
        if AosEnv.AOS_ROOT.name not in os.environ:
            os.environ[AosEnv.AOS_ROOT.name] = '/home/schorschi/hiwi/AMiRo-OS'

        if AosEnv.AOS_APPS_ROOT.name not in os.environ:
            os.environ[AosEnv.AOS_APPS_ROOT.name] = '/home/schorschi/hiwi/AMiRo-Apps'


    def test_read_aos_root_from_environmen_without_default(self):
        # os.environ[AosEnv.AOS_ROOT.name] = ''
        p_man = AosPathManager()
        self.assertEqual(Path(os.environ[AosEnv.AOS_ROOT.name]), p_man.aos_root)

    # def test_


        # needs to check if root is provided
    # root can be provided by environment as fallback or by ARGUMENT
    # check if root exists and make validity check one for aos and one for AppsConfigFinder
    # gather all apps in amiro apps
    # fall back to environment in case the provided root does not exists and do not match the expectations
    # this could be the case if no makefile or module dicectory is found in the root
