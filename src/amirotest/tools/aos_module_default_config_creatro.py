from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from . import yml_load, yml_dump, Loader, Dumper

from .search.search_result import SearchResult
# from amirotest.model.option import GlobalOption, UserOption
# from amirotest.model.aos_module import AosModule
import amirotest.model.aos_module as aos_module
import amirotest.model.option as aos_opt
import amirotest.model.option as aos_opt

GlobalOption = aos_opt.MakeGlobalOption
UserOption = aos_opt.MakeUserOption
AosModule = aos_module.AosModule

class ConfigYmlHandler:
    def get_config(self, conf_path: Path) -> Optional[dict]:
        with conf_path.open() as conf:
            data = yml_load(conf, Loader=Loader)
        return data

    def write_conf_to_file(self, path: Path, conf: dict):
        with path.open("w") as f:
            f.write(yml_dump(conf, Dumper=Dumper, default_flow_style=None))


class AosDumper(ABC):
    @abstractmethod
    def dump(self, module: AosModule, conf_path: Path):
        """Write module to file."""

    def dump_all(self, modules: list[AosModule], conf_path: Path):
        for module in modules:
            self.dump(module, conf_path)


class YamlDumper(AosDumper, ConfigYmlHandler):
    def dump(self, module: AosModule, conf_path: Path):
        current_conf = module.to_default_config_dict()
        # Update old conf if it exists with new module
        if conf_path.exists():
            old_conf = self.get_config(conf_path)
            if old_conf:
                old_conf.update(current_conf)
                current_conf = old_conf
        else:
            conf_path.touch(exist_ok=True)
        self.write_conf_to_file(conf_path, current_conf)


class AosModuleLoader(ABC):
    @abstractmethod
    def load(self, conf: Path) -> list[AosModule]:
        """Load modules from config file"""

# TODO: Dangerous Do not use!!
class YamlLoader(AosModuleLoader, ConfigYmlHandler):
    def load(self, conf: Path) -> list[AosModule]:
        default_conf = self.get_config(conf)
        return self.get_modules_from_config(default_conf)

    def get_modules_from_config(self, default_conf: dict) -> list[AosModule]:
        modules = []
        for module_name, config in default_conf.items():
            modules.append(self.create_module(module_name, config))
        return modules

    def create_module(self, module_name: str, config: dict):
        # TODO: Workaround for module creation because path is required (previously)
        # in order to search the Makefile
        # ==> How to handle paths after modules are loaded from default config?
        module = AosModule(Path(module_name))
        # print(config)
        # global_config_options = self.get_options_by_type(config, GlobalOption.__name__)
        config_options = self.dict_to_options(config)
        module.add_options(config_options)
        # print(global_config_options)
        # if global_config_options:
            # module.add_options(SearchResult(global_config_options, GlobalOption).get_options())
        # user_config_options = self.get_options_by_type(config, UserOption.__name__)
        # if user_config_options:
            # module.add_options(SearchResult(user_config_options, UserOption).get_options())
        return module

    def get_options_by_type(self, config: dict, opt_type: str):
        if opt_type in config:
            return self._get_options(config[opt_type])

    def dict_to_options(self, conf):
        print(conf)
        # TODO: for later if it is required to load modules from default:
        # https://stackoverflow.com/questions/11775460/lexical-cast-from-string-to-type


    def _get_options(self, config: dict) -> list[tuple[str, str]]:
        results = []
        for name, args in config.items():
            results.append((name, " ".join(args)))
        return results
