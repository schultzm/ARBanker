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

def hit_ar(params):
    target, bank_n = params
    print(target, bank_n)
    # get website content
    req = urllib.request.Request(url=target)
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')
    # print(xhtml)

    # instantiate the parser and feed it
    p = HTMLTableParser()
    p.feed(xhtml)
    bank = None
    mdata = None
    mic = None
    mmr = None
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
            table = {i[0].strip(): i[1].strip() for i in table}
            # Create pd.DataFrame()
            table = pd.DataFrame([table], index=None)
            print()
            # mdata = table
            outpath = pathlib.Path(f'../scraped/Metadata/')
            print(outpath)

            # table.to_csv(, sep='\t')
            # return table
        if index == 1:
            table = list(filter(None, [rw for rw in tabl[1:]]))
            table = pd.DataFrame(table[1:], columns=table[0])
            mic = table
        if index == 2:
            table = list(filter(None, [rw for rw in tabl[1:]]))
            table = pd.DataFrame(table[1:], columns=table[0])
            mmr = table

    df_final = pd.concat(df_result, axis=1)
    df_final = df_final.ffill()
    print(df_final)
    # for i in df_final.columns:
    #     df_final = df_final.ffill() 
    #     # df_final[i]
    # df.loc[df.date=='','date'] = np.nan
    # print(pd.concat(df_result, axis=1))
from parser import HTMLTableParser
import urllib.request
numbers = pd.read_csv("ARnumbers.tab", sep="\t", header=0, index_col=1)
print(numbers)
basetarget = 'https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID='
targets = [(f"{basetarget}{i}", i) for i in numbers.BANK]
# pool = Pool(2)
results = Pool(cpu_count()).map(hit_ar, targets)
# print(results)
import sys
sys.exit()



# results = pd.DataFrame()
# cmd1 = "esearch -db BioProject -query"
# cmd3 = "efetch -format xml"

# proc1 = Popen(shlex.split(f"{cmd1} {master_bioproject}"), stdout=PIPE)
# proc3 = Popen(shlex.split(cmd3), stdin=proc1.stdout, stdout=PIPE, stderr=PIPE)
# result_masterproj = proc3.communicate()[0].decode("UTF-8")
# masterproject = ET.fromstring(result_masterproj)
# for child in masterproject:
#     result = pd.DataFrame()
#     for link in child.iter('ProjectIDRef'):
#         # Get the metadata for the slave project
#         proc_a = Popen(shlex.split(f"{cmd1} {link.attrib['accession']}"),
#                        stdout=PIPE)
#         proc_b = Popen(shlex.split(cmd3), stdin=proc_a.stdout, stdout=PIPE,
#                        stderr=PIPE)
#         result_slaveproj = proc_b.communicate()[0].decode("UTF-8")
#         slaveproject = ET.fromstring(result_slaveproj)
#         for grandchild in slaveproject:
#             title_ = None
#             for title in grandchild.iter('Title'):
#                 title_ = title.text
#             for samn in grandchild.iter('LocusTagPrefix'):
#                 # Add the accessions to the result table
#                 grandchild_result = {}
#                 grandchild_result['Title'] = title_
#                 grandchild_result['SlaveBioProject'] = link.attrib['accession']
#                 grandchild_result['MasterBioProject'] = master_bioproject
#                 grandchild_result.update(samn.attrib)
#                 grandchild_result = pd.DataFrame([grandchild_result])
#                 results = pd.concat([grandchild_result, results],
#                                     ignore_index=True,
#                                     sort=False)
#                 proc_c = Popen(shlex.split(cmd1.replace('BioProject',
#                                                         'BioSample') + " " +\
#                                            samn.attrib['biosample_id']),
#                                stdout=PIPE)
#                 proc_d = Popen(shlex.split(cmd3), stdin=proc_c.stdout,
#                                stdout=PIPE,
#                                stderr=PIPE)
#                 samn_tabl = proc_d.communicate()[0].decode("UTF-8")
#                 # print(samn_tabl)
#                 samn_tabl_xml = ET.fromstring(samn_tabl)
#                 panel_id = None # the CDC Panel isolate number
#                 strain = None # the CDC AR number



#                 for attributes_ in samn_tabl_xml.iter("Attribute"):
#                     if "panel_id" in attributes_.attrib.values():
#                         panel_id = attributes_.text
#                     elif "strain" in attributes_.attrib.values():
#                         strain = attributes_.text
#                 antibiograms = []
#                 headers = None
#                 counter = 0
                

#                     # tabl_part = [row for row in tabl if 0<len(row)]
#                     # print(tabl_part)
#                     # for row in tabl:
#                         # print(len(row), row)
#                     # print(tabl[1:])
#                 # print(p.tables[0])
#                 # print(help(HTMLTableParser))
#                 # tables = pd.read_html("", match="table")
#                 # print(tables[0])  

#                 # table = ET.fromstring(s)
#                 # rows = iter(table)
#                 # headers = [col.text for col in next(rows)]
#                 # for row in rows:
#                 #     values = [col.text for col in row]
#                 #     print(dict(zip(headers, values)))

#                 while counter < 1:
#                     for header in samn_tabl_xml.iter('Header'):
#                         headers = [colname.text for colname in header.iter('Cell')]
#                         counter += 1
#                 for rown, rowvals in enumerate(samn_tabl_xml.iter('Row')):
#                     minidf = pd.DataFrame([dict(zip(headers, [value.text for value in rowvals.iter('Cell')]))])
#                     antibiograms.append(minidf)
#                 antibiogram = pd.concat(antibiograms)
#                 with open(f"{samn.attrib['biosample_id']}_antibiogram.txt", "w") as abgout:
#                     antibiogram.to_csv(abgout, sep = '\t', mode = 'w', index=False)
# results.to_csv(SLAVEPRJs)
