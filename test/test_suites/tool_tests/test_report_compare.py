import logging
from pathlib import Path

from pandas import DataFrame

from amiroci.tools.aos_logger import get_logger
from ..test_utils.comparator_stubs import NaiveComparatorStub, expected_result
from unittest import TestCase
from unittest.case import skipIf

from amiroci.tools.report_compare import NaiveComparator

log = get_logger(__name__, logging.WARN)


class TestNaiveReportComparator(TestCase):
    def setUp(self) -> None:
        self.comp = NaiveComparatorStub()
        self.comp.log.setLevel(logging.DEBUG)

    def test_native_comapre(self):
        df = self.comp.compare(Path(''), Path(''))
        self.assertTrue(DataFrame(expected_result).equals(df))
        log.debug(df.to_string())
        # self.assertIn(DataFrame(expected_result), df)

    # def test_
