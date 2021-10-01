from pathlib import Path

from pandas import DataFrame

from amirotest.tools.aos_logger import get_logger
from ..test_utils.comparator_stubs import NaiveComparatorStub, expected_result
from unittest import TestCase
from unittest.case import skipIf

from amirotest.tools.report_compare import NaiveComparator

log = get_logger(__name__)


class TestNaiveReportComparator(TestCase):
    def setUp(self) -> None:
        self.comp = NaiveComparatorStub()

    def test_init(self):
        df = self.comp.compare(Path(''), Path(''))
        self.assertTrue(DataFrame(expected_result).equals(df))
        # self.assertIn(DataFrame(expected_result), df)
