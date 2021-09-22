import multiprocessing
from os import cpu_count
from pathlib import Path
from unittest.case import skip
from typing import Type
import unittest

from amirotest.model.aos_module import AosModule
from amirotest.model.makefile_command_factory import MakeCommandFactory, MakeParameter, ParallelMakeCommandFactory, SerialMakeCommandFactory
from amirotest.model.option.aos_opt import AosOption, CfgOption, MakeOption
from amirotest.tools.path_manager import AosPathManager, AppsPathManager


class TestMakeCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.module_name = "DiWheelDrive_1-1"
        self.builddir = Path("/dev/shm/amiroCI")
        self.p_man = AosPathManager()
        self.make_factory = SerialMakeCommandFactory(self.p_man)

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

    @skip('Comment out for visual inspection')
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
        fac = SerialMakeCommandFactory(self.p_man)
        modules = [self.generate_module() for _ in range(module_count)]
        self.assertEqual(module_count, len(fac.build_make_commands(modules)))

    def test_apps_make_command(self):
        p_man = AppsPathManager()
        module = self.generate_module('HelloWorld/DiWheelDrive_1-1')
        final = ['make',
                 '-f',
                 f'{p_man.get_module_makefile(module.path)}',
                 f'-j{2*cpu_count()}',
                 'UDEFS=-DHELLO=true -DWORLD=false -DSTACK_SIZE=42',
                 'UADEFS=-DHELLO=true -DWORLD=false -DSTACK_SIZE=42',
                 'USE_OPT=-O2 -fdiagnostics-format=json',
                 f'BUILDDIR={p_man.b_dir.joinpath(module.uid)}',
                 module.name
                 ]
        smc = SerialMakeCommandFactory(p_man)
        cmd = smc.build_make_command(module)
        self.assertEqual(final, cmd)

    def generate_command(self, factory: Type[MakeCommandFactory] = SerialMakeCommandFactory):
        make_factory = factory(self.p_man)
        module = self.generate_module()
        self.assertTrue(module.is_resolved())
        return " ".join(make_factory.build_make_command(module))

    def generate_module(self, module_name=None) -> AosModule:
        module = AosModule(Path(module_name or self.module_name))
        options = [
            CfgOption("HELLO", "true"),
            CfgOption("WORLD", "false"),
            CfgOption("STACK_SIZE", "42"),
            MakeOption('USE_OPT', ['-O2', '-fdiagnostics-format=json']),
        ]
        module.add_options(options)
        return module
