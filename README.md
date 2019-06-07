# ARBanker


[![Build Status](https://travis-ci.com/schultzm/ARBanker.svg?branch=master)](https://travis-ci.com/schultzm/ARBanker)  
[![codecov](https://codecov.io/gh/schultzm/ARBanker/branch/master/graph/badge.svg)](https://codecov.io/gh/schultzm/ARBanker)  
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)  
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)  
[![Powered by](https://img.shields.io/badge/powered%20by-jekyl-blue.svg)](https://schultzm.github.io/ARBanker/)  


Download metadata for isolates stored in the 
[CDC & FDA Antibiotic Resistance Isolate Bank](https://www.cdc.gov/drugresistance/resistance-bank/index.html)  

This program will scrape the CDC webpages and parse out the tables to file for each AR Bank ID ("isolate").  


## Author

[Mark Schultz](https://github.com/schultzm)

## Installation

Install `pip3`, then do:  

```
pip3 install git+https://github.com/schultzm/ARBanker.git
```

You should see something like:

```
Collecting git+https://github.com/schultzm/ARBanker.git
  Cloning https://github.com/schultzm/ARBanker.git to /private/var/folders/cw/mt4j09h13bs407sx3rnyqg65lkl8k4/T/pip-req-build-tkrltx_p
Building wheels for collected packages: arbanker
  Building wheel for arbanker (setup.py) ... done
  Stored in directory: /private/var/folders/cw/mt4j09h13bs407sx3rnyqg65lkl8k4/T/pip-ephem-wheel-cache-4j3hinq4/wheels/de/bc/f5/a7ab859b598b192e1118877edf45de19649d177bee933741ab
Successfully built arbanker
Installing collected packages: arbanker
Successfully installed arbanker-1.0.1
```

If you want to run this program in parallel, use `gnu parallel`, installed via:  

```
brew install parallel
```

### Testing installation

Run the test suite:  
```
arbanker test
```

You should see:  

```
test_hit_url (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_hit_xml (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_render_metadatatable (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_render_datatables (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_hit_url (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok
test_hit_xml (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok
test_render_metadatatable (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok
test_render_datatables (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok

----------------------------------------------------------------------
Ran 8 tests in 11.004s

OK

```


## Quick start

In this example we will get data for isolate number 1.  

```
arbanker grab 1
```

The stdout should look like:

```
Written ${HOME}/arbanker_results/Metadata/0001.tab.
Written ${HOME}/arbanker_results/MIC/0001.tab.
Written ${HOME}/arbanker_results/MMR/0001.tab.
```

And the contents of each file are outlined below.

### Metadata/0001.tab  

```
AR Bank	Biosample Accession	Panel	Species
0001	SAMN04014842	Enterobacteriaceae Carbapenem Breakpoint	Escherichia coli
```

### MMR/0001.tab

```
AR Bank	Category	Gene
0001	Aminoglycoside	aac(6')Ib-cr,aadA5
0001	Beta-lactam	KPC-3 ,OXA-1
0001	Macrolide-Lincosamide-Streptogramin	mph(A)
0001	Sulfonamides	sul1
0001	Tetracyclines	tet(A)
0001	Trimethoprim	dfrA17
```

### MIC/0001.tab

```
AR Bank	Drug	MIC (μg/ml)	INT
0001	Amikacin	16	S
0001	Ampicillin	>32	R
0001	Ampicillin/sulbactam	>32	R
0001	Aztreonam	>64	R
0001	Cefazolin	>8	R
0001	Cefepime	>32	R
0001	Cefotaxime	>64	R
0001	Cefotaxime/clavulanic acid	8	---
0001	Cefoxitin	>16	R
0001	Ceftazidime	128	R
0001	Ceftazidime/avibactam	< =0.5	S
0001	Ceftazidime/clavulanic acid	>64	---
0001	Ceftolozane/tazobactam	>16	R
0001	Ceftriaxone	>32	R
0001	Ciprofloxacin	>8	R
0001	Colistin	0.5	---
0001	Doripenem	4	R
0001	Ertapenem	8	R
0001	Gentamicin	4	S
0001	Imipenem	4	R
0001	Imipenem+chelators	4	---
0001	Levofloxacin	>8	R
0001	Meropenem	4	R
0001	Piperacillin/tazobactam	>128	R
0001	Tetracycline	>32	R
0001	Tigecycline	< =0.5	S
0001	Tobramycin	>16	R
0001	Trimethoprim/sulfamethoxazole	>8	R
```

## Advanced usage

Output the data to a user-defined folder:  
 
```
arbanker grab 1 -o ~/tmp/arbanker
```

Run `arbanker` for multiple queries in parallel, outputting to custom 
destination:  

```
parallel --bar arbanker grab {} -o ~/tmp/arbankerparallel ::: $(seq 1 500)
```

## Acknowledgements

[Torsten Seemann](https://github.com/tseemann) (installed, ran test suite, made suggestions for improvements)  
[Josua Schmid](https://github.com/schmijos) (wrote the [parser.py](https://github.com/schmijos/html-table-parser-python3/blob/master/html_table_parser/parser.py) script, which importantly contains the `HTMLTableParser` Class that I have utilised for this package)  
[Microbiological Diagnostic Unit - Public Health Laboratory (my employer)](https://biomedicalsciences.unimelb.edu.au/departments/microbiology-Immunology/research/services/microbiological-diagnostic-unit-public-health-laboratory)
