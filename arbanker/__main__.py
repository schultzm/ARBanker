#!/usr/bin/env python3

"""
This package will download metadata from the
CDC & FDA's AR Isolate Bank.
"""

import pandas as pd
from multiprocessing import Pool, cpu_count
import re
from pathlib import Path
import sys


def getdata(bank_no, outdir):
    """Create an instance of an Isolate() for each bank_no.
       Write out tables from the CDC AR bank for each isolate.
       There will be one table each for:
           - Metadata
           - MIC
           - MMR
    
    Arguments:
        bank_no {int} -- The AR Isolate Bank number
        outdir {PosixPath} -- The output directory as a PosixPath object
    """
    from .utils.isolate import Isolate
    iso = Isolate(bank_no, outdir)
    for table_name in ['Metadata', 'MIC', 'MMR']:
        iso.write_table(table_name)


def main():
    """
    The main routine.
    """

    import argparse
    parser = argparse.ArgumentParser(
        prog='arbanker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser_args1 = argparse.ArgumentParser(add_help=False)
    subparser_args1.add_argument(
        "bank_no",
        help="""CDC AR Isolate Bank number (e.g., 001 or 1)""",
        type=int,
        default=None)
    subparser_args1.add_argument(
        "-o",
        "--output_directory",
        help="Specify path to output results",
        default=Path.home() / 'arbanker_results',
        type = Path,
        required=False
    )

    subparser_modules = parser.add_subparsers(
        title="Sub-commands help", help="", metavar="", dest="subparser_name")
    subparser_modules.add_parser(
        "grab",
        help="""Grab the metadata from the CDC & FDA's AR Isolate bank.""",
        description="Do the web-scraping for a given bank number.",
        parents=[subparser_args1],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparser_modules.add_parser(
        "version", help="Print version.", description="Print version.")
    subparser_modules.add_parser(
        "test", help="Run test suite.",
        description="Run test suite.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    if not args.subparser_name:
        parser.print_help()
    elif args.subparser_name == 'grab':
        getdata(args.bank_no, args.output_directory)
    elif args.subparser_name == 'version':
        from .utils.version import Version
        Version()
    elif args.subparser_name == 'test':
        import unittest
        from .tests.test_suite import suite
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite())




if __name__ == "__main__":
    main()