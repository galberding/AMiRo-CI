from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type

from amirotest.model.option import AosOption


@dataclass
class GenericSearchResult(ABC):
    results: list[Any]

    @abstractmethod
    def get_options(self) -> list[AosOption]:
        """Return options"""

    def _build_generic_options(self, opt_type: Type[AosOption]) -> list[AosOption]:
        options = []
        for option_name, option_args in self.results:
            options.append(opt_type(option_name, option_args))
        return options


class SearchResult(GenericSearchResult):
    def __init__(self, results: list[Any], opt_type: Type[AosOption]):
        self.opt_type = opt_type
        super().__init__(results)

    def get_options(self) -> list[AosOption]:
        return self._build_generic_options(self.opt_type)
