from argparse import Namespace
import logging
import os
from pathlib import Path
from shutil import copyfile, rmtree
from time import time
from unittest.case import skip

from amiroci.tools.aos_logger import get_logger
from ..test_utils.build_executer_fake import SerialExecutorFake
import unittest
from unittest.mock import patch
from io import StringIO
from amiroci.tools.cli_parser import AmiroParser
from amiroci.tools.path_manager import AosEnv, AosPathManager, AppsPathManager, NoAosEnvVariableError
import pandas as pd
import time


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = AmiroParser(executor=SerialExecutorFake)
        self.parser.log = get_logger("Dummy", logging.WARN)
        self.aos_root = os.environ[AosEnv.AOS_ROOT.name]
        self.apps_root = os.environ[AosEnv.AOS_APPS_ROOT.name]
        self.aos_repl_root = os.environ[AosEnv.AOS_REPLACE_CONF.name]
        self.tmp_dir = Path('/dev/shm/amiroCI')
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        repl_path = Path(os.environ[AosEnv.AOS_REPLACE_CONF.name])
        self.repl_path = self.tmp_dir.joinpath(repl_path.name)
        copyfile(repl_path, self.repl_path)

    def tearDown(self) -> None:
        rmtree(self.tmp_dir)
        self.set_env()

    @skip('Visualize help command')
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
        with patch('sys.stderr', new=StringIO()):
            self.assertRaises(
                SystemExit, self.parser.parse_args, ['--apps', '--aos']
            )
            # print(fake_out)

    def test_no_arg_provided(self):
        with patch('sys.stderr', new=StringIO()):
            self.assertRaises(SystemExit, self.parser.parse_args, [])

    def test_aos_pman_is_selected(self):
        self.parser.parse_args(['--aos'])
        self.assertTrue(isinstance(self.parser.p_man, AosPathManager))

    def test_apps_pman_is_selected(self):
        self.parser.parse_args(['--apps'])
        self.assertTrue(isinstance(self.parser.p_man, AppsPathManager))

    def test_pass_path(self):
        self.unset_env()
        self.parser.parse_args(['--aos', '--project-root', self.aos_root])
        self.assertEqual(Path(self.aos_root), self.parser.p_man.root)

        self.parser.parse_args(['--apps', '--project-root', self.apps_root])
        self.assertEqual(Path(self.apps_root), self.parser.p_man.root)

    def test_pass_path_to_path_manager(self):
        self.unset_env()
        self.assertRaises(
            NoAosEnvVariableError, self.parser.parse_args, ['--apps']
        )
        self.assertRaises(
            NoAosEnvVariableError, self.parser.parse_args, ['--aos']
        )

    def test_load_replacement_config(self):
        self.parser.parse_args(['--aos'])
        self.assertTrue(self.parser.repl_conf.is_valid())

    def test_set_repl_conf_path(self):
        self.parser.parse_args(['--aos', '--repl-conf', str(self.repl_path)])
        self.assertEqual(self.repl_path, self.parser.p_man.get_repl_conf_path())

    def test_create_build_controller(self):
        self.parser.parse_args(['--aos'])
        self.assertTrue(self.parser.bc)

    def test_always_dump_conf_matrix(self):
        self.parser.parse_args(['--aos', '--repl-conf', str(self.repl_path)])
        self.assertTrue(self.parser.p_man.get_conf_mat_path().exists())

    def test_dump_conf_matrix_different_name(self):
        mat_name = 'testmat.tsv'
        self.parser.parse_args(
            [
                '--aos', '--mat-name', mat_name, '--repl-conf',
                str(self.repl_path)
            ]
        )
        self.assertTrue(self.parser.p_man.get_conf_mat_path(mat_name).exists())

    @skip('take too long')
    def test_provide_alternative_matrix(self):
        os.environ[AosEnv.AOS_REPLACE_CONF.name] = str(self.repl_path)
        mat_name = self.create_matrix()
        self.parser.parse_args(['--aos', '--use-mat', mat_name])
        self.assertIsNotNone(self.parser.bc.conf_matrix)
        print(self.parser.bc.conf_matrix.shape)
        start = time.time()
        self.parser.bc.c_modules
        print('Elapsed time:', time.time() - start)

    def create_matrix(self) -> str:
        """!Use a new parser to create a conf martix in self.tmp_dir.
        return the name of that matrix (testmat.tsv)
        """
        parser = AmiroParser()
        mat_name = 'testmat.tsv'
        parser.parse_args(
            [
                '--aos', '--mat-name', mat_name, '--repl-conf',
                str(self.repl_path)
            ]
        )
        return mat_name

    def test_execute_none_if_not_used(self):
        self.parser.parse_args(['--aos'])
        self.assertIsInstance(self.parser.executor, SerialExecutorFake)

    @skip('Take time for module generation')
    def test_execute(self):
        self.parser.parse_args(['--aos', '-e'])
        self.assertGreater(self.parser.executor.executions, 0)  # type: ignore

    def unset_env(self):
        del os.environ[AosEnv.AOS_ROOT.name]
        del os.environ[AosEnv.AOS_APPS_ROOT.name]
        # del os.environ[AosEnv.AOS_REPLACE_CONF.name]

    def set_env(self):
        os.environ[AosEnv.AOS_APPS_ROOT.name] = self.apps_root
        os.environ[AosEnv.AOS_ROOT.name] = self.aos_root
        os.environ[AosEnv.AOS_REPLACE_CONF.name] = self.aos_repl_root
