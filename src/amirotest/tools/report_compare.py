from pandas import DataFrame
import pandas as pd
from abc import ABC
from pathlib import Path

from amirotest.tools.aos_logger import get_logger
log = get_logger(__name__, out=f'{__name__}.log')


class ReportComparator(ABC):
    """!Compare two reports with each other.
    """
    def compare(self, report: Path, database: Path):
        """Compare
        """

class NaiveComparator(ReportComparator):

    def compare(self, report: Path, database: Path):

        rep = self.load_report(report)
        db = self.load_db(database)
        log.debug('compared!')
        return DataFrame()

    def load_report(self, report: Path) -> DataFrame:
        return pd.read_csv(report, sep='\t', dtype=str) # type:ignore

    def load_db(self, db: Path) -> DataFrame:
        return pd.read_csv(report, sep='\t', dtype=str) # type:ignore
