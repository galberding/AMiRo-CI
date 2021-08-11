"""Convert modules to commands and execute them.
There are two strategies:
- Serial
- Parallel
The default is serial where one module is build at a time with -j
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from amirotest.model.aos_module import AosModule
from amirotest.model.makefile_command_factory import MakeCommandFactory, ParallelMakeCommandFactory, SerialMakeCommandFactory
from multiprocessing import Pool, cpu_count
import tqdm

from amirotest.tools.config_path_finder import ConfigFinder

class BuildExecutor(ABC):
    """!Interface for executing the build process.
    """
    def __init__(self, finder: ConfigFinder, cmd_factory: Type[MakeCommandFactory]=SerialMakeCommandFactory) -> None:
        self.finder = finder
        self.cmd_factory = cmd_factory(self.finder)

    @abstractmethod
    def build(self, modules: list[AosModule]):
        """!Build modules.
        """

    def process_cmds(self, cmds: list[str]):
        pass


    def issue_shell_command(self, cmd):
        pass

class SerialExecutor(BuildExecutor):
    """!Serial build.
    One module is build at a time with several cpus.
    """
    def __init__(self, finder: ConfigFinder) -> None:
        super().__init__(finder, SerialMakeCommandFactory)

    def build(self, modules: list[AosModule]):
        configs = self.cmd_factory.build_make_commands(modules)
        for config in tqdm.tqdm(configs):
            pass


class ParallelExecutor(BuildExecutor):
    def __init__(self, finder: ConfigFinder) -> None:
        super().__init__(finder, ParallelMakeCommandFactory)

    def build(self, modules: list[AosModule]):
        with Pool(cpu_count()*2) as p:
            for conf, duration in tqdm.tqdm(
                    p.imap_unordered(execute, confs), total=len(confs)
            ):
            # print(getConfigString(conf), "--", duration)
                pass
