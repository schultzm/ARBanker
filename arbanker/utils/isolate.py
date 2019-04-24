from pathlib import Path
import pandas as pd
import re
import sys


class Isolate:
    basetarget = "https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID="
    def __init__(self, bank_no, outdir):
        """Intialise the Isolate.
        
        Arguments:
            bank_no {int} -- The AR Isolate Bank item number.
            outdir {PosixPath} -- Destination folder for results.
        """

        self.bank_no   = str("{:03d}".format(bank_no))
        self.target    = f"{self.basetarget}{self.bank_no}"
        self.outdir    = outdir
        self.outfile   =  f"{self.bank_no}.tab"
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
        from urllib.request import Request, urlopen
        # get website content
        req = Request(url=self.target)
        f = urlopen(req)
        xhtml = f.read().decode('utf-8')
        # instantiate the parser and feed it
        p = HTMLTableParser()
        p.feed(xhtml)
        return {"Metadata": p.tables[0],
                "MIC": p.tables[1],
                "MMR": p.tables[2]}

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
                    replace('Negative  Carba', 'Negative\tCarba')
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
        if 'Drug' in table.columns:
            # Replace the footnote markers with ''
            table.Drug = table.Drug.apply(lambda x: re.sub(' [0-9]$', '', x))
        table[self.index_name] = self.bank_no
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
            print(table.to_csv())
            with open(self.outdir / table_name / self.outfile, "w") as outfile_:
                table.to_csv(outfile_, sep='\t', index=False)
                sys.stderr.write(f"Written {outfile_.name}\n")
        else:
            sys.stderr.write(f"No data to write for AR Bank number {self.bank_no}\n")
