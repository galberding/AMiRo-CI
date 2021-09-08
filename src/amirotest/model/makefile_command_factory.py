from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path

from overrides.overrides import overrides
from amirotest.model.aos_module import AosModule
import multiprocessing

from amirotest.tools.config_path_finder import PathManager


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
        opt_str = self._generate_option_str(module)
        module_build_dir = self.b_dir.joinpath(module.uid)
        return [
            f'{MakeParameter.make.name}',
            '-f',
            f'{self.p_man.get_module_makefile(module.path)}',
            f'-j{cpu_count}',
            f'{MakeParameter.UDEFS.name}={opt_str}',
            f'{MakeParameter.UADEFS.name}={opt_str}',
            'USE_OPT=-O2 -fstack-usage -Wl,--print-memory-usage -fdiagnostics-format=json',
            f'{MakeParameter.BUILDDIR.name}={module_build_dir}',
            f'{module.name}'
            ]


    def _generate_option_str(self, module):
        """!Convert AosOption to string.
        Each AosOption provides a get_build_option() which creates the
        desired format for the make command:
        \code{.unparsed}
        -DOPTION_NAME=VALUE
        \endcode
        """
        options = []
        for opt in module.options:
            options.append(opt.get_build_option())
        return ' '.join(options)


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
        return self._build_command_list(1, module)
