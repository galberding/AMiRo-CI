"""Test the copy project to RAM functionality.
"""
import logging
import pytest
from pathlib import Path
from amiroci.tools.aos_logger import get_logger
import amiroci.tools.path_manager as PM
# import os
# log = get_logger(__name__, logging.DEBUG)

class MockSHutil:
    def __init__(self):
        self.fr = None
        self.to = None

    def copytree(self, fr, to):
        self.fr = fr
        self.to = to
        print(fr, to)
        return to



@pytest.fixture
def aos_root(tmp_path):
    path = tmp_path / 'Amiro-OS'
    path.mkdir()
    return path

@pytest.fixture
def pm(aos_root):
    """Create AosPathManager, mock path and set logger.
    """
    pam = PM.AosPathManager(aos_root, move_root_to_ram=True)
    return pam


def test_create_file(pm: PM.PathManager):
    """TODO:
    Ugly test, try to mock copytree and rmtree for better testing
    Alternatively use wrapper in PathManager for copy and rm to control
    the behavior with inheritance.
    """
    # pm.copy_root_to_builddir()
    # print()
    assert pm.root.exists()
    assert pm.b_dir == pm.root.parent
