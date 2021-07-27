from amirotest.model.aos_model import AOSModule
from amirotest.tools.makefile_search import MakefileSearch
from ..test_utils.path_helper import PathHelper


class AosModuleHelper:
    def __init__(self) -> None:
        self.helper = PathHelper()
        self.searcher = MakefileSearch()

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
        user_res = self.get_user_results_for("NUCLEO-L476RG")
        module.create_global_options(self.nucleo_search_results)
        module.create_user_options(user_res)
        return module

    def get_global_results_for(self, module_name) -> list[tuple[str, str]]:
        return self.searcher.search_global_options(
            self.get_aos_module(module_name=module_name).get_makefile())

    def get_user_results_for(self, module_name) -> list[tuple[str, str]]:
        return self.searcher.search_user_options(
            self.get_aos_module(module_name=module_name).get_makefile())

    def get_aos_module(self, module_name="NUCLEO-L476RG") -> AOSModule:
        nucleo_path = self.helper.get_aos_module_path(module_name=module_name)
        return AOSModule(nucleo_path)
