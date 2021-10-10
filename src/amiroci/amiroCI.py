import logging
import sys
from amiroci.tools.aos_logger import get_logger
from amiroci.tools.cli_parser import AmiroParser
import cProfile
import pstats


def main():
    with cProfile.Profile() as pr:
        parser = AmiroParser()
        parser.log = get_logger('amiroCI', logging.INFO, out=None)
        parser.parse_args(None)  # type: ignore

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='logs/amiroci.prof')


if __name__ == '__main__':
    main()
