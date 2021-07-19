from test.test_suites.test_utils.path_helper import PathHelper
import unittest

from amirotest.model.aos_model import Argument, Flag
from amirotest.tools.makefile_search import MakefileSearch

class TestAosModel(unittest.TestCase):
    def test_create_arguments(self):
        arg = Argument("-WALL")
        self.assertEqual(arg.name, "-WALL")
        self.searcher = MakefileSearch()
        self.helper = PathHelper()

    def test_create_flag(self):
        name = "flag"
        wall = "-WALL"
        dtest = "-Dtest"
        arg_string = " ".join([wall, dtest])
        args = [Argument(wall), Argument(dtest)]
        flag = Flag(name, arg_string)
        self.assertEqual(flag.name, name)
        self.assertEqual(set(flag.args),set(args))

    def test_create_module(self):
