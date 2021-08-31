from pathlib import Path
from amirotest.controller.build_executer import SerialExecutor
from amirotest.controller.build_reporter import BuildReporter
from amirotest.model.aos_module import AosModule
from ..test_utils.test_helper import PathHelper
import unittest

from amirotest.tools.config_path_finder import AosModuleConfigFinder, AosPathManager
from ..test_utils.build_executer_fake import SerialExecutorFake

class TestReporter(unittest.TestCase):
    def setUp(self):
        self.path_helper = PathHelper()
        self.finder = AosPathManager(self.path_helper.aos_path)
        self.excecutor = SerialExecutorFake(self.finder)
        self.finder = AosModuleConfigFinder(self.path_helper.aos_path)
        self.rep = BuildReporter(self.finder)
        self.model_stub = AosModule(Path('Stub'))
        self.excecutor.build([self.model_stub])
        self.stderr = self.model_stub.build_info.comp_proc.stderr.decode('utf-8')


    def test_duration_extraction(self):
        duration = self.rep.extract_duration(self.stderr)
        self.assertEqual(25, duration)

    def test_get_json_from_compile_str(self):
        res = self.rep.extract_json_str(self.stderr)
        self.assertEqual(
            [self.stderr.split('\n')[113]],
            res
        )

    def test_convert_json_to_dicts(self):
        res = self.rep.convert_json_to_compile_results(
            self.rep.extract_json_str(self.stderr))
        self.assertEqual('error', res[0]['kind'])

    def test_get_compile_state_and_msg(self):
        compile_results = self.rep.convert_json_to_compile_results(
            self.rep.extract_json_str(self.stderr))
        c_info = self.rep.get_state_with_msg(compile_results)
        self.assertEqual(
            [
                ("error", "unknown type name 'SerialCANDriver'"),
                ("error", "unknown type name 'SerialCANConfig'"),
                ("error", "unknown type name 'aos_fbcan_filter_t'"),
            ],
            c_info
        )
