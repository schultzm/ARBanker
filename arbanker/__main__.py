#!/usr/bin/env python3

"""
The purpose of this package is to download metadata from the
CDC's AR Isolate Bank.
"""

import pandas as pd
from multiprocessing import Pool, cpu_count
import re
from pathlib import Path


def render_table(tabl, label, index_name, bank_n):
    """
    Render the 'tabl' into a pandas df.
    Label the index with 'index_name'
    Write the df to file named 'label'.
    """
    table = list(filter(None, [rw for rw in tabl[1:]]))
    print(table)
    table = pd.DataFrame(table[1:], columns=table[0])
    table[index_name] = bank_n
    cols = [index_name] + [i for i in table.columns if i != index_name]
    table = table[cols]
    table = table.ffill()
    table.to_csv(label, sep='\t', index=False)


def hit_ar(params):
    from .utils.parser import HTMLTableParser # code by https://github.com/schmijos/html-table-parser-python3
    from urllib.request import Request, urlopen

    target, bank_n = params
    bank_n = str("{:03d}".format(bank_n))
    mdata = Path.cwd() / f'../results/Metadata/{bank_n}.tab'
    mic = Path.cwd() / f'../results/MIC/{bank_n}.tab'
    mmr = Path.cwd() / f'../results/MMR/{bank_n}.tab'
    index_name = 'AR Bank'
    # get website content
    req = Request(url=target)
    f = urlopen(req)
    xhtml = f.read().decode('utf-8')
    # instantiate the parser and feed it
    p = HTMLTableParser()
    p.feed(xhtml)
    for index, tabl in enumerate(p.tables[0:3]):
        if index == 0:
            # Add 'species' as a header, filter empty lists and values
            table = [re.sub('(?<=\d) +(?=[A-Z])', '\tSpecies: ', rw[0])
                     for rw in list(filter(None, [list(filter(None, row))
                     for row in tabl]))]
            # split up further
            table = [rw.replace('Positive  Carba', 'Positive\tCarba').
                     replace('Negative  Carba', 'Negative\tCarba')
                     for rw in table]
            # remove hash characters, sub : for , and split on ,
            table = [item.replace(' #', '').replace('\r\n', ':').split('\t')
                     for item in table]
            # Flatten the 2d list
            table = [item for sublist in table for item in sublist]
            # put commas in place, split on comma
            table = [rw.replace(':', '\t').split('\t') for rw in table]
            # Convert 2d to dict
            table = {i[0].strip(): i[1].strip() for i in table if len(i) > 1}
            # Create pd.DataFrame()
            table = pd.DataFrame([table], index=None)
            # mdata = table
            table.to_csv(mdata, sep='\t', index=False)
            # return table
        if index == 1:
            render_table(tabl, mic, index_name, bank_n)
        if index == 2:
            render_table(tabl, mmr, index_name, bank_n)


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

    subparser_modules = parser.add_subparsers(
        title="Sub-commands help", help="", metavar="", dest="subparser_name")
    subparser_modules.add_parser(
        "grab",
        help="""Grab the metadata from the CDC's AR Isolate bank.""",
        description="Start the web-scraping for given bank number.",
        parents=[subparser_args1],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparser_modules.add_parser(
        "version", help="Print version.", description="Print version.")
    subparser_modules.add_parser(
        "depcheck", help="Check dependencies are in path.  Requires Rpy2.",
        description="Check dependencies.")
    subparser_modules.add_parser(
        "test", help="Run test suite.",
        description="Run test suite.",
        parents=[subparser_args1],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    if not args.subparser_name:
        parser.print_help()
    elif args.subparser_name == 'grab':
        numbers = args.bank_no
        print(numbers)
        basetarget = 'https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID='
        targets = (f"{basetarget}{args.bank_no}", args.bank_no)
        hit_ar(targets)
    elif args.subparser_name == 'version':
        from .utils.version import Version
        Version()


if __name__ == "__main__":
    main()