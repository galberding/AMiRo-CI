from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path

from overrides.overrides import overrides
from amirotest.model.aos_module import AosModule
import multiprocessing
from amirotest.model.option.aos_opt import CfgOption, MakeOption

from amirotest.tools.path_manager import PathManager


class MakeParameter(Enum):
    """!Dataholder used for make command creation.
    By issuing:
    \code{.py}
    MakeParameter.BUILDDIR.name # -> BUILDDIR
    # or
    MakeParameter.BUILDDIR.value # -> "/dev/shm/amiroCI"
    \endcode
    the single parts of the make command can be assembled.
    """
    UDEFS = auto()
    UADEFS = auto()
    make = auto()
    BUILDDIR = auto()


class MakeCommandFactory(ABC):
    """! Abstract class to create make commands.
    A basic structure is provided by _build_command() which can be
    adapted by overriding the build_make_command().
    For examples have a look at:
    - SerialMakeCommandFactory
    - ParallelMakeCommandFactory


    """
    def __init__(self, p_man: PathManager) -> None:
        self.p_man = p_man
        self.make_dir = p_man.get_project_makefile()
        self.b_dir = p_man.get_build_dir()

    def build_make_commands(self, modules: list[AosModule]) -> list[list[str]]:
        """!Build make command for all modules.
        @param modules: list of AosModules
        @return list of strings aka. make commands
        """
        make_cmd = []
        for module in modules:
            make_cmd.append(self.build_make_command(module))
        return make_cmd

    @abstractmethod
    def build_make_command(self, module: AosModule) -> list[str]:
        """!Generate make command.
        The command is generated after a fixed pattern, defined in _build_command_list().
        @param module: Resolved \b AosModule
        @return list of strings where each entry in the list corresponds to one part of the make command.
        """

    def _build_command_list(self, cpu_count, module: AosModule) -> list[str]:
        make_command = []
        make_command += self._cmd_add_make_command(module)
        make_command += self._cmd_add_cpu_count(cpu_count)
        make_command += self._cmd_add_cfg_options(module)
        make_command += self._cmd_add_make_optios(module)
        make_command += self._cmd_add_builddir(module)
        make_command += self._cmd_add_module_name(module)
        return make_command

    def _cmd_add_make_command(self, module: AosModule) -> list[str]:
        """!Create the make command pointing to the correct Makefile.
        """
        return [
            f'{MakeParameter.make.name}',
            '-f',
            f'{self.p_man.get_module_makefile(module.path)}',
        ]

    def _cmd_add_cpu_count(self, cpu_count: int) -> list[str]:
        return [f'-j{cpu_count}']

    def _cmd_add_cfg_options(self, module: AosModule) -> list[str]:
        opt_str = self._generate_cfg_option_str(module)
        return [
            f'{MakeParameter.UDEFS.name}={opt_str}',
            f'{MakeParameter.UADEFS.name}={opt_str}',
        ]

    def _generate_cfg_option_str(self, module: AosModule):
        """!Convert AosOption to string.
        Each AosOption provides a get_build_option() which creates the
        desired format for the make command:
        \code{.unparsed}
        -DOPTION_NAME=VALUE
        \endcode
        """
        options = []
        for opt in module.options:
            if isinstance(opt, CfgOption):
                options.append(opt.get_build_option())
        return ' '.join(options)

    def _cmd_add_make_optios(self, module: AosModule) -> list[str]:
        opts = []
        for opt in module.options:
            if isinstance(opt, MakeOption):
                opts.append(opt.get_build_option())
        return opts

    def _cmd_add_builddir(self, module: AosModule) -> list[str]:
        module_build_dir = self.p_man.get_build_dir().joinpath(module.uid)
        return [f'{MakeParameter.BUILDDIR.name}={module_build_dir}']

    def _cmd_add_module_name(self, module: AosModule) -> list[str]:
        return [module.name]


class SerialMakeCommandFactory(MakeCommandFactory):
    """!Generates commands similar to:
    \code{.unparsed}
    make -j8 \
        UDEFS="-DHELLO=true -DWORLD=false -DSTACK_SIZE=42" \
        UADEFS="-DHELLO=true -DWORLD=false -DSTACK_SIZE=42" \
        BUILDDIR="/dev/sha/amiroCI/cd946b53-f9d4-11eb-8745-80fa5b33770d" \
        TestModule
    \endcode
    """
    @overrides
    def build_make_command(self, module: AosModule) -> list[str]:
        cpu_count = multiprocessing.cpu_count() * 2
        return self._build_command_list(cpu_count, module)


class ParallelMakeCommandFactory(MakeCommandFactory):
    """!Generates commands similar to:
    \code{.unparsed}
    make -j1 \
        UDEFS="-DHELLO=true -DWORLD=false -DSTACK_SIZE=42" \
        UADEFS="-DHELLO=true -DWORLD=false -DSTACK_SIZE=42" \
        BUILDDIR="/dev/sha/amiroCI/cd946b53-f9d4-11eb-8745-80fa5b33770d" \
        TestModule
    \endcode
    """
    @overrides
    def build_make_command(self, module: AosModule) -> list[str]:
        return self._build_command_list(2, module)
