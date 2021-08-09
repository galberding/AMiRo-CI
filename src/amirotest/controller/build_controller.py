"""Controll the module creation and build process
"""
from pathlib import Path
from amirotest.model.aos_module import AosModule
from amirotest.model.option.aos_opt import AosOption
from amirotest.tools.config.conf_matrix_builder import ConfMatrixBuilder
from amirotest.tools.replace_config_builder import ReplaceConfig
class ConfigInvalidError(Exception):
    pass

class BuildController:
    def __init__(self, repl_conf: ReplaceConfig) -> None:
        self.repl_conf = repl_conf
        if not self.repl_conf.is_valid():
            raise ConfigInvalidError("Cannot use config!")
        self.mat_builder = ConfMatrixBuilder()

    def generate_config_matrix(self):
        return self.mat_builder.build_dataframe_config(
            self.repl_conf.get_flatten_config())

    def generate_template_modules_from_repl_conf(self):
        modules = []
        options = []
        for option, _ in self.repl_conf.get_flatten_config().items():
            options.append(AosOption(option, f"$({option}_VAR)"))

        for module_name in self.repl_conf.get_module_names():
            print(module_name)
            module = AosModule(Path(module_name))
            module.add_options(options)
            modules.append(module)
        return modules


    def generateConfiguredModulesFromTemplate(self):
        pass
    def buildConfiguredModules(self):
        pass
# Build module from search
# Build module from replacement config
# Create module configurations
# substitute configuration -> create configured module
# Build configured module
# Build all configured modules -> parallel
# Collect build results
# Check expectations
