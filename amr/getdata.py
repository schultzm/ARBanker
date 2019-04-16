#!/usr/bin/env python3
# This script will download metadata from NCBI PRJNA294416

SLAVEPRJs="slave_bioprojects.txt"
master_bioproject="PRJNA294416"
import os
from subprocess import Popen, PIPE
import shlex
import xml.etree.ElementTree as ET #https://docs.python.org/3.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
import pandas as pd
from collections import defaultdict
from multiprocessing import Pool, cpu_count
import re
from pathlib import Path

def render_table(tabl, label, index_name):
    """
    Render the 'tabl' into a pandas df.
    Label the index with 'index_name'
    Write the df to file named 'label'.
    """
    table = list(filter(None, [rw for rw in tabl[1:]]))
    table = pd.DataFrame(table[1:], columns=table[0])
    table[index_name] = bank_n
    cols = [index_name] + [i for i in table.columns if i != index_name]
    table = table[cols]
    table = table.ffill()
    table.to_csv(label, sep='\t', index=False)



def hit_ar(params):
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
                     for rw in list(filter(None, [list(filter(None, row)) for row in tabl]))]
            # split up further
            table = [rw.replace('Positive  Carba', 'Positive\tCarba').replace('Negative  Carba', 'Negative\tCarba') for rw in table]
            # print(table)
            # remove hash characters, sub : for , and split on ,
            table = [item.replace(' #', '').replace('\r\n', ':').split('\t') for item in table]
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
            render_table(tabl, mic, index_name)
        if index == 2:
            render_table(tabl, mmc, index_name)

if __name__ == "__main__":
    from parser import HTMLTableParser # code by https://github.com/schmijos/html-table-parser-python3
    from urllib.request import Request, urlopen
    numbers = pd.read_csv("ARnumbers.tab", sep="\t", header=0, index_col=1)
    print(numbers)
    basetarget = 'https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID='
    targets = [(f"{basetarget}{i}", i) for i in numbers.BANK]
    Pool(cpu_count()).map(hit_ar, targets)
