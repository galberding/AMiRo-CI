from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
from . import yml_load, yml_dump, Loader, Dumper
import amirotest.model.aos_module as aos_module
import amirotest.model.option as aos_opt
import amirotest.model.option as aos_opt

GlobalOption = aos_opt.MakeOption
UserOption = aos_opt.MakeUserOption
AosModule = aos_module.AosModule

class ConfigYmlHandler:
    def get_config(self, conf_path: Path) -> dict[str, Any]:
        with conf_path.open() as conf:
            data = yml_load(conf, Loader=Loader)
        return data

    def write_conf_to_file(self, path: Path, conf: dict):
        with path.open("w") as f:
            f.write(yml_dump(conf, Dumper=Dumper, default_flow_style=None))
