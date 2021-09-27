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
from typing import Iterator, Type
import subprocess
from amirotest.controller.build_reporter import BuildReporter
from amirotest.model.aos_module import AosModule, BuildInfo
from amirotest.model.makefile_command_factory import MakeCommandFactory, ParallelMakeCommandFactory, SerialMakeCommandFactory
from multiprocessing import Pool, cpu_count
import tqdm
from timeit import default_timer as timer
from time import perf_counter as ptimer
from amirotest.tools.path_manager import PathManager


class BuildExecutor(ABC):
    """!Interface for executing the build process.
    """
    def __init__(self, p_man: PathManager, cmd_factory: Type[MakeCommandFactory]=SerialMakeCommandFactory) -> None:
        self.p_man = p_man
        self.cmd_factory = cmd_factory(self.p_man)
        self.reporter = BuildReporter(self.p_man)

    @abstractmethod
    def build(self, modules: Iterator[AosModule]):
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
        cpu_time_start = ptimer()
        comp_proc = self.process_cmd(cmd)
        cpu_time_end = ptimer()
        end = timer()
        bi = BuildInfo(comp_proc, end - start, cpu_time_end - cpu_time_start)
        self.cleanup(self.p_man.get_build_dir().joinpath(module.uid))
        module.build_info = bi
        return module

    def cleanup(self, buildir: Path):
        if buildir.exists():
            shutil.rmtree(buildir)


class SerialExecutor(BuildExecutor):
    """!Serial build.
    One module is build at a time with several cpus.
    """
    def __init__(self, p_man: PathManager, vis=False) -> None:
        self.vis = vis
        super().__init__(p_man, SerialMakeCommandFactory)

    @overrides
    def build(self, modules: Iterator[AosModule]):
        for module in tqdm.tqdm(modules) if self.vis else modules:
            self._build_module(module)
            self.reporter.record_module(module)
        self.reporter.record_save()


class ParallelExecutor(BuildExecutor):
    def __init__(self, p_man: PathManager, save_report_every=100 ) -> None:
        self.save_report_every = save_report_every
        super().__init__(p_man, ParallelMakeCommandFactory)

    @overrides
    def build(self, modules: Iterator[AosModule]):
        build_count = 0
        with Pool(cpu_count()*4) as p:
            for module in tqdm.tqdm(p.imap_unordered(self._build_module, modules), total=len(modules)):
                build_count += 1
                if build_count % self.save_report_every:
                    self.reporter.record_module(module)

            self.reporter.record_save()
