from pathlib import Path
from unittest.case import skip
from amirotest.controller.build_executer import SerialExecutor
from amirotest.controller.build_reporter import BuildReporter, RecordEntry
from amirotest.model.aos_module import AosModule
from amirotest.model.option.aos_opt import AosOption, AosVariable
from ..test_utils.test_helper import PathHelper
import unittest

from amirotest.tools.config_path_finder import  AosPathManager
from ..test_utils.build_executer_fake import SerialExecutorFake

class TestReporter(unittest.TestCase):
    def setUp(self):
        self.path_helper = PathHelper()
        self.finder = AosPathManager(self.path_helper.aos_path)
        self.excecutor = SerialExecutorFake(self.finder)
        # self.finder = AosModuleConfigFinder(self.path_helper.aos_path)
        self.rep = BuildReporter(self.finder)
        self.module_stub = AosModule(Path('Stub'))
        self.excecutor.build([self.module_stub])
        self.stderr = self.module_stub.build_info.comp_proc.stderr.decode('utf-8')


    def test_convert_json_to_dicts(self):
        res = self.rep.convert_json_to_compile_results(
            self.rep.extract_json_str(self.stderr))
        self.assertEqual('note', res[0]['kind'])

    def test_get_compile_state_and_msg(self):
        compile_results = self.rep.convert_json_to_compile_results(
            self.rep.extract_json_str(self.stderr))
        c_info = self.rep.get_state_with_msg_from_results(compile_results)
        self.assertEqual(
            [
                ('note', 'info'),
                ('warning', 'warning'),
                ("error", "unknown type name 'SerialCANDriver'"),
                ("error", "unknown type name 'SerialCANConfig'"),
                ("error", "unknown type name 'aos_fbcan_filter_t'"),
            ],
            c_info
        )

    def test_record_init(self):
        self.assertIn(RecordEntry.Module.name, self.rep.record)
        self.assertIn(RecordEntry.Duration.name, self.rep.record)
        self.assertIn(RecordEntry.CPU_Time.name, self.rep.record)

    def test_record_create_empty_entry(self):
        prelen = len(self.rep.record.index)
        self.rep.record_create_empty_row()
        postlen = len(self.rep.record.index)
        self.assertGreater(postlen, prelen)

    def test_record_indsert_col_if_not_existing(self):
        col = 'test'
        self.rep.record_insert_col(col)
        self.assertIn(col, self.rep.record)

    def test_record_set_tail_value(self):
        self.check_record_tail_set(RecordEntry.Module.name, 'Module Name')

    def test_record_set_value_of_unknown_column(self):
        col, value = 'Unknown Col', 'True'
        self.check_record_tail_set(col, value)

    def test_record_module_name_duration(self):
        self.rep.record_module(self.module_stub)
        self.check_record_tail(RecordEntry.Module.name, str(self.module_stub.name))
        self.check_record_tail(RecordEntry.Duration.name, str(self.module_stub.build_info.duration))

    def test_record_module_options(self):
        self.module_stub.add_options([AosOption('PARAM1', 'True')])
        self.rep.record_module(self.module_stub)
        self.check_record_tail('PARAM1', 'True')

    def test_record_module_exclude_variables(self):
        self.module_stub.add_options(
            [AosOption('PARAM1', '$(VAR)'),
             AosVariable('VAR', 'True')])
        self.module_stub.resolve()
        self.rep.record_module(self.module_stub)
        self.check_record_tail('PARAM1', 'True')
        self.assertNotIn('VAR', self.rep.record)

    # @skip('Not implemented')
    def test_record_state_state(self):
        self.rep.record_module(self.module_stub)
        self.check_record_tail(RecordEntry.Error.name, 3)
        self.check_record_tail(RecordEntry.Warning.name, 1)
        self.check_record_tail(RecordEntry.Info.name, 1)


    # @skip('Not implemented')
    def test_record_error_messages(self):
        self.rep.record_module(self.module_stub)
        self.check_record_tail(RecordEntry.ErrorMsg.name, ', '.join(
            [
                "unknown type name 'SerialCANDriver'",
                "unknown type name 'SerialCANConfig'",
                "unknown type name 'aos_fbcan_filter_t'",
            ]
        ))

        self.check_record_tail(RecordEntry.WarnMsg.name, ', '.join(['warning']))
        self.check_record_tail(RecordEntry.InfoMsg.name, ', '.join(['info']))
        # self.check_record_tail(RecordEntry.Error.name, str(3))

    def test_reformat_compiler_state(self):
        c_state_msg = [
            (RecordEntry.Error.value, 'msg1'),
            (RecordEntry.Error.value, 'msg2'),
            (RecordEntry.Warning.value, 'msg3'),
            (RecordEntry.Info.value, 'msg4'),
        ]

        msg_states = self.rep.build_compiler_state_dict(c_state_msg)
        self.assertEqual(2, msg_states[RecordEntry.Error.value][RecordEntry.Error.value])
        self.assertEqual(1, msg_states[RecordEntry.Warning.value][RecordEntry.Warning.value])
        self.assertEqual(1, msg_states[RecordEntry.Info.value][RecordEntry.Info.value])

    def check_record_tail_set(self, col, value):
        # print(self.rep.record)
        self.rep.record_create_empty_row()
        self.rep.record_set_tail_entry(col, value)
        self.check_record_tail(col, value)

    def check_record_tail(self, col, value):
        self.assertEqual(value, self.rep.record[col].iloc[-1])
