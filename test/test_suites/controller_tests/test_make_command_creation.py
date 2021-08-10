import multiprocessing
from pathlib import Path
from typing import Type
import unittest

from amirotest.model.aos_module import AosModule
from amirotest.model.makefile_command_factory import MakeCommandFactory, MakeParameter, ParallelMakeCommandFactory, SerialMakeCommandFactory
from amirotest.model.option.aos_opt import AosOption


class TestMakeCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.module_name = "TestModule"
        self.make_factory = SerialMakeCommandFactory()


    def test_make_command_make_at_first_place(self):
        command = self.generate_command()
        self.assertEqual(0, command.find(MakeParameter.make.name))

    def test_UDEFS_set(self):
        command = self.generate_command()
        self.assertRegex(command, rf'{MakeParameter.UDEFS.name}="(?P<paras>.*)"')

    def test_ADEFS_set(self):
        command = self.generate_command()
        self.assertRegex(command, rf'{MakeParameter.ADEFS.name}="(?P<paras>.*)"')

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
        self.assertRegex(command, rf'{MakeParameter.ADEFS.name}="(?P<paras>.*)"')


    # UDEFS and ADEFS needs to be set and equal
    # BUILDDIR needst to be set
    # Target / Module name at the end

    def generate_command(self, factory: Type[MakeCommandFactory] = SerialMakeCommandFactory):
        make_factory = factory()
        module = AosModule(Path(self.module_name))
        options = [
            AosOption("HELLO", "true"),
            AosOption("WORLD", "false"),
            AosOption("STACK_SIZE", "42"),
        ]
        module.add_options(options)
        self.assertTrue(module.is_resolved())
        return make_factory.build_make_command(module)
