# ARBanker


[![Build Status](https://travis-ci.com/schultzm/ARBanker.svg?branch=master)](https://travis-ci.com/schultzm/ARBanker)  
[![codecov](https://codecov.io/gh/schultzm/ARBanker/branch/master/graph/badge.svg)](https://codecov.io/gh/schultzm/ARBanker)  
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)  
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)  
[![Powered by](https://img.shields.io/badge/powered%20by-jekyl-blue.svg)](https://schultzm.github.io/ARBanker/)  


Download metadata for isolates stored in the 
[CDC & FDA's Antibiotic Resistance Isolate Bank](https://www.cdc.gov/drugresistance/resistance-bank/index.html)  

This program will scrape the CDC webpages and parse out the tables to file for each AR Bank ID ("isolate").  

## Motivation 

Upon requesting (via email) metadata from the CDC for all isolates stored in the ARIsolateBank, we were informed that was no API so would need to manually click through to get the data tables – in excel format and pdf.  Since this did not suit our purposes and there was likely a need for other analysts to do a similar thing, ARBanker was born.

## Authors

[Mark Schultz](https://github.com/schultzm)  
[Torsten Seemann](https://github.com/tseemann)  

## Installation

If you don't already have it, install `python3` (with `brew install python3`).  Install [`pipenv`](https://docs.pipenv.org/en/latest/) (with `brew install pipenv`).  After this, do:  

```
git clone https://github.com/schultzm/ARBanker.git
cd ARBanker
pipenv install .
pipenv shell
cd
```

If at any time you need to exit the `pipenv shell`, just do `exit`.
On installing, you should see something like:

```
Installing .…
Adding arbanker to Pipfile's [packages]…
✔ Installation Succeeded 
Installing dependencies from Pipfile.lock (f80b0a)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 5/6 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

If you want to run this program in parallel, use `gnu parallel`, installed via:  

```
brew install parallel
```

#### Upgrading the installation  

To get the latest version, do:
```
pip3 install git+https://github.com/schultzm/ARBanker.git --upgrade
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

[Josua Schmid](https://github.com/schmijos) (wrote the [parser.py](https://github.com/schmijos/html-table-parser-python3/blob/master/html_table_parser/parser.py) script, which importantly contains the `HTMLTableParser` Class that I have utilised for this package)  
[Microbiological Diagnostic Unit - Public Health Laboratory (my employer)](https://biomedicalsciences.unimelb.edu.au/departments/microbiology-Immunology/research/services/microbiological-diagnostic-unit-public-health-laboratory)
