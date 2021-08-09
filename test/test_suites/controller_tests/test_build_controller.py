import unittest

from amirotest.controller.build_controller import BuildController

class TestBuildController(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {"Module": ["Name1", "Name2"],
                       "Config":{
                       "Aosconf":{
                           "Opt1": [1,2],
                           "Opt2": [1,2]},
                       "AnotherConf":{
                           "OS_OPT": ["true", "false"],
                           "OS_SHELL": ["on", "off"]}}}
    def test_build_generate_conf_matrix(self):
        bc = BuildController()
        bc.generateConfigMatrix()
