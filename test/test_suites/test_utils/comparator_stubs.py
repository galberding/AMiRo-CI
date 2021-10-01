from pathlib import Path
from overrides.overrides import overrides
from pandas.core.frame import DataFrame
from amirotest.tools.report_compare import NaiveComparator


report_stub = {
    'Module': ['mod1', 'mod1', 'mod1', 'mod1'],
    'Duration': [1, 1, 1, 1],
    'CPU_Time': [1, 1, 1, 1],
    'OPT1': [0, 1, 0, 1],
    'OPT2': [0, 0, 1, 1],
    'Error': [0, 1, 1, 0],
    'ErrorMsg': ['', 'error', 'error2', ''],
    'Warning': [1, 1, 1, 0],
    'WarnMsg': ['warn', 'warn', 'warn', ''],
    'Info': [0, 0, 0, 0],
    'InfoMsg': ['', '', '', ''],
}

db_stub = {
    'Module': ['mod1', 'mod1', 'mod1'],
    'Duration': [1,1,1],
    'CPU_Time': [1,1,1],
    'OPT1': [0, 1, 0],
    'OPT2': [0, 0, 1],
    'Error': [0, 1, 0],
    'ErrorMsg': ['', 'error', ''],
    'Warning': [0, 1, 1],
    'WarnMsg': ['', 'warn', 'warn'],
    'Info': [0, 0, 0],
    'InfoMsg': ['','',''],
}

"""
"""
expected_result = {
    'Module': ['mod1', 'mod1', 'mod1'],
    'Duration': [1, 1, 1],
    'CPU_Time': [1, 1, 1],
    'OPT1': [0, 0, 1],
    'OPT2': [0, 1, 1],
    'Error': [0, 1, 0],
    'ErrorMsg': ['', 'error2', ''],
    'Warning': [1, 1, 0],
    'WarnMsg': ['warn', 'warn', ''],
    'Info': [0, 0, 0],
    'InfoMsg': ['', '', ''],
}

class NaiveComparatorStub(NaiveComparator):
    @overrides
    def load_report(self, report: Path) -> DataFrame:
        return DataFrame(report_stub)

    @overrides
    def load_db(self, db: Path) -> DataFrame:
        return DataFrame(db_stub)
