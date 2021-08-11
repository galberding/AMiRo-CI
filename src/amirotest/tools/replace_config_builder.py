from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from warnings import catch_warnings

from amirotest.tools.aos_module_default_config_creatro import ConfigYmlHandler

class ConfigFormatError(Exception):
    pass

class ReplaceConfigNotFound(Exception):
    def __init__(self, path: Path) -> None:
        msg = f"Cannot find config: {path}"
        super().__init__(msg)


class ReplaceConfig(ABC):
    def __init__(self) -> None:
        self.valid = False
        self.conf = {}
        self.module_names: list[str] = []
        self.options = []

    @abstractmethod
    def load(self, path: Path):
        """Load config.
        """

    @abstractmethod
    def get_flatten_config(self) -> dict[str, list]:
        """Get flattened config.
        """

    def is_valid(self) -> bool:
        return self.valid

    def get_module_names(self) -> list[str]:
        return self.module_names

    def get_options(self):
        return self.options

class YamlReplConf(ReplaceConfig, ConfigYmlHandler):

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.load(path)

    def load(self, path: Path):
        if not path.exists():
            raise ReplaceConfigNotFound(path)
        self.valid = True
        self.conf = self.get_config(path)
        self.valid &= self._set_module_names()
        self.valid &= self._set_options()

    def _set_module_names(self) -> bool:
        try:
            self.module_names = self.conf["Modules"]
        except:
            raise ConfigFormatError("Cannot find module names!\nAdd \"Modules: [...]\" to the config!")
        return bool(self.module_names)

    def _set_options(self) -> bool:
        try:
            self.options = self.conf["Options"]
        except:
            raise ConfigFormatError("Cannot find Options!\nAdd \"Options: {...}\" to the config!")
        return bool(self.options)

    def get_flatten_config(self) -> dict[str, list]:
        # return super().get_flatten_config()
        flattened = {}
        for name, opt in self.options.items():
            # print(name)
            flattened.update(opt)
        return flattened
