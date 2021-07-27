from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from amirotest.model import AOSModule

from amirotest.tools import yml_load, yml_dump, Loader, Dumper

class AosDumper(ABC):
    @abstractmethod
    def dump(self, module: AOSModule, conf_path: Path):
        """Write module to file."""

    def dump_all(self, modules: list[AOSModule], conf_path: Path):
        for module in modules:
            self.dump(module, conf_path)


class YamlDumper(AosDumper):
    def dump(self, module: AOSModule, conf_path: Path):
        # current_conf = asdict(module)
        # module.resolve()
        current_conf = module.to_dict()

        # Update old conf if it exists with new module
        if conf_path.exists():
            old_conf = self.get_config(conf_path)
            if old_conf:
                old_conf.update(current_conf)
                current_conf = old_conf
        else:
            conf_path.touch(exist_ok=True)
        with conf_path.open("w") as conf:
            conf.write(yml_dump(current_conf, Dumper=Dumper, default_flow_style=None))

    def get_config(self, conf_path: Path) -> Optional[dict]:
        with conf_path.open() as conf:
            data = yml_load(conf, Loader=Loader)
        return data