import subprocess
from amirotest.model.aos_module import AosModule

from amirotest.tools.config_path_finder import ConfigFinder
from ..test_utils.test_helper import PathHelper
from overrides.overrides import overrides
from amirotest.controller.build_executer import BuildExecutor, SerialExecutor



class SerialExecutorFake(SerialExecutor):
    """Prevents actual execution.
    Use for test purposes.
    """
    def __init__(self, finder: ConfigFinder, vis=False) -> None:
        self.helper = PathHelper()
        with self.helper.get_assets_stderr_log().open() as stderr:
            self.stderr = stderr.read().encode('utf-8')
        super().__init__(finder, vis=vis)

    @overrides
    def process_cmd(self, cmd) -> subprocess.CompletedProcess:
        # pass
        # print(self.stderr)
        return subprocess.CompletedProcess(
            ['Fake123'],
            returncode=0,
            stderr=self.stderr
        )
        # return subprocess.run(cmd, capture_output=True)

class BuildExecutorDummy(BuildExecutor):
    def __init__(self) -> None:
        # super().__init__(None, cmd_factory=None)
        pass

    @overrides
    def build(self, modules: list[AosModule]):
        pass
