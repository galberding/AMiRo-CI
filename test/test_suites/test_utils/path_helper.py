from pathlib import Path
import unittest

from amirotest.model.aos_model import Module


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

    def select_aos_module(self, module_name="NUCLEO-L476RG") -> Path:
        moduleSearch = [i for i in self.listAosModules() if i.name == module_name]
        if len(moduleSearch) == 0:
            raise Exception("Module does not exist")
        return moduleSearch[0]

    def get_nucleo_module(self) -> Module:
        nucleo_path = self.select_aos_module()
        return Module(nucleo_path)
