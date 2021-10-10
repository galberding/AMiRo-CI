import subprocess
from typing import Iterator
from overrides.overrides import overrides

from amiroci.model.aos_module import AosModule
from amiroci.tools.path_manager import PathManager
from amiroci.controller.build_executer import BuildExecutor, SerialExecutor


class SerialExecutorFake(SerialExecutor):
    """Prevents actual execution.
    Use for test purposes.
    """
    def __init__(self, p_man: PathManager, vis=False) -> None:
        self.executions = 0
        self.stderr = """
...
[]
[]
[{"kind": "note","message": "info"}]
[{"kind": "warning","message": "warning"}]
[{"kind": "error", "message": "unknown type name 'SerialCANDriver'"}, {"kind": "error", "message": "unknown type name 'SerialCANConfig'"}, {"kind": "error", "message": "unknown type name 'aos_fbcan_filter_t'"}]
make[1]: *** [clutter ... ] Error 1
make: *** [other stuff] Error 2
        """.encode('utf-8')
        super().__init__(p_man, vis=vis)

    @overrides
    def process_cmd(self, cmd) -> subprocess.CompletedProcess:
        self.executions += 1
        return subprocess.CompletedProcess(
            ['Fake123'], returncode=0, stderr=self.stderr
        )


class BuildExecutorDummy(BuildExecutor):
    def __init__(self) -> None:
        # super().__init__(None, cmd_factory=None)
        pass

    @overrides
    def build(self, modules: Iterator[AosModule]):
        pass
