import argparse
from argparse import Namespace
import logging
from pathlib import Path
from typing import Optional, Type
from amiroci.controller.build_controller import BuildController
import pandas as pd
from amiroci.controller.build_executer import BuildExecutor, ParallelExecutor
from amiroci.tools.aos_logger import get_logger
from amiroci.tools.path_manager import AosPathManager, AppsPathManager, PathManager
from amiroci.tools.gcc_version_checker import GccVersionChecker
from amiroci.tools.config.replace_config_builder import ReplaceConfig, YamlReplConf


class AmiroParser:
    """! Create CLI for configuring and executing the integration pipeline.
    """
    def __init__(
        self, executor: Type[BuildExecutor] = ParallelExecutor
    ) -> None:
        self.log = get_logger(
            type(self).__name__, logging.DEBUG, out='parser.log'
        )
        self.exe_type = executor
        self.p_man: Optional[PathManager] = None
        self.repl_conf: Optional[ReplaceConfig] = None
        self.bc: Optional[BuildController] = None
        self.executor: Optional[BuildExecutor] = None
        self.parser = argparse.ArgumentParser(prog='AmiroCI')
        self.add_project_group()
        self.add_config_args()
        self.gcc_version_checker = GccVersionChecker()

    def add_project_group(self):
        """!Add the project type.
        For now `AmiroOS` and `AmiroApps` are supported.
        It is important that this option is set because each project
        requires its own `PathManager`.
        """
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--aos', action='store_true', help=f'Test Amiro-OS')
        group.add_argument(
            '--apps', action='store_true', help='Test Amiro-Apps'
        )

    def add_config_args(self):
        """!Arguments related to configuration:
        * Overriding the path to a project or config
        * Generating the conf matrix
        * Using a provided conf matrix
        * Use the replacement conf for execution
        """
        self.parser.add_argument(
            '--project-root',
            help='Set path to project root, (Default: AOS_ROOT | AOS_APPS_ROOT)'
        )
        self.parser.add_argument(
            '--repl-conf',
            help='Set path to replacement config. (Default: AOS_REPLACE_CONF)'
        )
        self.parser.add_argument(
            '--mat-name',
            help=
            'Set name for config matrix (Default: conf_mat.tsv). It is saved to the same directory as the replacement config.'
        )
        self.parser.add_argument(
            '--use-mat', '-m', help='Provide name for matrix to use.'
        )
        self.parser.add_argument(
            '--execute',
            '-e',
            action='store_true',
            help='Execute the test pipeline'
        )

    def parse_args(self, args: list[str]) -> Namespace:
        """!Wires all together and creates all required objects for further processing.
        """
        res: Namespace = self.parser.parse_args(args)
        self.create_path_manager(res)
        self.load_repl_conf(res)
        self.create_build_controller(res)
        self.save_conf_matrix(res)
        self.create_executor()
        self.log_current_configuration()
        self.execute_pipeline(res)
        return res

    def create_path_manager(self, conf: Namespace):
        """!Create the project specific PathManager and overrides the
        default path if provided.
        """
        proj_path = Path(conf.project_root) if conf.project_root else None
        repl_conf = Path(conf.repl_conf) if conf.repl_conf else None
        if conf.aos:
            self.log.info('Aos selected')
            self.p_man = AosPathManager(proj_path, repl_conf=repl_conf)
        elif conf.apps:
            self.log.info('Apps selected')
            self.p_man = AppsPathManager(proj_path, repl_conf=repl_conf)

    def load_repl_conf(self, conf: Namespace):
        """!Load replacement config from given path.
        If no path is provided the default path set by the environment is used.
        """
        self.repl_conf = YamlReplConf(
            Path(conf.repl_conf) if conf.repl_conf else self.p_man.repl_conf
        )

    def create_build_controller(self, conf: Namespace):
        """!Create the Build controller.
        """
        mat = None
        if conf.use_mat:
            self.log.info('Use predefined Matrix')
            mat = pd.read_csv(
                self.p_man.get_conf_mat_path(conf.use_mat), sep='\t', dtype=str
            )
        else:
            self.log.info('Regenerate Matrix')

        self.bc = BuildController(
            self.repl_conf, prebuild_conf_matrix=mat
        )  # type: ignore

    def save_conf_matrix(self, conf: Namespace):
        """!Generate the conf matrix and save it.
        """
        if conf.use_mat:
            self.log.debug('Matrix already provided so it is not saved again!')
            return
        cmat_path = self.p_man.get_conf_mat_path(conf.mat_name)
        self.log.info(f'Dump generated matrix to:\n{cmat_path}')
        cmat = self.bc.generate_config_matrix()
        cmat.to_csv(cmat_path, sep='\t', index=False)

    def create_executor(self):
        self.executor = self.exe_type(self.p_man)  # type: ignore

    def log_current_configuration(self):
        groups = ', '.join(
            self.repl_conf.get_filtered_groups().keys()
        )  # type: ignore
        self.log.info(
            f'''Current Configuration:
    Project Root:\t{self.p_man.root}
    Repl Config:\t{self.p_man.get_repl_conf_path()}
    Config Groups:\t{groups}
        '''
        )

    def execute_pipeline(self, conf: Namespace):
        if not conf.execute:
            self.log.info('Ready to go, use -e to execute the pipeline.')
            return
        self.gcc_version_checker.validate()
        modules = self.bc.iter_c_modules()
        self.executor.build(modules)
