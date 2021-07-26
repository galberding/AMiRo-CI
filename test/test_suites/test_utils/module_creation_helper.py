

from pathlib import Path
from amirotest.model.aos_model import AOSModule
from ..test_utils.path_helper import PathHelper


class AosModuleMockData:
    def __init__(self) -> None:
        self.helper = PathHelper()
        self.nucleo_search_results = [
            ('USE_OPT', '-O2 -fstack-usage -Wl,--print-memory-usage'), # Has option for preprocessor (-Wl,)
            ('USE_COPT', '-std=c99 -fshort-enums'),
            ('USE_CPPOPT', '-fno-rtti -std=c++17'),
            ('USE_LINK_GC', 'yes'),
            ('USE_LDOPT', '-lm'),
            ('USE_LTO', 'yes'),
            ('USE_VERBOSE_COMPILE', 'no'),
            ('USE_SMART_BUILD', 'no'),
            ('USE_PROCESS_STACKSIZE', '0x400'),
            ('USE_EXCEPTIONS_STACKSIZE', '0x400'),
            ('USE_FPU', 'softfp'),
            ('USE_FPU_OPT', '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16') # Needs to be substituted
        ]
        self.nucleo_flag_count = len(self.nucleo_search_results)

    def get_nucleo_with_flags(self) -> AOSModule:
        module = self.get_aos_module()
        module.create_flags(self.nucleo_search_results)
        return module

    def get_aos_module(self, module_name="NUCLEO-L476RG") -> AOSModule:
        nucleo_path = self.helper.get_aos_module_path(module_name=module_name)
        return AOSModule(nucleo_path)

    def listAosModules(self) -> list[Path]:
        aos_modules = []
        for path_obj in self.helper.get_aos_module_dir().glob("*"):
            if path_obj.is_dir():
                aos_modules.append(path_obj)
        return aos_modules
