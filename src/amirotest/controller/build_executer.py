"""Convert modules to commands and execute them.
There are two strategies:
- Serial
- Parallel
The default is serial where one module is build at a time with -j
"""
from abc import ABC, abstractmethod
from pathlib import Path

from amirotest.model.aos_module import AosModule
from amirotest.model.makefile_command_factory import MakeCommandFactory, ParallelMakeCommandFactory, SerialMakeCommandFactory
from multiprocessing import Pool, cpu_count
import tqdm

class BuildExecutor(ABC):
    """!Interface for executing the build process.
    """
    def __init__(self, builddir: Path, cmd_factory: MakeCommandFactory) -> None:
        self.b_dir = builddir
        self.cmd_factory = cmd_factory

    @abstractmethod
    def build(self, modules: list[AosModule]):
        """!Build modules.
        """



class SerialExecutor(BuildExecutor):
    """!Serial build.
    One module is build at a time with several cpus.
    """
    def __init__(self, builddir: Path) -> None:
        cmd_factory = SerialMakeCommandFactory()
        super().__init__(builddir, cmd_factory)

    def build(self, modules: list[AosModule]):
        pass

    def executeConfigs(confs):
        with Pool(CPU_CORES) as p:
            for conf, duration in tqdm.tqdm(
                    p.imap_unordered(execute, confs), total=len(confs)
            ):
            # print(getConfigString(conf), "--", duration)
                pass




class ParallelExecutor(BuildExecutor):
    def __init__(self, builddir: Path) -> None:
        cmd_factory = ParallelMakeCommandFactory()
        super().__init__(builddir, cmd_factory)

    def build(self, modules: list[AosModule]):
        pass
