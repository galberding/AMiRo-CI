from amirotest.model.option import AosOption, AosconfOption
from amirotest.tools.search.search_result import GenericSearchResult

class AosconfResult(GenericSearchResult):

    def get_options(self) -> list[AosOption]:
        return self._build_aosconf_options()

    def _build_aosconf_options(self) -> list[AosconfOption]:
        options = []
        for res in self.results:
            options.append(AosconfOption(*res))
        return options
