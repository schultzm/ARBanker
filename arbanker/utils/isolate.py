from pathlib import Path
import pandas as pd
import re
import sys
from subprocess import Popen, PIPE
import shlex


class Isolate:
    basetarget = "https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID="
    def __init__(self, outdir, resource, resource_no):
        """Intialise the Isolate.
        
        Arguments:
            bank_no {int} -- The AR Isolate Bank item number.
            outdir {PosixPath} -- Destination folder for results.
        """
        self.resource = resource
        if self.resource == 'arbank':
            self.resource_no = str("{:04d}".format(int(resource_no)))
            self.target    = f"{self.basetarget}{self.resource_no}"
        elif self.resource == 'ncbi':
            self.resource_no = resource_no
        self.outdir    = outdir
        self.outfile   =  f"{self.resource_no}.tab"
        self.mdata_name = "Metadata"
        self.mic_name   = "MIC" 
        self.mmr_name   = "MMR"
        self.index_name = "AR Bank"
    
    def hit_xml(self):
        """Query the CDC webpage and return the table.
        
        Returns:
            dict -- {'Name of table': 'table'}.
        """
        from .parser import HTMLTableParser # code by https://github.com/schmijos/html-table-parser-python3
        xhtml = None
        if self.resource == 'ncbi':
#             cmd = f"esearch -db biosample -query {self.resource_no}"
#             cmd2 = f"efetch -format xml"
#             proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
#             proc2 = Popen(shlex.split(cmd), stdin=proc.stdout, stdout=PIPE, stderr=PIPE)
            from Bio import Entrez
            Entrez.email = "mark.schultz@unimelb.edu.au"
            handle = Entrez.efetch(db="biosample", id=self.resource_no, retmode="xml")
            xml = '\n'.join(list(filter(None, [i.rstrip('\n') for i in handle.readlines()])))
            xml = xml.replace('><', '>\n<').replace('> ', '>\n ')
            print(xml)
            # print(xml[0:1000])
            # from defusedxml.ElementTree import fromstring
            from defusedxml import ElementTree as ET
            root = ET.fromstring(xml)
            print(root)
            # headers = [cell.text for cell in header.iter('Cell') for header in root.iter('Table')]
            # print(headers)
            # print([[j.text for j in i.getchildren()] for i in root[0][1][2][0].getchildren()[1: 3]])

            # # print('root.tag', root.tag)
            # table = root.iter('Table')
            # # print(dir(ET))
            headers = []
            rows = []
            for header in root.iter('Header'):
                for cell in header.iter('Cell'):
                    headers.append(cell.text)
            for row in root.iter('Row'):
                cells = [cell.text for cell in row.iter('Cell')]
                rows.append(cells)
            import pandas as pd
            # rows = list(zip(rows))
            print(rows)
            df = pd.DataFrame(rows, columns = headers)
            print(df.to_csv())
            # print(rows)
                # for grandchild in child.iter('table'):
                #     print(grandchild.tag, grandchild.attrib)
            # print('root', elementtree)
            # print('roottag', elementtree.tag)
            # print('rootattrib', elementtree.attrib)
            # print('elementtree', elementtree)
            # for child in elementtree.getchildren():
            #     print('child', child)
            #     print('attrib', child.attrib)
            #     print('tag', child.tag)
                # for infant in child.getchildren():
                #     print(infant)
                # for child in header.getchildren():
                #     for comment in child.findall('Comment'):
                #         for table in comment.getchildren():
                #             for header2 in table.findall('Header'):
                #                 print(header2.getroot())
            # for child in et.iter('Antibiogram'):
            #     print(child.tag, child.attrib)
#             print(xhtml)
#             print(handle)
#             records = Entrez.read(handle, validate=False)
#             print(list(records))
#                 print(record)
            import sys
            sys.exit()
#             print(records)
#             for record in records:
#                 print(record)
#             # each record is a Python dictionary or list.
#                 print(record)
#                 print(proc2)
#             result = proc2.communicate()
#             print(result)
#             xhtml = None
        else:
            from urllib.request import Request, urlopen
            # get website content
            req = Request(url=self.target)
            f = urlopen(req)
            xhtml = f.read().decode('utf-8')
        # instantiate the parser and feed it
        p = HTMLTableParser()
        p.feed(xhtml)
        print(p.rawdata)
#         return {"Metadata": p.tables[0],
#                 "MIC": p.tables[1],
#                 "MMR": p.tables[2]}
    

    def render_metadatatable(self, tabl):
        """Formatter method for a metadata table.
        
        Arguments:
            tabl {list} -- A list of lists (i.e., a 2d list).
        
        Returns:
            pandas.core.frame.DataFrame -- A pandas dataframe.
        """
        # Add 'species' as a header, filter empty lists and values
        table = [re.sub("(?<=\d) +(?=[A-Z])", "\tSpecies: ", rw[0])
                    for rw in list(filter(None, [list(filter(None, row))
                    for row in tabl]))]
        # split up further
        table = [rw.replace('Positive  Carba', 'Positive\tCarba').
                    replace('Negative  Carba', 'Negative\tCarba').
                    replace('Sequence Accession', 'Biosample Accession')
                    for rw in table]
        # remove hash characters, sub : for , and split on ,
        table = [item.replace(' #', '').replace('\r\n', ':').split('\t')
                    for item in table]
        # Flatten the 2d list
        table = [item for sublist in table for item in sublist]
        table = [rw.replace(':', '\t').split('\t') for rw in table]
        # Convert 2d to dict
        table = {i[0].strip(): i[1].strip() for i in table if len(i) > 1 and len(i[1].strip()) > 0}
        table = pd.DataFrame([table], index=None)
        return table

    def render_datatable(self, tabl):
        """Formatter method for data table.
        
        Arguments:
            tabl {list} -- A list of lists (i.e., a 2d list).
        
        Returns:
            pandas.core.frame.DataFrame -- A pandas dataframe.
        """
        table = list(filter(None, [rw for rw in tabl[1:]]))
        nheaders = len(table[0])
        data = [tabl for tabl in table[1:] if len(tabl) == nheaders] 
        table = pd.DataFrame(data, columns=table[0])
        # replace the artifact spaces from interpreting bold HTML text 
        table = table.applymap(lambda x: x.replace(" ,", ","). \
                                           replace(", ", ","))
        if 'Drug' in table.columns:
            # Replace the footnote markers with ''
            table.Drug = table.Drug.apply(lambda x: re.sub(' [0-9]$', '', x))
        table[self.index_name] = self.resource_no
        cols = [self.index_name] + \
               [i for i in table.columns.tolist() if i != self.index_name]
        table = table[cols]
        table = table.ffill()
        return table


    def write_table(self, table_name):
        """Write out the data table.
        
        Arguments:
            table_name {str} -- Name of the table in hit_xml dict. 
        """
        if table_name == 'Metadata':
            table = self.render_metadatatable(self.hit_xml()[table_name])
        else:
            table = self.render_datatable(self.hit_xml()[table_name])
        if not table.empty:
            Path.mkdir(self.outdir / table_name, parents=True, exist_ok=True)
            with open(self.outdir / table_name / self.outfile, "w") as outfile_:
                table.to_csv(outfile_, sep='\t', index=False)
                sys.stderr.write(f"Written {outfile_.name}\n")
        else:
            sys.stderr.write(f"No data to write for AR Bank number {self.bank_no}\n")
