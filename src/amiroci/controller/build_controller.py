"""Control the module creation and build process.
"""

from pathlib import Path
from typing import Iterator, Optional
import pandas as pd
from amiroci.controller.build_executer import BuildExecutor
from amiroci.model.aos_module import AosModule
from amiroci.model.option.aos_opt import AosOption, CfgOption, ConfVariable, MakeOption
from amiroci.tools.aos_logger import get_logger
from amiroci.tools.config.conf_matrix_builder import ConfMatrixBuilder
from amiroci.tools.config.dependency_checker import DependencyChecker
from amiroci.tools.config.replace_config_builder import ReplaceConfig

# log = get_logger(__name__)


class ConfigInvalidError(Exception):
    pass


class CModuleBuilder:
    """!Construct configured modules and wrap them in an iterator.
    """
    def __init__(
        self, t_modules: list[AosModule], conf_mat: pd.DataFrame
    ) -> None:
        self.log = get_logger(type(self).__name__)
        self.conf_mat = conf_mat
        self.t_modules = t_modules
        self.t_mod = 0
        self.row = 0
        self.col = 0

    def __iter__(self):
        self.row = 0
        self.t_mod = 0
        return self

    def __next__(self) -> AosModule:
        if self.t_mod >= len(self.t_modules):
            raise StopIteration
        module = self.generate_configured_module()
        self.inc_row()
        return module

    def __len__(self):
        return self.conf_mat.shape[0] * len(self.t_modules)

    def generate_configured_module(self) -> AosModule:
        variables: list[AosOption] = []
        for col in self.conf_mat.columns:  # type: ignore
            variables.append(
                ConfVariable(col, self.conf_mat[col].iloc[self.row])
            )
        # create module and add options
        module = self.t_modules[self.t_mod].copy()
        module.add_options(variables)
        module.resolve()
        return module

    def inc_row(self):
        self.row += 1
        if self.row == self.conf_mat.shape[0]:
            self.row = 0
            self.t_mod += 1


class BuildController:
    """!# Build Controller
    The BuildController is responsible for generating configured modules.
    It builds them in the following order:
    1. Create the configuration Matrix
    2. Generate template modules
    3. Generate configured modules from templates
    @warning: The prebuild conf matrix is not validated right now!
    """
    def __init__(
        self,
        repl_conf: ReplaceConfig,
        prebuild_conf_matrix: Optional[pd.DataFrame] = None
    ) -> None:
        """!# Initialize controller
        - Check if repl config exists
        - initialize conf matrix builder
        @param repl_conf: ReplaceConfig for generating test cases
        @param build_executor: BuildExecuter to controll the execution
        @param builddir: directory to save build results
        """
        self.log = get_logger(type(self).__name__)
        self.repl_conf = repl_conf
        self.mat_builder = ConfMatrixBuilder()

        self.dep_checker = DependencyChecker(self.repl_conf.get_dependencies())
        self.conf_matrix = prebuild_conf_matrix

    def iter_c_modules(self) -> Iterator[AosModule]:
        """!Construct iterator that builds configured modules.
        """
        if self.conf_matrix == None:
            self.log.debug('No default matrix provided, generating one ...')
            self.conf_mat = self.generate_config_matrix()
        else:
            self.log.debug('Default provided, continuing ...')
        t_modules = self.generate_template_modules_from_repl_conf()
        builder = CModuleBuilder(t_modules, self.conf_mat)
        return iter(builder)

    @property
    def c_modules(self) -> list[AosModule]:
        """!Construct configured modules based on replacement config.
        """
        return list(self.iter_c_modules())

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
                        self._generate_template_module(
                            f'{app}/{module_name}', options
                        )
                    )
            else:
                modules.append(
                    self._generate_template_module(module_name, options)
                )
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
            options.append(CfgOption(option, f"$({option}_VAR)"))

        options += self._generate_make_options()
        return options

    def _generate_make_options(self):
        make_opts = []
        for name, args in self.repl_conf.make_options.items():
            make_opts.append(MakeOption(name, args))
        return make_opts

    def _generate_template_module(
        self, name: str, options: list[AosOption]
    ) -> AosModule:
        """!Return AosModule, set options and
        """
        module = AosModule(Path(name))
        module.add_options(options)
        return module

    def generate_configured_modules_from_templates(
        self, t_modules: list[AosModule]
    ) -> list[AosModule]:
        c_mods = []
        for tmod in t_modules:
            c_mods += self.generate_configured_modules_from_template(tmod)
        return c_mods

    def generate_configured_modules_from_template(
        self, t_module: AosModule
    ) -> list[AosModule]:
        """!Generate configured modules from template.
        All configurations, listed in the conf matrix are used to configure the template.
        At the end each row in the conf matrix generate one configured module.
        The template modules is copied and subsequently configured.
        @param t_module: Template AosModule
        @return list of configured AosModules
        """
        conf_mat = self.conf_matrix if self.conf_matrix is not None else self.generate_config_matrix(
        )
        c_modules = []
        for row in range(conf_mat.shape[0]):
            variables: list[AosOption] = []
            for col in conf_mat.columns:  # type: ignore
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
            self.repl_conf.get_flatten_config()
        )


# Build module from search
# Build module from replacement config
# Create module configurations
# substitute configuration -> create configured module
# Build configured module
# Build all configured modules -> parallel
# Collect build results
# Check expectations
