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

    @abstractmethod
    def build_make_command(self, module: AosModule) -> str:
        """Generate make command.
        """

    def _build_command(self, cpu_count, module: AosModule):
        """Build the actual make command.
        cpu_count: parameter which is set for -j<cpu_count>
        module: resolved \a AosModule
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
    def build_make_command(self, module: AosModule) -> str:
        cpu_count = multiprocessing.cpu_count() * 2
        return self._build_command(cpu_count, module)


class ParallelMakeCommandFactory(MakeCommandFactory):
    def build_make_command(self, module: AosModule) -> str:
        return self._build_command(1, module)
