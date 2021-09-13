import sys
from amirotest.tools.cli_parser import AmiroParser


if __name__ == '__main__':
    parser = AmiroParser()
    parser.parse_args(sys.argv)
