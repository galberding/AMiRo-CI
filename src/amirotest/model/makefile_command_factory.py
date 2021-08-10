from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path
from amirotest.model.aos_module import AosModule
import multiprocessing


class MakeParameter(Enum):
    UDEFS = auto()
    UADEFS = auto()
    make = auto()
    # TODO: Ugly should be set by ConfigFinder module or something else
    BUILDDIR = Path("/dev/shm/amiroCI")

class MakeCommandFactory(ABC):
    """! Abstract class to create make commands.
    A basic structure is provided by _build_command() which can be
    adapted by overriding the build_make_command().
    For examples have a look at:
    - SerialMakeCommandFactory
    - ParallelMakeCommandFactory


    """
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
        module_build_dir = MakeParameter.BUILDDIR.value.joinpath(module.uid)
        return f'''{MakeParameter.make.name} -j{cpu_count} \\
        {MakeParameter.UDEFS.name}="{opt_str}" \\
        {MakeParameter.UADEFS.name}="{opt_str}" \\
        {MakeParameter.BUILDDIR.name}="{module_build_dir}" \\
        {module.name}'''

    def _generate_option_str(self, module):
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
