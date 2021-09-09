from abc import ABC, abstractmethod
import os
from pathlib import Path
from enum import Enum, auto
from typing import Optional
from overrides.overrides import overrides


class AosEnv(Enum):
    AOS_ROOT = 'Amiro-OS'
    AOS_APPS_ROOT = 'Amiro-Apps'
    AOS_REPLACE_CONF = 'Replacement Config'


class NoAosEnvVariableError(Exception):
    def __init__(self, param: AosEnv, option: str = '--project-root') -> None:
        super().__init__(f'''
        Please provide a project root with:
        \t{option} path/to/{param.value}
        or set an environment variable with:
        \texport {param.name}=path/to/{param.value}
        ''')

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
        try:
            self.config_root = config_root or os.environ[AosEnv.AOS_REPLACE_CONF.name]
        except:
            raise NoAosEnvVariableError(AosEnv.AOS_REPLACE_CONF, option='--repl-conf')
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
        if AosEnv.AOS_REPLACE_CONF.name in os.environ:
            repl = self.get_env_path(AosEnv.AOS_REPLACE_CONF)
            if repl and repl.exists():
                return repl
        return self.config_root.joinpath('repl_conf.yml')

    def get_build_dir(self) -> Path:
        return self.b_dir

    def _ensure_config_exists(self, config: Path):
        if not config.exists():
            raise CannotFindConfigError(config)

    def get_report_config(self) -> Path:
         return self.config_root.joinpath('report.tsv')

    def get_env_path(self, param: AosEnv) -> Optional[Path]:
        if param.name in os.environ:
            return Path(os.environ[param.name])



class AosPathManager(PathManager):
    def __init__(self,
                 root: Path = None) -> None:
        try:
            aos_root: Path = root or Path(os.environ[AosEnv.AOS_ROOT.name])
        except KeyError:
            raise NoAosEnvVariableError(AosEnv.AOS_ROOT)
        super().__init__(aos_root)

    @overrides
    def get_module_makefile(self, module_name: Path) -> Path:
        makepath = self.root.joinpath('modules').joinpath('Makefile')
        if not makepath.exists():
            raise CannotFindMakefile(makepath)
        return makepath


class AppsPathManager(PathManager):
    def __init__(self, root: Path = None) -> None:
        try:
            apps_root: Path = root or Path(os.environ[AosEnv.AOS_APPS_ROOT.name])
        except:
            raise NoAosEnvVariableError(AosEnv.AOS_APPS_ROOT)
        super().__init__(apps_root)

    @overrides
    def get_module_makefile(self, module_name: Path) -> Path:
        path_content = module_name.parts
        app = path_content[0]
        makepath = self.root.joinpath('configurations')\
                                .joinpath(app)\
                                .joinpath('Makefile')
        if not makepath.exists():
            raise CannotFindMakefile(makepath)
        return makepath
