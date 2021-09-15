from abc import ABC, abstractmethod
from pathlib import Path

from overrides.overrides import overrides

from amirotest.tools.aos_module_default_config_creatro import ConfigYmlHandler
from amirotest.tools.config.config_tags import ConfTag


class ConfigFormatError(Exception):
    pass

class ReplaceConfigNotFound(Exception):
    def __init__(self, path: Path) -> None:
        msg = f"Cannot find config: {path}"
        super().__init__(msg)


class ReplaceConfig(ABC):
    """!Load the replacement configuration.
    During the load it is checked if the provided config is valid.
    """
    def __init__(self) -> None:
        self.valid = False
        self.conf = {}
        self.module_names: list[str] = []
        self.options = []
        self.apps = []

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

    def filter_option_groups(self, exclude: list[str] = [], include: list[str] = []) -> dict[str, dict[str, list[str]]]:
        options = self.conf[ConfTag.Options.name]
        filtered_groups = {}
        for group_name, group_members in options.items():
            if self.ignore_group(group_name, include, exclude):
                continue
            filtered_groups.update(
                self.apply_to_nested_groups(
                    group_name, group_members, exclude=exclude))
        return filtered_groups

    def apply_to_nested_groups(self,opt_group_name: str,
                                 group: dict,
                                 exclude: list[str] = [],
                                 include: list[str] = []) -> dict[str,dict[str,list[str]]]:
        opt_group = {opt_group_name: {}}
        for name, val in group.items():
            if self.ignore_group(name, include, exclude):
                continue
            if isinstance(val, dict):
                opt_group.update(self.apply_to_nested_groups(name, val))
            else:
                opt_group[opt_group_name][name] = val
        return opt_group

    def ignore_group(self, name:str, include: list[str], exclude: list[str]) -> bool:
        """!Is true when name is not listed in include or contained in exclude.
        The include path is checked before the exclude path, in case both lists are provided
        """
        if include:
            return name not in include
        elif exclude:
            return name in exclude
        return False


    def get_dependencies(self) -> dict:
        if ConfTag.Dependencies.name in self.conf:
            return self.conf[ConfTag.Dependencies.name]
        return {}


class YamlReplConf(ReplaceConfig, ConfigYmlHandler):

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.load(path)

    @overrides
    def load(self, path: Path):
        if not path.exists():
            raise ReplaceConfigNotFound(path)
        self.valid = True
        self.conf = self.get_config(path)
        self.valid &= self._set_module_names()
        self.valid &= self._set_options()
        self._set_apps()

    def _set_module_names(self) -> bool:
        try:
            self.module_names = self.conf[ConfTag.Modules.name]
        except:
            raise ConfigFormatError("Cannot find module names!\nAdd \"Modules: [...]\" to the config!")
        return bool(self.module_names)

    def _set_options(self) -> bool:
        try:
            self.options = self.conf[ConfTag.Options.name]
        except:
            raise ConfigFormatError("Cannot find Options!\nAdd \"Options: {...}\" to the config!")
        return bool(self.options)

    def _set_apps(self):
        if ConfTag.Apps.name in self.conf:
            self.apps = self.conf[ConfTag.Apps.name]

    def get_flatten_config(self) -> dict[str, list]:
        """!Remove all config groups and join all underlying options.
        A config group is usually provided to indicate where the options take effect
        or determine how those options should be treated.
        Options in different groups have different names therefore they
        can be merged together.
        @return dict with all options as keys and lists as values.
        """
        flattened = {}
        for _, opt in self.options.items():
            flattened.update(opt)
        return flattened
