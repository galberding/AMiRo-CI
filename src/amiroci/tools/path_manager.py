from abc import ABC, abstractmethod
from logging import Logger
import logging
import os
from pathlib import Path
from enum import Enum, auto
from typing import Optional
from overrides.overrides import overrides
from amiroci.tools.aos_logger import get_logger
import shutil

class AosEnv(Enum):
    AOS_ROOT = 'Amiro-OS'
    AOS_APPS_ROOT = 'Amiro-Apps'
    AOS_REPLACE_CONF = 'Replacement Config'


class NoAosEnvVariableError(Exception):
    def __init__(self, param: AosEnv) -> None:
        super().__init__(
            f'''
        Please set an environment variable with:
        \texport {param.name}=path/to/{param.value}
        '''
        )


class AosEnvPathNotFound(Exception):
    def __init__(self, param: AosEnv, path: Path) -> None:
        super().__init__(f'Cannot find {path} set by: {param.name}')


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
    def __init__(
            self,
            root: Path,
            repl_conf: Optional[Path],
            builddir=Path("/dev/shm/amiroCI"),
            move_root_to_ram: bool = False
    ) -> None:
        self.root = root
        self.log: Logger = get_logger(type(self).__name__)
        self.b_dir: Path = builddir
        self.move_root: bool = move_root_to_ram
        self.b_dir.mkdir(exist_ok=True)
        self.repl_conf = repl_conf \
            or self.get_env_path(AosEnv.AOS_REPLACE_CONF)
        if not self.root.exists():
            raise CannotFindProjectRoot(f"Cannot find module at: {self.root}")
        if move_root_to_ram:
            self.log.info(f'''Move Project to Ram:
            {self.root}
            to: target.''')
            self.copy_root_to_builddir()

    def get_project_makefile(self) -> Path:
        return self.root.joinpath("Makefile")

    @abstractmethod
    def get_module_makefile(self, module_name: Path) -> Path:
        """!Construct path to Makefile where the target is included.
        """

    def get_repl_conf_path(self) -> Path:
        """!Return path to replacement config
        """
        return self.repl_conf

    def get_build_dir(self) -> Path:
        return self.b_dir

    def _ensure_config_exists(self, config: Path):
        if not config.exists():
            raise CannotFindConfigError(config)

    def get_report_path(self) -> Path:
        return self.repl_conf.parent.joinpath('report.tsv')

    def get_conf_mat_path(self, name=None) -> Path:
        return self.repl_conf.parent.joinpath(name or 'conf_mat.tsv')

    def get_env_path(self, param: AosEnv) -> Path:
        if param.name in os.environ:
            path = Path(os.environ[param.name])
            if not path.exists():
                raise AosEnvPathNotFound(param, path)
            return path
        else:
            raise NoAosEnvVariableError(param)

    def copy_root_to_builddir(self):
        """Copy the project root to the builddir.
        This is only effective if the builddir is placed on a ramdisk (default: /dev/shm/...)
        """
        self.root = Path(shutil.copytree(self.root, self.b_dir.joinpath(self.root.name)))

    # def __del__(self):
    #     if self.move_root:
    #         shutil.rmtree(self.b_dir)

class AosPathManager(PathManager):
    def __init__(
            self,
            root: Optional[Path] = None,
            repl_conf: Optional[Path] = None,
            move_root_to_ram = False

    ) -> None:
        aos_root = root \
            or self.get_env_path(AosEnv.AOS_ROOT)

        try:
            aos_root: Path = root or Path(os.environ[AosEnv.AOS_ROOT.name])
        except KeyError:
            raise NoAosEnvVariableError(AosEnv.AOS_ROOT)
        super().__init__(aos_root, repl_conf=repl_conf, move_root_to_ram=move_root_to_ram)

    @overrides
    def get_module_makefile(self, module_name: Path) -> Path:
        makepath = self.root.joinpath('modules').joinpath('Makefile')
        if not makepath.exists():
            raise CannotFindMakefile(makepath)
        return makepath


class AppsPathManager(PathManager):
    def __init__(self, root: Path = None, repl_conf=None, move_root_to_ram = False) -> None:
        try:
            apps_root: Path = root or Path(
                os.environ[AosEnv.AOS_APPS_ROOT.name]
            )
        except:
            raise NoAosEnvVariableError(AosEnv.AOS_APPS_ROOT)
        super().__init__(apps_root, repl_conf=repl_conf, move_root_to_ram=move_root_to_ram)

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
