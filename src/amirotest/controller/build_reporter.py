from enum import Enum, auto
import subprocess
from typing import Union
from amirotest.model.aos_module import AosModule
from amirotest.model.option.aos_opt import AosVariable, ConfVariable
from amirotest.tools.config_path_finder import PathManager
import re
import json
import pandas as pd

class RecordEntry(Enum):
    Module = auto()
    Duration = auto()
    CPU_Time = auto()
    Default = '-'
    CompilerState = auto()
    Message = auto()
    Error = 'error'
    Warning = 'warning'
    Info = 'note'
    ErrorMsg  = auto()
    WarnMsg = auto()
    InfoMsg = auto()

class GccMsg(Enum):
    kind = auto()
    message = auto()

class BuildReporter:
    """!Parse the compiler output and store the information in the
    report tsv.

    \note If the processed modules do not have a BuildInfo an
    exception is risen.
    """
    def __init__(self, finder: PathManager):
        self.re = re.compile(r'^\[.+\]$')
        self.record = pd.DataFrame()
        self.record_init()
        self.finder = finder


    def record_init(self):
        """!Set the first columns with Module and Duration.
        """
        self.record_insert_col(RecordEntry.Module.name)
        self.record_insert_col(RecordEntry.Duration.name)
        self.record_insert_col(RecordEntry.CPU_Time.name)

    def record_module(self, module: AosModule):
        """!Record all interesting values to the record.
        """
        self.record_create_empty_row()
        self.record_general_infos(module)
        self.record_options(module)
        self.record_compiler_state(module)

    def record_general_infos(self, module: AosModule):
        """!Record module name, build and cpu time.
        """
        self.record_set_tail_entry(RecordEntry.Module.name, module.name)
        self.record_set_tail_entry(RecordEntry.Duration.name, str(module.build_info.duration))
        self.record_set_tail_entry(RecordEntry.CPU_Time.name, str(module.build_info.cpu_time))

    def record_create_empty_row(self):
        """!Insert row to record.
        The default value for all entries in the row is set to '-'
        """
        self.record.loc[len(self.record.index)] = \
            [RecordEntry.Default.value] * len(self.record.columns)

    def record_save(self):
        self.record.to_csv(self.finder.get_report_config(), sep='\t')


    def record_options(self, module: AosModule):
        """!Iterate over module option and insert their values into the record.
        \note
        AosVariable is ignored ignored and not written to the record.
        """
        for option in module.options:
            # print(type(option))
            if isinstance(option, AosVariable):
                continue
            if len(option.args) > 1:
                raise NotImplementedError('Unclear what to do with multiple arguments!')
            self.record_set_tail_entry(option.name, option.args[0].name)

    def record_compiler_state(self, module: AosModule):
        """!Set Compiler state entries in the record.
        This includes the following entries in the given order:
        Error, Warning, Info, ErrorMsg, WarningMsg, InfoMsg
        """
        c_state_msgs = self.build_state_msg_pairs_from_compiler_output(module.build_info.comp_proc)

        state_dict = self.build_compiler_state_dict(c_state_msgs)
        self.record_set_tail_entry(
            RecordEntry.Error.name,
            state_dict[RecordEntry.Error.value][RecordEntry.Error.value])
        self.record_set_tail_entry(
            RecordEntry.ErrorMsg.name,
            ', '.join(state_dict[RecordEntry.Error.value][RecordEntry.Message])
        )
        self._set_compiler_state_entry_for(RecordEntry.Error, RecordEntry.ErrorMsg, state_dict)
        self._set_compiler_state_entry_for(RecordEntry.Warning, RecordEntry.WarnMsg, state_dict)
        self._set_compiler_state_entry_for(RecordEntry.Info, RecordEntry.InfoMsg, state_dict)

    def _set_compiler_state_entry_for(self, rec: RecordEntry, rec_msg: RecordEntry, state_dict: dict):
        """!Helper method to set the parameter from the state dict to
        the record.
        """
        self.record_set_tail_entry(
            rec.name,
            state_dict[rec.value][rec.value])
        self.record_set_tail_entry(
            rec_msg.name,
            ', '.join(state_dict[rec.value][RecordEntry.Message])
        )

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

    def build_state_msg_pairs_from_compiler_output(self, proc: subprocess.CompletedProcess) -> list[tuple[str, str]]:
        """!Process the output captured during the compilation.
        The compiler is instructed to write all output into json format to stderr.
        This is captured, decoded and extracted to json strings.
        Those are transformed to dictionaries where the actual compiler state is
        read in for of error kind and message.
        @param proc process with recorded stdout and stderr
        @return list of tuples containing error type and message.
        """
        stderr = proc.stderr.decode('utf-8')
        json_res = self.extract_json_str(stderr)
        c_res = self.convert_json_to_compile_results(json_res)
        return self.get_state_with_msg_from_results(c_res)

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

    def get_state_with_msg_from_results(self, c_res: list[dict[str, str]]) -> list[tuple[str, str]]:
        """!If error, warning or info is reported by the compiler those are contained
        in the c_res / converted dictionaries.
        For easier processing only the kind of error and the message is extracted
        to save for the final report.
        @param c_res compiler results in for of dictionaries
        @return tuples of kinds and messages
        """
        return [(res[GccMsg.kind.name], res[GccMsg.message.name]) for res in c_res]


    def build_compiler_state_dict(self, c_state_msg: list[tuple[str, str]]):
        states = {
            RecordEntry.Error.value: {RecordEntry.Error.value: 0,
                                      RecordEntry.Message: []},
            RecordEntry.Warning.value: {RecordEntry.Warning.value: 0,
                                        RecordEntry.Message: []},
            RecordEntry.Info.value: {RecordEntry.Info.value: 0,
                                     RecordEntry.Message: []}
        }

        for kind, msg in c_state_msg:
            states[kind][kind] += 1
            states[kind][RecordEntry.Message].append(msg)

        # print(c_state_msg)
        return states
