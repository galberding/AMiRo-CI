from abc import ABC, abstractmethod
from enum import Enum, auto
from amirotest.model.aos_module import AosModule
import multiprocessing


class MakeParameter(Enum):
    UDEFS = auto()
    ADEFS = auto()
    make = auto()
    BUILDDIR = auto()

class MakeCommandFactory(ABC):
    def __init__(self) -> None:
        self.cpu_count = multiprocessing.cpu_count() * 2

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
        return f'''{MakeParameter.make.name} -j{cpu_count} \\
        {MakeParameter.UDEFS.name}="{opt_str}" \\
        {MakeParameter.ADEFS.name}="{opt_str}" \\
        {module.name}'''

    def _generate_option_str(self, module):
        options = []
        for opt in module.options:
            options.append(opt.get_build_option())
        return ' '.join(options)


class SerialMakeCommandFactory(MakeCommandFactory):
    def build_make_command(self, module: AosModule) -> str:
        return self._build_command(self.cpu_count, module)


class ParallelMakeCommandFactory(MakeCommandFactory):
    def build_make_command(self, module: AosModule) -> str:
        return self._build_command(1, module)
