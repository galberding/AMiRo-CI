from overrides.overrides import overrides
from pandas import DataFrame
import pandas as pd
from abc import ABC
from pathlib import Path

from amirotest.tools.aos_logger import get_logger
from amirotest.tools.record_tags import RecordEntry
log = get_logger(__name__)


class ReportComparator(ABC):
    def __init__(self) -> None:
        self.ignored_labels = [
            RecordEntry.CPU_Time.name,
            RecordEntry.Duration.name,
        ]

    """!Compare two reports with each other.
    """
    def compare(self, report: Path, database: Path):
        """Compare
        """

class NaiveComparator(ReportComparator):

    @overrides
    def compare(self, report: Path, database: Path):
        rep_full = self.load_report(report)
        db_full = self.load_db(database)
        rep = rep_full.drop(labels=self.ignored_labels, axis='columns')
        db = db_full.drop(labels=self.ignored_labels, axis='columns')

        res = {col: [] for col in rep_full.columns} # type: ignore
        for index, row in rep.iterrows():
            if (db==row).all(axis=1).any():
                continue
            for col in rep_full.columns: # type: ignore
                res[col].append(rep_full[col].iloc[index])

        return DataFrame(res)

    def load_report(self, report: Path) -> DataFrame:
        return pd.read_csv(report, sep='\t', dtype=str) # type:ignore

    def load_db(self, db: Path) -> DataFrame:
        return pd.read_csv(report, sep='\t', dtype=str) # type:ignore
