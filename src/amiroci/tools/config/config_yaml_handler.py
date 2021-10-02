from pathlib import Path
from typing import Any
from .. import yml_load, yml_dump, Loader, Dumper


class ConfigYmlHandler:
    def get_config(self, conf_path: Path) -> dict[str, Any]:
        with conf_path.open() as conf:
            data = yml_load(conf, Loader=Loader)
        return data

    def write_conf_to_file(self, path: Path, conf: dict):
        with path.open("w") as f:
            f.write(yml_dump(conf, Dumper=Dumper, default_flow_style=None))
