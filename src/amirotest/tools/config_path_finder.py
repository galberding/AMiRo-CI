from abc import ABC, abstractmethod
import os
from pathlib import Path
from enum import Enum, auto
from typing import Optional
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

class CannotFindMakefile(Exception):
    def __init__(self, makepath: Path) -> None:
        super().__init__(f'Makefile not found at: {makepath}')


class PathManager(ABC):
    def __init__(self, root: Path,
                 config_root: Optional[Path] = Path('../assets/').resolve(),
                 builddir=Path("/dev/shm/amiroCI")) -> None:
        self.root = root
        self.b_dir: Path = builddir
        self.b_dir.mkdir(exist_ok=True)
        self.config_root = config_root
        if not self.root.exists():
            raise CannotFindProjectRoot(f"Cannot find module at: {self.root}")

    def get_project_makefile(self) -> Path:
        return  self.root.joinpath("Makefile")

    @abstractmethod
    def get_module_makefile(self, module_name: Path) -> Path:
        """!Construct path to Makefile where the target is included.
        """

    def get_repl_conf_path(self) -> Path:
        """!Return path to replacement config
        """
        return self.config_root.joinpath('repl_conf.yml')

    def get_build_dir(self) -> Path:
        return self.b_dir

    def _ensure_config_exists(self, config: Path):
        if not config.exists():
            raise CannotFindConfigError(config)

    def get_report_config(self) -> Path:
         return self.config_root.joinpath('report.tsv')


class AosPathManager(PathManager):
    def __init__(self,
                 root: Path = None) -> None:
        aos_root: Path = root or Path(os.environ[AosEnv.AOS_ROOT.name])
        super().__init__(aos_root)

    @overrides
    def get_module_makefile(self, module_name: Path) -> Path:
        makepath = self.root.joinpath('modules').joinpath(module_name).joinpath('Makefile')
        if not makepath.exists():
            raise CannotFindMakefile(makepath)
        return makepath


class AppsPathManager(PathManager):
    def __init__(self, root: Path = None) -> None:
        apps_root: Path = root or Path(os.environ[AosEnv.AOS_APPS_ROOT.name])
        super().__init__(apps_root)

    @overrides
    def get_module_makefile(self, module_name: Path) -> Path:
        path_content = module_name.parts
        name = path_content[-1]
        app = path_content[0]
        makepath = self.root.joinpath('configurations')\
                                .joinpath(app)\
                                .joinpath('modules')\
                                .joinpath(name)\
                                .joinpath('Makefile')
        if not makepath.exists():
            raise CannotFindMakefile(makepath)
        return makepath
