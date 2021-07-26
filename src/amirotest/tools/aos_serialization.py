from abc import ABC, abstractclassmethod, abstractmethod
from pathlib import Path
from yaml import load, dump

from amirotest.model.aos_model import AOSModule
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class AosDumper(ABC):
    @abstractmethod
    def dump(self, module: AOSModule, conf_path: Path):
        """Write module to file."""

    def dump_all(self, modules: list[AOSModule], conf_path: Path):
        for module in modules:
            self.dump(module, conf_path)


class YamlDumper(AosDumper):
    def dump(self, module: AOSModule, conf_path: Path):
        pass


class AosLoader(ABC):
    @abstractmethod
    def load(self, conf_path: Path) -> list[AOSModule]:
        """Return list of modules if config path exists"""
