from enum import Enum, auto
import re
import subprocess


class GccVersion(Enum):
    major = 0
    minor = 1
    bug = 2

class WrongGccVersion(Exception):
    def __init__(self, major, minor, bug, msg) -> None:
        super().__init__(f'Detected version: {major}.{minor}.{bug}\n{msg}')

class GccVersionChecker:
    """!Extract the current arm gcc version and raise an error if
    the detected version is too low.
    """
    def __init__(self) -> None:
        self.regex = re.compile(fr'gcc\sversion\s(?P<major>\d+)\.(?P<minor>\d+)\.(?P<bug>\d+)')

    def validate(self) -> bool:
        """!Perform the version check.
        If the version is insufficient an error is raised.
        """
        version_str = self.get_version_string()
        version = self.get_version(version_str)
        self.check_version(version)
        return True

    def get_version_string(self) -> str:
        """!Capture and decode gcc version info.
        @return decoded version info
        """
        process = subprocess.run(['arm-none-eabi-gcc', '-v'], capture_output=True)
        return process.stderr.decode('utf-8')

    def get_version(self, version_str: str) -> tuple[int, int, int]:
        """!Extract the version number from the provided version string
        with regex.
        @param version_str
        @return version number (major, minor, bug)
        """
        version = self.regex.search(version_str)
        return int(version.group(GccVersion.major.name)), \
            int(version.group(GccVersion.minor.name)),\
            int(version.group(GccVersion.bug.name))

    def check_version(self, version: tuple[int, int, int]):
        """!Check if current version matches the requirements.
        Raise error if any condition fails.
        @param version number
        """
        if version[GccVersion.major.value] < 9:
            raise WrongGccVersion(*version, f'Version to low requires at least 9 or higher!')
