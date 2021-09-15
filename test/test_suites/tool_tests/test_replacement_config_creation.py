from pathlib import Path
from typing import Optional
import unittest
from amirotest.tools.config_path_finder import  AosPathManager
from ..test_utils.replace_conf_stub import ReplacementConfWithAppsStub, ReplacementConfWithSubgroupsStub


class TestReplacementConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.conf_finder = AosPathManager()
        self.repl_conf = ReplacementConfWithAppsStub(list_apps=True)

    def test_check_if_config_exists(self):
        self.assertTrue(self.repl_conf.is_valid())

    def test_get_module_names(self):
        self.assertEqual(self.repl_conf.get_module_names(),
                         ['TestModule'])

    def test_get_option_groups(self):
        self.assertEqual(2, len(self.repl_conf.filter_option_groups()))

    def test_get_apps(self):
        self.assertEqual(['TestApp1', 'TestApp2'], self.repl_conf.apps)

    def test_stub_exclude_apps(self):
        rp_stub = ReplacementConfWithAppsStub(list_apps=False)
        self.assertEqual([], rp_stub.apps)

    def test_get_flatten_config(self):
        self.repl_conf.load(self.conf_finder.get_repl_conf_path())
        self.assertAlmostEqual(4, len(self.repl_conf.get_flatten_config()))


    # def test
    # TODO:
    # - Check malformat exceptions
    # - Check invalid path


class TestReplacementConfigSuboptions(unittest.TestCase):
    def setUp(self) -> None:
        # self.conf_finder = AosPathManager()
        self.repl_conf = ReplacementConfWithSubgroupsStub()

    def test_detect_option_groups(self):
        groups = self.repl_conf.filter_option_groups()
        self.assertEqual(8, len(groups))
        self.check_group_contains(
            groups,
            ['Opt1','Sub1', 'Opt2', 'Sub2', 'Sub3', 'SubSub1', 'Empty_Opt3', 'Sub4'])

    def test_exclude_options(self):
        """Opt1: -- exclude
               Sub1: -- exclude
           Opt2:
               Sub2:
               Sub3: -- exclude
                    SubSub1 -- exclude
           Empty_Opt3:
               Sub4:
        """
        groups = self.repl_conf.filter_option_groups(exclude=['Opt1', 'Sub3'])
        self.check_group_contains(groups, ['Opt2', 'Sub2', 'Empty_Opt3', 'Sub4'])

    def test_include_options(self):
        groups = self.repl_conf.filter_option_groups(include=['Opt1'])
        self.check_group_contains(groups, ['Opt1', 'Sub1'])

    def check_group_contains(self, group, names):
        for name, _ in group.items():
            self.assertIn(name, names)


class TestReplacementConfigReadExcludeIncludeTagStub(unittest.TestCase):
    pass
