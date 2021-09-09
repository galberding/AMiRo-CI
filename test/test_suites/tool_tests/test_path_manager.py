import os
from pathlib import Path
from amirotest.tools.config_path_finder import AosEnv, AosPathManager, AppsPathManager
import unittest


def set_env_entry(name: str, value: str):
    if name not in os.environ \
       or not Path(os.environ[name]).exists():
        os.environ[name] = value


def set_env_if_not_existing():
    set_env_entry(AosEnv.AOS_ROOT.name, '/home/schorschi/hiwi/AMiRo-OS')
    set_env_entry(AosEnv.AOS_APPS_ROOT.name, '/home/schorschi/hiwi/AMiRo-Apps')
    set_env_entry(AosEnv.AOS_REPLACE_CONF.name, '/home/schorschi/hiwi/amiroci/assets/repl_conf.yml')


class TestAosConfigManager(unittest.TestCase):
    def setUp(self) -> None:
        set_env_if_not_existing()
        self.p_man = AosPathManager()

    def test_read_aos_root_from_environmen_without_default(self):
        # os.environ[AosEnv.AOS_ROOT.name] = ''
        p_man = AosPathManager()
        self.assertEqual(Path(os.environ[AosEnv.AOS_ROOT.name]), p_man.root)

    def test_aos_set_path_directly(self):
        test_path = os.environ[AosEnv.AOS_ROOT.name]
        os.environ[AosEnv.AOS_ROOT.name] = 'some/wrong/vaue'
        p_man = AosPathManager(Path(test_path))
        self.assertEqual(Path(test_path), p_man.root)

    def test_get_module_makefile(self):
        test_path = Path(os.environ[AosEnv.AOS_ROOT.name])
        make_path = self.p_man.get_module_makefile(Path('DiWheelDrive_1-1'))
        self.assertEqual(
            test_path.joinpath('modules/Makefile'),
            make_path
        )



class TestAppsManager(unittest.TestCase):
    def setUp(self) -> None:
        set_env_if_not_existing()
        # self.aos_finder = AosModuleConfigFinder(self.nucleo.path)
        self.p_man = AppsPathManager()


    def test_makefile_generation(self):
        apps_root = Path(os.environ[AosEnv.AOS_APPS_ROOT.name])
        test_path = apps_root.joinpath(Path('configurations/HelloWorld/Makefile'))
        self.assertEqual(
            test_path,
            self.p_man.get_module_makefile(Path('HelloWorld/DiWheelDrive_1-1'))
        )

    # def

    # root can be provided by environment as fallback or by ARGUMENT
    # check if root exists and make validity check one for aos and one for AppsConfigFinder
    # gather all apps in amiro apps
    # fall back to environment in case the provided root does not exists and do not match the expectations
    # this could be the case if no makefile or module dicectory is found in the root
