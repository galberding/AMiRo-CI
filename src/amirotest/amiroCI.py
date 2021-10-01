import logging
import sys
from amirotest.tools.aos_logger import get_logger
from amirotest.tools.cli_parser import AmiroParser


if __name__ == '__main__':
    parser = AmiroParser()
    parser.log = get_logger('amiroCI', logging.INFO, out=None)
    parser.parse_args(None)     # type: ignore
