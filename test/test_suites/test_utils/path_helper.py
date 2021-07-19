from pathlib import Path
import unittest


class PathHelper():

    def getPathToAosModules(self) -> Path:
        return Path("/home/schorschi/hiwi/AMiRo-OS/modules/").resolve()

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
