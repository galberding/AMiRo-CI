from pathlib import Path
from ..test_utils.comparator_stubs import NaiveComparatorStub
from unittest import TestCase
from unittest.case import skipIf

from amirotest.tools.report_compare import NaiveComparator


class TestNaiveReportComparator(TestCase):
    def setUp(self) -> None:
        self.comp = NaiveComparatorStub()

    def test_init(self):
        df = self.comp.compare(Path(''), Path(''))
        self.assertEqual(1, df.shape[0])
