from abc import ABC, abstractmethod
from pathlib import Path

class CannotFindConfigError(Exception):
    def __init__(self, config: Path) -> None:
        msg = f"Cannot find config at: {config}!"
        super().__init__(msg)

class CannotFindModuleError(Exception):
    pass

class CannotFindProjectRoot(Exception):
    pass

class ConfigFinder(ABC):
    def __init__(self, module_path: Path, builddir=Path("/dev/shm/amiroCI")) -> None:
        self.module = module_path
        self.b_dir = builddir
        if not self.module.exists():
            raise CannotFindModuleError(f"Cannot find module at: {self.module}")

    @abstractmethod
    def get_module_makefile(self, module_name: str) -> Path:
        pass

    @abstractmethod
    def get_aosconf(self, module_name: str) -> Path:
        pass

    @abstractmethod
    def get_project_makefile(self) -> Path:
        pass

    def get_repl_conf_path(self) -> Path:
        # TODO: Point to correct path!
        return Path("/home/schorschi/hiwi/amiroci/assets/repl_conf.yml")

    def get_build_dir(self) -> Path:
        return self.b_dir

    def _ensure_config_exists(self, config: Path):
        if not config.exists():
            raise CannotFindConfigError(config)

class AosModuleConfigFinder(ConfigFinder):
    def __init__(self, module_path: Path) -> None:
        self.aos_root = module_path.parent.parent
        if not self.aos_root.exists():
            raise CannotFindProjectRoot(f"AmiroOS not at location: {self.aos_root}")
        super().__init__(module_path)

    def get_module_makefile(self, module_name: str) -> Path:
        return self._get_module_config_by_name("Makefile")

    def get_aosconf(self, module_name: str) -> Path:
        return self._get_module_config_by_name("aosconf.h")

    def get_project_makefile(self) -> Path:
        return self.aos_root

    def _get_module_config_by_name(self, name: str):
        conf = self.module.joinpath(name)
        self._ensure_config_exists(conf)
        return conf

class AosPathManager(ConfigFinder):
    def __init__(self, aos_root: Path) -> None:
        self.aos_root = aos_root
        self.modules = self.aos_root.joinpath("modules")

        if not self.aos_root.exists():
            raise CannotFindProjectRoot(f"AmiroOS not at location: {self.aos_root}")
        super().__init__(aos_root)

    def get_module_makefile(self, module_name: str) -> Path:
        return self.modules.joinpath(module_name).joinpath("Makefile")

    def get_aosconf(self, module_name: str) -> Path:
        return self._get_module_path(module_name, "aosconf.h")

    def _get_module_path(self, module_name: str, file: str) -> Path:
        return self.modules.joinpath(module_name).joinpath(file)

    def get_project_makefile(self) -> Path:
        return self.aos_root.joinpath("Makefile")


# class AppsConfigFinder(ConfigFinder):
#     def __init__(self, module_path: Path) -> None:
#         super().__init__(module_path)
