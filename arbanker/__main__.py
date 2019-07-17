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
    iso = Isolate(outdir, bank_no=bank_no)
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
        "-o",
        "--output_directory",
        help="Specify path to output results",
        default=Path.home() / 'arbanker_results',
        type = Path,
        required=False
    )
    subparser_args1.add_argument(
        "-r",
        "--resource",
        help="NCBI or AR Isolate Bank",
        choices = ['arbank', 'ncbi'],
        required = True
    )
    subparser_args1.add_argument(
        "-n",
        "--bank_no",
        help="""CDC AR Isolate Bank number (e.g., 0001, 01 or 1)""",
        type=int,
        default=None
    )
    subparser_args1.add_argument(
        "-b",
        "--biosample_no",
        help="Biosample number",
        default=None,
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
        if args.resource == "arbank":
            getdata(args.bank_no, args.output_directory, bank_noargs.bank_no, None)
        elif args.resource == 'ncbi':
            getdata(args.biosample_no, args.output_directory, 0, args.biosample_no)
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