"""Convert modules to commands and execute them.
There are two strategies:
- Serial
- Parallel
The default is serial where one module is build at a time with -j
"""
from abc import ABC, abstractmethod
from pathlib import Path

from amirotest.model.aos_module import AosModule


class BuildExecutor(ABC):
    """!Interface for executing the build process.
    """
    def __init__(self, builddir: Path) -> None:
        self.b_dir = builddir

    @abstractmethod
    def build(self, modules: list[AosModule]):
        """!Build modules.
        """

class SerialExecutor(BuildExecutor):
    """!Serial build.
    One module is build at a time with several cpus.
    """
    def build(self, modules: list[AosModule]):
        pass

class ParallelExecutor(BuildExecutor):
    def build(self, modules: list[AosModule]):
        pass
