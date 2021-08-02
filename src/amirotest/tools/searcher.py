from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import re
from typing import Any

from amirotest.model import AosModule
from amirotest.tools.config_path_finder import ConfigFinder



class Searcher(ABC):

    def __init__(self) -> None:
        self.regex_options = re.VERBOSE | re.MULTILINE

    @abstractmethod
    def search_options(self, module : ConfigFinder) -> list[Any]:
        """Search options by the paths provided in the module."""

    def _search_with_regex(self, path: Path, regex: re.Pattern) -> list[Any]:
        with path.open() as make:
            content = make.read()
            res =  regex.findall(content)
            return res
