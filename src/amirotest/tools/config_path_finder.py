from abc import ABC, abstractmethod
import os
from pathlib import Path
from enum import Enum, auto
from overrides.overrides import overrides


class AosEnv(Enum):
    AOS_ROOT = auto()
    AOS_APPS_ROOT = auto()
    AOS_REPLACE_CONF = auto()


class CannotFindConfigError(Exception):
    def __init__(self, config: Path) -> None:
        msg = f"Cannot find config at: {config}!"
        super().__init__(msg)


class CannotFindRootDirectoryError(Exception):
    pass


class CannotFindProjectRoot(Exception):
    pass


class PathManager(ABC):
    def __init__(self, root: Path,
                 builddir=Path("/dev/shm/amiroCI")) -> None:
        self.root = root
        self.b_dir: Path = builddir
        self.b_dir.mkdir(exist_ok=True)
        if not self.root.exists():
            raise CannotFindProjectRoot(f"Cannot find module at: {self.root}")

    @abstractmethod
    def get_project_makefile(self) -> Path:
        pass

    @abstractmethod
    def get_repl_conf_path(self) -> Path:
        """!Return path to replacement config
        """
        # TODO: Point to correct path!
        # return Path("/home/schorschi/hiwi/amiroci/assets/repl_conf.yml")

    def get_build_dir(self) -> Path:
        return self.b_dir

    def _ensure_config_exists(self, config: Path):
        if not config.exists():
            raise CannotFindConfigError(config)

    def get_report_config(self):
        pass

class AosPathManager(PathManager):
    def __init__(self,
                 aos_root: Path = None,
                 config_root=Path('../assets/').resolve()) -> None:
        self.aos_root: Path = aos_root or Path(os.environ[AosEnv.AOS_ROOT.name])
        self.modules = self.aos_root.joinpath("modules")
        self.config_root = config_root

        if not self.aos_root.exists():
            raise CannotFindProjectRoot(f"AmiroOS not at location: {self.aos_root}")
        super().__init__(self.aos_root)


    def _get_module_path(self, module_name: str, file: str) -> Path:
        return self.modules.joinpath(module_name).joinpath(file)

    @overrides
    def get_project_makefile(self) -> Path:
        return self.aos_root.joinpath("Makefile")

    @overrides
    def get_repl_conf_path(self) -> Path:
        return self.config_root.joinpath('repl_conf.yml')

    @overrides
    def get_report_config(self):
        return self.config_root.joinpath('report.tsv')

# class AppsConfigFinder(ConfigFinder):
#     def __init__(self, module_path: Path) -> None:
#         super().__init__(module_path)
