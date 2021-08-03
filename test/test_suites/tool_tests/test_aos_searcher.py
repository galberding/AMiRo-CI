from amirotest.model.option import AosOption, GlobalOption
from amirotest.model.search_result import GenericSearchResult
from ..test_utils.test_helper import PathHelper
import unittest

from amirotest.tools import AosConfSearcher, SearchGroupIdx
from amirotest.tools.config_path_finder import AosConfigFinder


class TestAosSearcher(unittest.TestCase):
    def setUp(self) -> None:
        self.path_helper = PathHelper()
        self.conf_finder = AosConfigFinder(self.path_helper.get_aos_module_path())
        self.searcher = AosConfSearcher()


    def test_get_options_returns_default_options(self):
        pass
        # res = self.get_options()

    # def test_search_aosconf(self):
    #     res = self.get_options()
    #     self.assertEqual(len(res), 27)
    #     # Ensure that results contain the str OS_CONF and AMIROOS_CFG
    #     # are at the right index
    #     self.assertIn(
    #         SearchGroupIdx.OS_CFG.name,
    #         res[0][SearchGroupIdx.OS_CFG.value]
    #     )
    #     self.assertIn(
    #         SearchGroupIdx.AMIROOS_CFG.name,
    #         res[0][SearchGroupIdx.AMIROOS_CFG.value]
    #     )

    # def get_options(self) -> list[AosOption]:
    #     res = self.searcher.search_options(self.conf_finder)
    #     res = res.get_options()
    #     return res


    # Ensure default options are returned
    #
