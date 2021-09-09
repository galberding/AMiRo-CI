import unittest
from unittest.mock import patch
from io import StringIO
from amirotest.tools.cli_parser import AmiroParser
from amirotest.tools.config_path_finder import AosPathManager, AppsPathManager


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = AmiroParser()

    def test_display_help(self):
        self.assertRaises(SystemExit, self.parser.parse_args, ['-h'])

    def test_aos_set(self):
        res = self.parser.parse_args(['--aos'])
        self.assertTrue(res.aos)
        self.assertFalse(res.apps)

    def test_apps_set(self):
        res = self.parser.parse_args(['--apps'])
        self.assertTrue(res.apps)
        self.assertFalse(res.aos)

    def test_both_not_allowed(self):
        with patch('sys.stderr', new = StringIO()):
            self.assertRaises(SystemExit, self.parser.parse_args, ['--apps', '--aos'])
            # print(fake_out)

    def test_no_arg_provided(self):
        with patch('sys.stderr', new = StringIO()):
            self.assertRaises(SystemExit, self.parser.parse_args, [])

    def test_aos_pman_is_selected(self):
        self.parser.parse_args(['--aos'])
        self.assertTrue(isinstance(self.parser.p_man, AosPathManager))

    def test_apps_pman_is_selected(self):
        self.parser.parse_args(['--apps'])
        self.assertTrue(isinstance(self.parser.p_man, AppsPathManager))
