"""Convert modules to commands and execute them.
There are two strategies:
- Serial
- Parallel
The default is serial where one module is build at a time with -j and the amount of
available cpu cores.
"""
from abc import ABC, abstractmethod
from overrides import overrides
from pathlib import Path
from typing import Type
import subprocess
from amirotest.model.aos_module import AosModule, BuildInfo
from amirotest.model.makefile_command_factory import MakeCommandFactory, ParallelMakeCommandFactory, SerialMakeCommandFactory
from multiprocessing import Pool, cpu_count
import tqdm
from timeit import default_timer as timer

from amirotest.tools.config_path_finder import ConfigFinder


class BuildExecutor(ABC):
    """!Interface for executing the build process.
    """
    def __init__(self, finder: ConfigFinder, cmd_factory: Type[MakeCommandFactory]=SerialMakeCommandFactory) -> None:
        self.finder = finder
        self.cmd_factory = cmd_factory(self.finder)

    @abstractmethod
    def build(self, modules: list[AosModule], vis=False):
        """!Build modules.
        """

    def process_cmd(self, cmd) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True)

    def _build_module(self, module: AosModule):
        """!Convert module to command and execute it.
        The build information is passed to the module together with
        the build duration.
        """
        cmd = self.cmd_factory.build_make_command(module)
        start = timer()
        comp_proc = self.process_cmd(cmd)
        end = timer()
        bi = BuildInfo(comp_proc, end - start)
        module.build_info = bi


class SerialExecutor(BuildExecutor):
    """!Serial build.
    One module is build at a time with several cpus.
    """
    def __init__(self, finder: ConfigFinder) -> None:
        super().__init__(finder, SerialMakeCommandFactory)

    @overrides
    def build(self, modules: list[AosModule], vis=False):
        for module in tqdm.tqdm(modules) if vis else modules:
            self._build_module(module)

class SerialExecutorFake(SerialExecutor):
    """Prevents actual execution.
    Use for test purposes.
    """
    @overrides
    def process_cmd(self, cmd) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(['Fake'], returncode=0)
        # return subprocess.run(cmd, capture_output=True)



class ParallelExecutor(BuildExecutor):
    def __init__(self, finder: ConfigFinder) -> None:
        super().__init__(finder, ParallelMakeCommandFactory)

    @overrides
    def build(self, modules: list[AosModule], vis=False):
        with Pool(cpu_count()*2) as p:
            # for conf, duration in tqdm.tqdm(
                    # p.imap_unordered(execute, confs), total=len(confs)
            # ):
            # print(getConfigString(conf), "--", duration)
            raise NotImplementedError()
