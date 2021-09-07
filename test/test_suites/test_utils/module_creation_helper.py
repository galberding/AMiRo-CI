from amirotest.model import AosModule
from .test_helper import PathHelper

class UnknownModuleNameException(Exception):
    pass

class AosModuleHelper:
    def __init__(self) -> None:
        self.helper = PathHelper()
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


    def get_aos_module(self, module_name="NUCLEO-L476RG") -> AosModule:
        nucleo_path = self.helper.get_aos_module_path(module_name=module_name)
        return AosModule(nucleo_path)
