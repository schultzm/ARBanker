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

results = pd.DataFrame()
cmd1 = "esearch -db BioProject -query"
cmd3 = "efetch -format xml"

proc1 = Popen(shlex.split(f"{cmd1} {master_bioproject}"), stdout=PIPE)
proc3 = Popen(shlex.split(cmd3), stdin=proc1.stdout, stdout=PIPE, stderr=PIPE)
result_masterproj = proc3.communicate()[0].decode("UTF-8")
masterproject = ET.fromstring(result_masterproj)
for child in masterproject:
    result = pd.DataFrame()
    for link in child.iter('ProjectIDRef'):
        # Get the metadata for the slave project
        proc_a = Popen(shlex.split(f"{cmd1} {link.attrib['accession']}"),
                       stdout=PIPE)
        proc_b = Popen(shlex.split(cmd3), stdin=proc_a.stdout, stdout=PIPE,
                       stderr=PIPE)
        result_slaveproj = proc_b.communicate()[0].decode("UTF-8")
        slaveproject = ET.fromstring(result_slaveproj)
        for grandchild in slaveproject:
            title_ = None
            for title in grandchild.iter('Title'):
                title_ = title.text
            for samn in grandchild.iter('LocusTagPrefix'):
                # Add the accessions to the result table
                grandchild_result = {}
                grandchild_result['Title'] = title_
                grandchild_result['SlaveBioProject'] = link.attrib['accession']
                grandchild_result['MasterBioProject'] = master_bioproject
                grandchild_result.update(samn.attrib)
                grandchild_result = pd.DataFrame([grandchild_result])
                results = pd.concat([grandchild_result, results],
                                    ignore_index=True,
                                    sort=False)
                proc_c = Popen(shlex.split(cmd1.replace('BioProject',
                                                        'BioSample') + " " +\
                                           samn.attrib['biosample_id']),
                               stdout=PIPE)
                proc_d = Popen(shlex.split(cmd3), stdin=proc_c.stdout,
                               stdout=PIPE,
                               stderr=PIPE)
                samn_tabl = proc_d.communicate()[0].decode("UTF-8")
                samn_tabl_xml = ET.fromstring(samn_tabl)
                antibiograms = []
                headers = None
                counter = 0
                while counter < 1:
                    for header in samn_tabl_xml.iter('Header'):
                        headers = [colname.text for colname in header.iter('Cell')]
                        counter += 1
                for rown, rowvals in enumerate(samn_tabl_xml.iter('Row')):
                    minidf = pd.DataFrame([dict(zip(headers, [value.text for value in rowvals.iter('Cell')]))])
                    antibiograms.append(minidf)
                antibiogram = pd.concat(antibiograms)
                with open(f"{samn.attrib['biosample_id']}_antibiogram.txt", "w") as abgout:
                    antibiogram.to_csv(abgout, sep = '\t', mode = 'w', index=False)
results.to_csv(SLAVEPRJs)
