# ARBanker

Download metadata for isolates stored in the 
[CDC & FDA Antibiotic Resistance Isolate Bank](
    https://wwwn.cdc.gov/ARIsolateBank/
)  

This program will scrape the CDC webpages and parse out the tables to file for each AR Bank ID ("isolate").

## Author

[Mark Schultz](https://github.com/schultzm)

## Installation

Install pip3, then do:  

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

If you want to run this program in parallel, use `gnu parallel`, installed via:  

```
brew install parallel
```


## Quick start

In this example we will get data for isolate number 1.  

```
arbanker grab 1
```

The output should look like:

```
Written ${HOME}/ARBanker/results/Metadata/001.tab.
Written ${HOME}/ARBanker/results/MIC/001.tab.
Written ${HOME}/ARBanker/results/MMR/001.tab.
```

## Advanced usage

Output the data to a user-defined folder:  
 
```
arbanker grab 1 -o ~/tmp/arbanker
```

Run `arbanker` for multiple queries in parallel, outputting to custom 
destination:  

```
parallel --bar arbanker grab {} -o ~/tmp/arbankerparallel ::: $(seq 1 100)
```
