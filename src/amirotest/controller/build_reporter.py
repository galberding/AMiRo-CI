from enum import Enum, auto
from amirotest.model.aos_module import AosModule
from amirotest.tools.config_path_finder import ConfigFinder
import re
import json
import pandas as pd

class RecordEntry(Enum):
    Module = auto()
    Duration = auto()
    Default = '-'


class GccMsg(Enum):
    kind = auto()
    message = auto()

class BuildReporter:
    """!Parse the compiler output and store the information in the
    report tsv.

    \note If the processed modules do not have a BuildInfo an
    exception is risen.
    """
    def __init__(self, finder: ConfigFinder):
        self.re = re.compile(r'^\[.+\]$')
        self.record = pd.DataFrame()
        self.record_init()

    def record_init(self):
        """!Set the first columns with Module and Duration.
        """
        self.record_insert_col(RecordEntry.Module.name)
        self.record_insert_col(RecordEntry.Duration.name)

    def record_module(self, module: AosModule):
        self.record_create_empty_row()


    def record_set_tail_entry(self, col: str, value: str):
        """!Insert value at the end of the record.
        \note
        If the column does not exists it is created.
        @param col column name
        @param value
        """
        if col not in self.record:
            self.record_insert_col(col)
        self.record[col].iloc[-1] = value

    def record_insert_col(self, col: str):
        self.record[col] = RecordEntry.Default.name

    def record_create_empty_row(self):
        """!Insert row to record.
        The default value for all entries in the row is set to '-'
        """
        self.record.loc[len(self.record.index)] = \
            [RecordEntry.Default.value] * len(self.record.columns)


    def extract_json_str(self, stderr: str) -> list[str]:
        """!Extract compile results.
        """
        results = []
        for line in stderr.split('\n'):
            if self.re.match(line):
                results.append(line)
        return results

    def convert_json_to_compile_results(self, json_res: list[str]) -> list[dict[str, str]]:
        res = []
        for jres in json_res:
            res += json.loads(jres)
        return res

    def get_state_with_msg(self, c_res: list[dict[str, str]]) -> list[tuple[str, str]]:
        """!If error, warning or info is reported by the compiler those are contained
        in the c_res / converted dictionaries.
        For easier processing only the kind of error and the message is extracted
        to save for the final report.
        @param c_res compiler results in for of dictionaries
        @return tuples of kinds and messages
        """
        return [(res[GccMsg.kind.name], res[GccMsg.message.name]) for res in c_res]
