#!/usr/bin/env python3
# This script will download metadata from NCBI PRJNA294416

SLAVEPRJs="slave_bioprojects.txt"
master_bioproject="PRJNA294416"
import os
from subprocess import Popen, PIPE
import shlex
import xml.etree.ElementTree as ET #https://docs.python.org/3.7/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
import pandas as pd
# from collections import defaultdict

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
        print(result_slaveproj)
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
                # print(samn.attrib)
                grandchild_result.update(samn.attrib)
                # print(grandchild_result)
                grandchild_result = pd.DataFrame([grandchild_result])
                # print(grandchild_result)
                # print(grandchild_result)
                results = pd.concat([grandchild_result, results],
                                    ignore_index=True,
                                    sort=False)
                # proc_a = Popen(
                #     shlex.split(f"{cmd1} {link.attrib['accession']}"),
                #     stdout=PIPE)
                # proc_b = Popen(shlex.split(cmd3), stdin=proc_a.stdout,
                #                stdout=PIPE,
                #                stderr=PIPE)

                # result['BioSample'] = samn.attrib['biosample_id']

                # for text in sublink.iter():
                #     print(text)
        #     print(help(grandchild))
            # sys.exit()
            # for docsum in grandchild.findall('DocumentSummary'):
            #     print(docsum.attr)

results.to_csv(SLAVEPRJs)
    # result = pd.DataFrame(result)
    # print(result)
            # print(grandchild.tag)
    # print(projectlinks.tag, projectlinks.attrib)


# for slaveprojects in masterproject.findall('DocumentSummary'):
#     for slaveproject in slaveprojects.iter('ProjectLinks'):
#         print(slaveproject.tag)
    

# print(masterproject)
# for docsum in masterproject:
#     for recordset in docsum:
#         print(recordset.attrib)
#     result = defaultdict(list)
#     result['Master'] = master_bioproject
#     print(projectlink)
#     for project in slaveproject:
#         print(project)
#         result['Title'] = element.attrib('Title')    
#     for element in child.iter('ProjectIDRef'):
#         print(element.attrib['accession'])
#         result['SlaveAccessions'].append(element.attrib['accession'])
#     print(result)
#         print(result)
#         results[]
#         proc1 = Popen(shlex.split(f"{cmd1} {slave_bioproject}"), stdout = PIPE)
#         proc2 = Popen(shlex.split(f"{cmd3}"), stdin=proc1.stdout, stdout=PIPE)
#         root_of_slave = ET.fromstring(proc2.communicate()[0].decode("UTF-8"))
#         for cousin in root_of_slave:
#             for element_slave in cousin.iter('LocusTagPrefix'):
#                 print(element_slave.attrib)


