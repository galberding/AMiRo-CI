from amirotest.model import AosModule
from amirotest.tools.makefile_search import MakefileSearch
from ..test_utils.path_helper import PathHelper

class UnknownModuleNameException(Exception):
    pass

class AosModuleHelper:
    def __init__(self) -> None:
        self.helper = PathHelper()
        self.searcher = MakefileSearch()
        self.module_names = [
            "DiWheelDrive_1-1",
            "DiWheelDrive_1-2",
            "LightRing_1-0",
            "LightRing_1-2",
            "NUCLEO-F103RB",
            "NUCLEO-F401RE",
            "NUCLEO-F767ZI",
            "NUCLEO-G071RB",
            "NUCLEO-L476RG",
            "PowerManagement_1-1",
            "PowerManagement_1-2",
            "STM32F407G-DISC1",
        ]

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

    def get_nucleo_with_options(self) -> AosModule:
        return self.get_module_with_options("NUCLEO-L476RG")

    def get_power_management_with_options(self) -> AosModule:
        return self.get_module_with_options("PowerManagement_1-2")

    def get_modules_with_options(self, module_names: list[str]) -> list[AosModule]:
        modules = []
        for module_name in module_names:
            modules.append(self.get_module_with_options(module_name))
        return modules

    def get_module_with_options(self, module_name: str) -> AosModule:
        if module_name not in self.module_names:
            raise UnknownModuleNameException(f"Cannot find {module_name}")
        module = self.get_aos_module(module_name=module_name)
        global_opts  = self.search_global_options_for(module_name)
        user_opts = self.search_user_options_for(module_name)
        module.create_global_options(global_opts)
        module.create_user_options(user_opts)
        return module

    def search_global_options_for(self, module_name) -> list[tuple[str, str]]:
        return self.searcher.search_global_options(
            self.get_aos_module(module_name=module_name).get_makefile())

    def search_user_options_for(self, module_name) -> list[tuple[str, str]]:
        return self.searcher.search_user_options(
            self.get_aos_module(module_name=module_name).get_makefile())

    def get_aos_module(self, module_name="NUCLEO-L476RG") -> AosModule:
        nucleo_path = self.helper.get_aos_module_path(module_name=module_name)
        return AosModule(nucleo_path)
