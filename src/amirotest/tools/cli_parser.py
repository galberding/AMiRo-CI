import argparse
from argparse import Namespace
from pathlib import Path
from typing import Optional

from amirotest.tools.config_path_finder import AosPathManager, AppsPathManager, PathManager


class AmiroParser:
    """! Create CLI for configuring and executing the integration pipeline.
    """

    def __init__(self) -> None:
        self.p_man: Optional[PathManager] = None
        self.parser = argparse.ArgumentParser(prog='AmiroCI')
        self.add_project_group()
        self.add_config_args()

    def add_project_group(self):
        """!Add the project type.
        For now `AmiroOS` and `AmiroApps` are supported.
        It is important that this option is set because each project
        requires its own `PathManager`.
        """
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--aos', action='store_true', help=f'Test Amiro-OS')
        group.add_argument('--apps', action='store_true', help='Test Amiro-Apps')

    def add_config_args(self):
        """!Arguments related to configuration:
        * Overriding the path to a project or config
        * Generating the conf matrix
        * Using a provided conf matrix
        * Use the replacement conf for execution
        """
        self.parser.add_argument('--project-root', help='Set path to project root')
        self.parser.add_argument('--repl-conf', help='Set path to replacement config')
        self.parser.add_argument('--gen-mat', help='Generate configuration matrix')

    def parse_args(self, args: list[str]) -> Namespace:
        """!Wires all together and creates all required objects for further processing.
        """
        res: Namespace = self.parser.parse_args(args)
        self.create_path_manager(res)

        return res

    def create_path_manager(self, conf: Namespace):
        """!Create the project specific PathManager and overrides the
        default path if provided.
        """
        proj_path = Path(conf.project_root) if conf.project_root else None
        if conf.aos:
            self.p_man = AosPathManager(proj_path)
        elif conf.apps:
            self.p_man = AppsPathManager(proj_path)
