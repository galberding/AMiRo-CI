"""Controll the module creation and build process
"""
from copy import deepcopy
from pathlib import Path
from amirotest.model.aos_module import AosModule
from amirotest.model.option.aos_opt import AosOption, ConfVariable
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

    def generateConfiguredModulesFromTemplate(self, t_module: AosModule):
        conf_mat = self.generate_config_matrix()
        c_modules = []
        # print(conf_mat.shape)
        for i in range(conf_mat.shape[0]):
            variables = []
            for col in conf_mat.columns:
                variables.append(ConfVariable(col, conf_mat[col].iloc[i]))
            module = deepcopy(t_module)
            module.add_options(variables)
            module.resolve()
            c_modules.append(module)
        return c_modules

    def generate_config_matrix(self):
        return self.mat_builder.build_dataframe_config(
            self.repl_conf.get_flatten_config())

    def generate_template_modules_from_repl_conf(self) -> list[AosModule]:
        modules = []
        options = self._generate_options()

        for module_name in self.repl_conf.get_module_names():
            # print(module_name)
            module = AosModule(Path(module_name))
            module.add_options(options)
            modules.append(module)
        return modules

    def _generate_options(self) -> list[AosOption]:
        options = []
        for option, _ in self.repl_conf.get_flatten_config().items():
            options.append(AosOption(option, f"$({option}_VAR)"))
        return options


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
