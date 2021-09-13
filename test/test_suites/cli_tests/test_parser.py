from argparse import Namespace
import os
from pathlib import Path
from shutil import copyfile, rmtree
import unittest
from unittest.mock import patch
from io import StringIO
from amirotest.tools.cli_parser import AmiroParser
from amirotest.tools.config_path_finder import AosEnv, AosPathManager, AppsPathManager, NoAosEnvVariableError


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = AmiroParser()
        self.aos_root = os.environ[AosEnv.AOS_ROOT.name]
        self.apps_root = os.environ[AosEnv.AOS_APPS_ROOT.name]
        # Project dir /home/schoschi/hiwi/amiroci
        self.tmp_dir = Path('/home/schorschi/hiwi')
        # self.tmp_dir = Path('/dev/shm/amiroCI')
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        repl_path = Path(os.environ[AosEnv.AOS_REPLACE_CONF.name])
        self.repl_path = self.tmp_dir.joinpath(repl_path.name)
        copyfile(repl_path, self.repl_path)

    def tearDown(self) -> None:
        # rmtree(self.tmp_dir)
        self.set_env()

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

    def test_pass_path(self):
        self.unset_env()
        self.parser.parse_args(['--aos',
                                      '--project-root',
                                      self.aos_root
                                      ])
        self.assertEqual(Path(self.aos_root), self.parser.p_man.root)

        self.parser.parse_args(['--apps',
                                      '--project-root',
                                      self.apps_root
                                      ])
        self.assertEqual(Path(self.apps_root), self.parser.p_man.root)

    def test_pass_path_to_path_manager(self):
        self.unset_env()
        self.assertRaises(NoAosEnvVariableError, self.parser.parse_args, ['--apps'])
        self.assertRaises(NoAosEnvVariableError, self.parser.parse_args, ['--aos'])

    def test_load_replacement_config(self):
        self.parser.parse_args(['--aos'])
        self.assertTrue(self.parser.repl_conf.is_valid())

    def test_set_repl_conf_path(self):
        self.parser.parse_args(['--aos', '--repl-conf', str(self.repl_path)])
        self.assertEqual(self.repl_path, self.parser.p_man.get_repl_conf_path())

    def test_create_build_controller(self):
        self.parser.parse_args(['--aos'])
        self.assertTrue(self.parser.bc)

    def test_dump_conf_matrix(self):
        self.parser.parse_args(['--aos', '--gen-mat', '--repl-conf', str(self.repl_path)])
        self.assertTrue(self.parser.p_man.get_conf_mat().exists())

    def unset_env(self):
        del os.environ[AosEnv.AOS_ROOT.name]
        del os.environ[AosEnv.AOS_APPS_ROOT.name]

    def set_env(self):
        os.environ[AosEnv.AOS_APPS_ROOT.name] = self.apps_root
        os.environ[AosEnv.AOS_ROOT.name] = self.aos_root
