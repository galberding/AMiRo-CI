from pathlib import Path

class PathHelper():

    def __init__(self, aos_root=Path("/home/schorschi/hiwi/AMiRo-OS")):
        self.aos_path = aos_root
        self.default_test_env = Path("/tmp/aos_test_env/")
        self.default_config_yml_path = self.default_test_env.joinpath("default_conf.yml")

    def create_test_env(self):
        self.default_test_env.mkdir(parents=True, exist_ok=True)

    def clear_test_env(self):
        self.default_config_yml_path.unlink(missing_ok=True)

    def get_aos_module_dir(self) -> Path:
        return self.aos_path.joinpath("modules")

    def list_aos_module_paths(self) -> list[Path]:
        aos_modules = []
        for path_obj in self.get_aos_module_dir().glob("*"):
            if path_obj.is_dir():
                aos_modules.append(path_obj)
        return aos_modules

    def get_aos_module_path(self, module_name="NUCLEO-L476RG") -> Path:
        moduleSearch = [i for i in self.list_aos_module_paths() if i.name == module_name]
        if len(moduleSearch) == 0:
            raise Exception("Module does not exist")
        return moduleSearch[0]

    def get_default_config_yml_path(self) -> Path:
        return self.default_config_yml_path
