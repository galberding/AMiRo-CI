import multiprocessing
from pathlib import Path
from ..test_utils.test_helper import PathHelper
from typing import Type
import unittest

from amirotest.model.aos_module import AosModule
from amirotest.model.makefile_command_factory import MakeCommandFactory, MakeParameter, ParallelMakeCommandFactory, SerialMakeCommandFactory
from amirotest.model.option.aos_opt import AosOption
from amirotest.tools.config_path_finder import AosPathManager


class TestMakeCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.module_name = "TestModule"
        self.builddir = Path("/dev/shm/amiroCI")
        self.finder = AosPathManager(self.path_helper.aos_path)
        self.make_factory = SerialMakeCommandFactory(self.finder)

    def test_make_command_make_at_first_place(self):
        command = self.generate_command()
        self.assertEqual(0, command.find(MakeParameter.make.name))

    def test_UDEFS_set(self):
        command = self.generate_command()
        self.assertRegex(command, rf'{MakeParameter.UDEFS.name}=(?P<paras>.*)')

    def test_UADEFS_set(self):
        command = self.generate_command()
        self.assertRegex(command, rf'{MakeParameter.UADEFS.name}=(?P<paras>.*)')

    def test_contains_module_name(self):
        command = self.generate_command()
        self.assertRegex(command, rf'{self.module_name}')

    def test_serial_cpu_count(self):
        command = self.generate_command()
        cpus = multiprocessing.cpu_count() * 2
        self.assertRegex(command, f"-j{cpus}")

    def test_parallel_cpu_count(self):
        command = self.generate_command(factory=ParallelMakeCommandFactory)
        cpus = 1
        self.assertRegex(command, f"-j{cpus}")

    def test_contains_build_dir(self):
        command = self.generate_command()
        self.assertRegex(command, rf'{MakeParameter.BUILDDIR.name}={self.builddir}.*')

    @unittest.SkipTest
    def test_visual_command_inspection(self):
        command = self.generate_command()
        print()
        print("Serial Command")
        print(command)
        command = self.generate_command(factory=ParallelMakeCommandFactory)
        print()
        print("Parallel Command")
        print(command)
        print()

    def test_build_commands(self):
        module_count = 5
        fac = SerialMakeCommandFactory(self.finder)
        modules = [self.generate_module() for _ in range(module_count)]
        self.assertEqual(module_count, len(fac.build_make_commands(modules)))

    def generate_command(self, factory: Type[MakeCommandFactory] = SerialMakeCommandFactory):
        make_factory = factory(self.finder)
        module = self.generate_module()
        self.assertTrue(module.is_resolved())
        return " ".join(make_factory.build_make_command(module))

    def generate_module(self) -> AosModule:
        module = AosModule(Path(self.module_name))
        options = [
            AosOption("HELLO", "true"),
            AosOption("WORLD", "false"),
            AosOption("STACK_SIZE", "42"),
        ]
        module.add_options(options)
        return module
