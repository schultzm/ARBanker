# ARBanker

Download metadata for isolates stored in the 
[CDC & FDA Antibiotic Resistance Isolate Bank](
    https://wwwn.cdc.gov/ARIsolateBank/
)  

This program will scrape the CDC webpages and parse out the tables for an 
isolate to file.

## Author

[Mark Schultz](https://github.com/schultzm)

## Installation
Install pip3, then install `pipenv` with `pip3 install pipenv`.  

After installing `pipenv`, do:  

```
pipenv shell
pip3 install git+https://github.com/schultzm/ARBanker.git
```

You should see something like:

```
...
Building wheels for collected packages: arbanker
  Building wheel for arbanker (setup.py) ... done
  Stored in directory: /private/var/folders/cw/mt4j09h13bs407sx3rnyqg65lkl8k4/T/pip-ephem-wheel-cache-0jer2a44/wheels/de/bc/f5/a7ab859b598b192e1118877edf45de19649d177bee933741ab
Successfully built arbanker
Installing collected packages: arbanker
Successfully installed arbanker-0.1.0b0
```

### Testing installation

After staring pipenv, run the test suite:  
```
pipenv shell
arbanker test
```

You should see:  
```
arbanker test
test_hit_url (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_hit_xml (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_render_metadatatable (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_render_datatables (arbanker.tests.test_isolate.IsolateTestCasePass) ... ok
test_hit_url (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok
test_hit_xml (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok
test_render_metadatatable (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok
test_render_datatables (arbanker.tests.test_isolate.IsolateTestCaseFail) ... ok

----------------------------------------------------------------------
Ran 8 tests in 13.132s

OK

```

If you want to run this program in parallel, use `gnu parallel`, installed via:  

```
brew install parallel
```


## Quick start

In this example we will get data for isolate number 1.  

Start the environment by running:
```
pipenv shell
```

Now query the webpage for isolate number 1:

```
arbanker grab 1
```

The output should look like:

```
(ARBanker) bash-3.2$ arbanker grab 1
Written ${HOME}/ARBanker/results/Metadata/001.tab.
Written ${HOME}/ARBanker/results/MIC/001.tab.
Written ${HOME}/ARBanker/results/MMR/001.tab.
```

## Advanced usage

Output the data to a user-defined folder:  
- Start the environment:  
```
pipenv shell
```

- Run `arbanker`:  
```
arbanker grab 1 -o ~/tmp/arbanker
```

Run `arbanker` for multiple queries in parallel, outputting to custom 
destination:  

```
parallel --bar arbanker grab {} -o ~/tmp/arbankerparallel ::: $(seq 1 100)
```
