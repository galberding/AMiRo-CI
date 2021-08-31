from amirotest.model.aos_module import AosModule
from amirotest.tools.config_path_finder import ConfigFinder
import re
import json

class BuildReporter:
    def __init__(self, finder: ConfigFinder):
        self.re = re.compile(r'^\[.+\]$')

    def extract_duration(self, stderr: str):
        """!Extract the duration of the compilation which is always in the
        first line.
        It is stored in the format: 'Duration: 25.70021364599961'
        @param strerr string from stderr
        @return time in seconds
        """
        duration = stderr.split('\n')[0]
        description, time = duration.split(':')
        # TODO: Why cast here, do it when saving time!
        return int(float(time))
        # print(stderr)

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
        return [(res['kind'], res['message']) for res in c_res]
