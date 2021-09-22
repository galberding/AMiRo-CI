"""Control the module creation and build process.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
from amirotest.controller.build_executer import BuildExecutor
from amirotest.model.aos_module import AosModule
from amirotest.model.option.aos_opt import AosOption, ConfVariable, MakeOption
from amirotest.tools.config.conf_matrix_builder import ConfMatrixBuilder
from amirotest.tools.config.dependency_checker import DependencyChecker
from amirotest.tools.config.replace_config_builder import ReplaceConfig


class ConfigInvalidError(Exception):
    pass


class BuildController:
    """!# Build Controller
    The BuildController connects all components together
    and provides following functionality:
    1. Create the configuration Matrix
    2. Generate template modules
    3. Configure template modules
    4. TODO: Pass configured modules to BuildExecutor
    5. TODO: Call reporter on the build results
    @warning: The prebuild conf matrix is not validated right now!
    """
    def __init__(self,
                 repl_conf: ReplaceConfig,
                 build_executor: BuildExecutor,
                 prebuild_conf_matrix: Optional[pd.DataFrame] = None) -> None:
        """!# Initialize controller
        - Check if repl config exists
        - initialize conf matrix builder
        @param repl_conf: ReplaceConfig for generating test cases
        @param build_executor: BuildExecuter to controll the execution
        @param builddir: directory to save build results
        """

        self.repl_conf = repl_conf
        # self.repl_conf = YamlReplConf(finder.get_repl_conf_path())
        # TODO: Better place would be in the repl_conf to not allow an
        # invalid config in the first place!
        if not self.repl_conf.is_valid():
            raise ConfigInvalidError("Cannot use config!")
        self.mat_builder = ConfMatrixBuilder()

        self.b_executor = build_executor
        self.dep_checker = DependencyChecker(self.repl_conf.get_dependencies())
        self.prebuild_conf_matrix = prebuild_conf_matrix


    def execute_build_modules(self) -> list[AosModule]:
        """!Generate configured modules from replacement config and invoke the
        executor to build those modules.
        @return List of AosModule with BuildInformation
        @note
        This is the entrypoint of the test pipeline. One can use the generated modules for
        report creation.
        """
        c_modules = self.c_modules
        self.b_executor.build(c_modules)
        return c_modules

    @property
    def c_modules(self) -> list[AosModule]:
        """!Construct configured modules based on replacement config.
        """
        t_modules = self.generate_template_modules_from_repl_conf()
        c_modules = self.generate_configured_modules_from_templates(t_modules)
        return c_modules


    def generate_template_modules_from_repl_conf(self) -> list[AosModule]:
        """!Generate template modules from given module names and options
        provided by replace config.
        If apps are provided the module names are combined with those.
        """
        modules = []
        options = self._generate_template_options()
        m_names = self.repl_conf.module_names
        apps = self.repl_conf.apps
        for module_name in m_names:
            if apps:
                for app in apps:
                    modules.append(
                        self._generate_template_module(f'{app}/{module_name}', options))
            else:
                modules.append(self._generate_template_module(module_name, options))
        return modules

    def _generate_template_options(self) -> list[AosOption]:
        """!Generate option from replacement config.
        The replacement config proves the get_flatten_config() in order
        to get all option.
        TODO: Too many responsibilities!
        Instead of manually adding the _VAR to the option this should
        be done in a specific AosOption subclass.
        """
        options = []
        for option, _ in self.repl_conf.get_flatten_config().items():
            options.append(AosOption(option, f"$({option}_VAR)"))

        options += self._generate_make_options()
        return options

    def _generate_make_options(self):
        make_opts = []
        for name, args in self.repl_conf.make_options.items():
            make_opts.append(MakeOption(name, ' '.join(args)))
        return make_opts

    def _generate_template_module(self, name: str,
                                  options: list[AosOption]) -> AosModule:
        """!Return AosModule, set options and
        """
        module = AosModule(Path(name))
        module.add_options(options)
        return module


    def generate_configured_modules_from_templates(self, t_modules: list[AosModule]) -> list[AosModule]:
        c_mods = []
        for tmod in t_modules:
            c_mods += self.generate_configured_modules_from_template(tmod)
        return c_mods

    def generate_configured_modules_from_template(self, t_module: AosModule) -> list[AosModule]:
        """!Generate configured modules from template.
        All configurations, listed in the conf matrix are used to configure the template.
        At the end each row in the conf matrix generate one configured module.
        The template modules is copied and subsequently configured.
        @param t_module: Template AosModule
        @return list of configured AosModules
        """
        conf_mat = self.prebuild_conf_matrix if self.prebuild_conf_matrix is not None else self.generate_config_matrix()
        c_modules = []
        for row in range(conf_mat.shape[0]):
            variables: list[AosOption] = []
            for col in conf_mat.columns: # type: ignore
                variables.append(ConfVariable(col, conf_mat[col].iloc[row]))
            # create module and add options
            module = t_module.copy()
            module.add_options(variables)
            module.resolve()
            # exclude non matching options
            if self.dep_checker.is_valid(module):
                c_modules.append(module)
        return c_modules

    def generate_config_matrix(self) -> pd.DataFrame:
        """!Invoke ConfMatrixBuilder to generate the conf matrix.
        @return DataFrame
        """
        return self.mat_builder.build_dataframe_config(
            self.repl_conf.get_flatten_config())



# Build module from search
# Build module from replacement config
# Create module configurations
# substitute configuration -> create configured module
# Build configured module
# Build all configured modules -> parallel
# Collect build results
# Check expectations
