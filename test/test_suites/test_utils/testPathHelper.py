from .path_helper import PathHelper
import unittest

# @unittest.SkipTest
class TestPathHelper(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = PathHelper()
        self.module_names = [
            "DiWheelDrive_1-1",
            "DiWheelDrive_1-2",
            "LightRing_1-0",
            "LightRing_1-2",
            "NUCLEO-F103RB",
            "NUCLEO-F401RE",
            "NUCLEO-F767ZI",
            "NUCLEO-G071RB",
            "NUCLEO-L476RG",
            "PowerManagement_1-1",
            "PowerManagement_1-2",
            "STM32F407G-DISC1",
        ]

    def test_check_if_all_modules_are_listed(self):
        aos_modules = self.helper.listAosModules()
        for module_name in aos_modules:
            self.assertIn(module_name.name, self.module_names)

    def test_check_if_right_modules_are_found(self):
        aos_modules = [i.name for i in self.helper.listAosModules()]
        for module_name in self.module_names:
            self.assertIn(module_name, aos_modules)
