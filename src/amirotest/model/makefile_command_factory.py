from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path
from amirotest.model.aos_module import AosModule
import multiprocessing

from amirotest.tools.config_path_finder import ConfigFinder


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
    # TODO: Ugly should be set by ConfigFinder module or something else
    BUILDDIR = auto()

class MakeCommandFactory(ABC):
    """! Abstract class to create make commands.
    A basic structure is provided by _build_command() which can be
    adapted by overriding the build_make_command().
    For examples have a look at:
    - SerialMakeCommandFactory
    - ParallelMakeCommandFactory


    """
    def __init__(self, finder: ConfigFinder) -> None:
        self.finder = finder
        self.make_dir = finder.get_project_makefile()
        self.b_dir = finder.get_build_dir()

    def build_make_commands(self, modules: list[AosModule]) -> list[str]:
        """!Build make command for all modules.
        @param modules: list of AosModules
        @return list of strings aka. make commands
        """
        make_cmd = []
        for module in modules:
            make_cmd.append(self.build_make_command(module))
        return make_cmd

    @abstractmethod
    def build_make_command(self, module: AosModule) -> str:
        """!Generate make command.
        @param module: Resolved \b AosModule
        """


    def _build_command(self, cpu_count, module: AosModule):
        """!Build the actual make command.
        @param cpu_count: Parameter for \b -j<cpu_count>
        @param module: Resolved \b AosModule
        """
        opt_str = self._generate_option_str(module)
        module_build_dir = self.b_dir.joinpath(module.uid)
        return f'''{self._generate_make_f_makefile_path()} -j{cpu_count} \\
        {MakeParameter.UDEFS.name}="{opt_str}" \\
        {MakeParameter.UADEFS.name}="{opt_str}" \\
        {MakeParameter.BUILDDIR.name}="{module_build_dir}" \\
        {module.name}'''


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

    def _generate_make_f_makefile_path(self) -> str:
        """!Generate command of the form:
        \code{.unparsed}
        make -f /path/to/Makefile
        \endcode
        """
        return f'{MakeParameter.make.name} -f {self.make_dir}'



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
    def build_make_command(self, module: AosModule) -> str:
        cpu_count = multiprocessing.cpu_count() * 2
        return self._build_command(cpu_count, module)


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
    def build_make_command(self, module: AosModule) -> str:
        return self._build_command(1, module)
