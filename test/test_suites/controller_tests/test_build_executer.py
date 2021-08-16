import os
from pathlib import Path
from amirotest.controller.build_controller import BuildController
from amirotest.model.aos_module import AosModule
from amirotest.model.makefile_command_factory import SerialMakeCommandFactory
from amirotest.model.option.aos_opt import AosOption
from amirotest.tools.config_path_finder import AosModuleConfigFinder, AosPathManager
from amirotest.tools.replace_config_builder import ReplaceConfig, YamlReplConf
from ..test_utils.module_creation_helper import AosModuleHelper
import unittest

from amirotest.controller.build_executer import SerialExecutor
from amirotest.tools.aos_module_default_config_creatro import AosModuleLoader

@unittest.SkipTest
class TestExecutor(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = AosModuleHelper()
        self.finder = AosPathManager(self.helper.helper.aos_path)
        self.repl_conf = YamlReplConf(self.finder.get_repl_conf_path())
        self.bc = BuildController(self.finder, SerialExecutor)

    def test_executer_init(self):
        exe = SerialExecutor(self.finder)
        exe.build(self.get_configured_modules())

    def get_configured_modules(self) -> list[AosModule]:
        tmpl = self.bc.generate_template_modules_from_repl_conf()
        return self.bc.generate_configured_modules_from_template(tmpl[0])

proj_path = Path("/home/schorschi/hiwi/amiroci/test/test_suites/controller_tests/")

@unittest.skipIf(not proj_path.exists(), "Path not found!")
class TestMakeParameterPassing(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = AosModuleHelper()
        # TODO: Fix absolute import!
        self.finder = AosPathManager(proj_path)
        self.exe = SerialExecutor(self.finder)


    def test_pass_command_read_output(self):
        mod = AosModule(Path("test"))
        mod.add_options([
            AosOption("Para1", "true"),
            AosOption("Para2", "true"),
        ])
        cmd = self.exe.cmd_factory.build_make_command(mod)
        proc = self.exe.process_cmd(cmd)
        print(proc.stdout)
        output = proc.stdout.decode("UTF-8").split("\n")
        self.assertEqual("UDEFS=-DPara1=true -DPara2=true", output[0])
        self.assertEqual("UADEFS=-DPara1=true -DPara2=true", output[1])
        # print(proc)
