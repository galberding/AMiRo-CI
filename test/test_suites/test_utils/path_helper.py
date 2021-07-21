from pathlib import Path
import unittest

from amirotest.model.aos_model import AOSModule


class PathHelper():

    def __init__(self, aos_root=Path("/home/schorschi/hiwi/AMiRo-OS")):
        self.aos_path = aos_root

    def getPathToAosModules(self) -> Path:
        return self.aos_path.joinpath("modules")

    def listAosModules(self) -> list[Path]:
        aos_modules = []
        for path_obj in self.getPathToAosModules().glob("*"):
            if path_obj.is_dir():
                aos_modules.append(path_obj)
        return aos_modules

    def get_aos_module_path(self, module_name="NUCLEO-L476RG") -> Path:
        moduleSearch = [i for i in self.listAosModules() if i.name == module_name]
        if len(moduleSearch) == 0:
            raise Exception("Module does not exist")
        return moduleSearch[0]

    def get_aos_module(self, module_name="NUCLEO-L476RG") -> AOSModule:
        nucleo_path = self.get_aos_module_path(module_name=module_name)
        return AOSModule(nucleo_path)
