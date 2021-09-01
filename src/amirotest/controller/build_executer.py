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
import shutil
from typing import Type
import subprocess
from amirotest.controller.build_reporter import BuildReporter
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
        self.reporter = BuildReporter(self.finder)

    @abstractmethod
    def build(self, modules: list[AosModule]):
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
        self.cleanup(self.finder.get_build_dir().joinpath(module.uid))
        bi.dump(self.finder.get_build_dir().joinpath(f'{module.uid}.log'))
        module.build_info = bi
        return module

    def cleanup(self, buildir: Path):
        if buildir.exists():
            shutil.rmtree(buildir)


class SerialExecutor(BuildExecutor):
    """!Serial build.
    One module is build at a time with several cpus.
    """
    def __init__(self, finder: ConfigFinder, vis=False) -> None:
        self.vis = vis
        super().__init__(finder, SerialMakeCommandFactory)

    @overrides
    def build(self, modules: list[AosModule]):
        for module in tqdm.tqdm(modules) if self.vis else modules:
            self._build_module(module)
            self.reporter.record_module(module)


class ParallelExecutor(BuildExecutor):
    def __init__(self, finder: ConfigFinder) -> None:
        super().__init__(finder, ParallelMakeCommandFactory)

    @overrides
    def build(self, modules: list[AosModule]):
        with Pool(cpu_count()*2) as p:
            for module in tqdm.tqdm(p.imap_unordered(self._build_module, modules), total=len(modules)):
                self.reporter.record_module(module)
