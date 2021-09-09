import argparse
from argparse import Namespace
from typing import Optional

from amirotest.tools.config_path_finder import AosPathManager, AppsPathManager, PathManager


class AmiroParser:
    def __init__(self) -> None:
        self.p_man: Optional[PathManager] = None
        self.parser = argparse.ArgumentParser(prog='AmiroCI')
        self.add_project_group()

    def add_project_group(self):
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--aos', action='store_true', help='Test Amiro-OS')
        group.add_argument('--apps', action='store_true', help='Test Amiro-Apps')

    def parse_args(self, args: list[str]) -> Namespace:
        res: Namespace = self.parser.parse_args(args)
        self.create_path_manager(res)
        return res

    def create_path_manager(self, conf: Namespace):
        if conf.aos:
            self.p_man = AosPathManager()
        elif conf.apps:
            self.p_man = AppsPathManager()
