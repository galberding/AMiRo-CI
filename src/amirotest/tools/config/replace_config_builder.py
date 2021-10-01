from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from overrides.overrides import overrides
from amirotest.tools.config.config_yaml_handler import ConfigYmlHandler
from amirotest.tools.config.config_tags import ConfTag


ConfigYmlHandler

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
        self.options = {}
        self.apps = []
        self.exclude = []
        self.include = []
        self.make_options = {}

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

    def filter_option_groups(
            self,
            exclude: list[str] = [],
            include: list[str] = []) -> dict[str, dict[str, list[str]]]:
        """!Applies filter in for of name matching.
        The exclude and include filter hold names of options groups listed in the
        replacement config. In case a name appears in one if those lists the
        option group is either ignored or listed in the resulting options.
        @param exclude list instructing which groups to exclude
        @param include list which options to include
        @note If a name matches both filters it will be included.
        @note Subgroups are excluded if the parent is excluded.
        @return dict of option groups with no subgroups (the dict is not nested)
        """
        filtered_groups = {}
        for group_name, group_members in self.options.items():
            if self.ignore_group(group_name, include, exclude):
                continue
            filtered_groups.update(
                self.apply_to_nested_groups(
                    group_name, group_members, exclude=exclude, include=include))
        return filtered_groups

    def apply_to_nested_groups(self,parent_group_name: str,
                                 parent_group: dict,
                                 exclude: list[str] = [],
                                 include: list[str] = []) -> dict[str,dict[str,list[str]]]:
        """!Applies the include and exclude filter to all subgroups if existing.
        Furthermore all subgroups are removed such that the resulting dict is not
        nested.
        """
        opt_group = {parent_group_name: {}}
        for name, val in parent_group.items():
            if isinstance(val, dict): # group detected
                if self.ignore_group(name, include, exclude):
                    continue
                opt_group.update(self.apply_to_nested_groups(name, val))
            else:
                opt_group[parent_group_name][name] = val
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
        self._set_filter()
        self._set_make_options()

    def _set_module_names(self) -> bool:
        """!Set module names.
        * Required tag, ConfigFormatException raised if not existing
        * Used to set target for build
        """
        try:
            self.module_names = self.conf[ConfTag.Modules.name]
        except:
            raise ConfigFormatError("Cannot find module names!\nAdd \"Modules: [...]\" to the config!")
        return bool(self.module_names)

    def _set_options(self) -> bool:
        """!Set unfiltered option groups.
        * Required tag, ConfigFormatException raised if not existing
        """
        try:
            self.options = self.conf[ConfTag.Options.name]
        except:
            raise ConfigFormatError("Cannot find Options!\nAdd \"Options: {...}\" to the config!")
        return bool(self.options)

    def _set_apps(self):
        """!Set Apps that should be tested.
        * Optional tag
        * Only works in combination with Amiro Apps
        """
        if ConfTag.Apps.name in self.conf:
            self.apps = self.conf[ConfTag.Apps.name]

    def _set_filter(self):
        """!Set exclude and include filter.
        * Optional tags
        * Include dominates Exclude (see filter_option_groups())
        """
        if ConfTag.ExcludeOptions.name in self.conf:
            self.exclude = self.conf[ConfTag.ExcludeOptions.name]

        if ConfTag.IncludeOptions.name in self.conf:
            self.include = self.conf[ConfTag.IncludeOptions.name]

    def _set_make_options(self):
        if ConfTag.MakeOptions.name in self.conf:
            self.make_options.update(self.conf[ConfTag.MakeOptions.name])

    def get_flatten_config(self) -> dict[str, list]:
        """!Remove all config groups and join all underlying options.
        A config group is usually provided to indicate where the options take effect
        or determine how those options should be treated.
        Options in different groups have different names therefore they
        can be merged together.
        @return dict with all options as keys and lists as values.
        """
        flattened = {}
        for _, opt in self.get_filtered_groups().items():
            flattened.update(opt)
        return flattened

    def get_filtered_groups(self):
        """!Wrapper for filter_option_groups().
        """
        return self.filter_option_groups(exclude=self.exclude, include=self.include)
