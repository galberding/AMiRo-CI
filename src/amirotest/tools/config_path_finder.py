from abc import ABC, abstractmethod
from pathlib import Path

class CannotFindConfigError(Exception):
    def __init__(self, config: Path) -> None:
        msg = f"Cannot find config at: {config}!"
        super().__init__(msg)

class CannotFindModuleError(Exception):
    pass

class ConfigFinder(ABC):
    def __init__(self, module_path: Path) -> None:
        self.module = module_path
        if not self.module.exists():
            raise CannotFindModuleError(f"Cannot find module at: {self.module}")

    @abstractmethod
    def get_makefile(self) -> Path:
        pass

    @abstractmethod
    def get_aosconf(self) -> Path:
        pass

    def _ensure_config_exists(self, config: Path):
        if not config.exists():
            raise CannotFindConfigError(config)

class AosConfigFinder(ConfigFinder):
    def __init__(self, module_path: Path) -> None:
        self.aos_root = module_path.parent.parent
        if not self.aos_root.exists():
            pass
        super().__init__(module_path)

    def get_makefile(self) -> Path:
        return self._get_module_config_by_name("Makefile")

    def get_aosconf(self) -> Path:
        return self._get_module_config_by_name("aosconf.h")

    def get_repl_conf_path(self) -> Path:
        # TODO: Point to correct path!
        return Path("/home/schorschi/hiwi/amiroci/assets/repl_conf.yml")

    def _get_module_config_by_name(self, name: str):
        conf = self.module.joinpath(name)
        self._ensure_config_exists(conf)
        return conf


class AppsConfigFinder(ConfigFinder):
    def __init__(self, module_path: Path) -> None:
        super().__init__(module_path)
