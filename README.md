# ARBanker

Download metadata for isolates stored in the 
[CDC & FDA Antibiotic Resistance Isolate Bank](
    https://wwwn.cdc.gov/ARIsolateBank/Panel/IsolateDetail?IsolateID=99999999
)

Install pip3, then install `pipenv` with `pip3 install pipenv`

## Quick start

### Install
In this example we will get data for Isolate 1.  
After launching an environment with `pipenv shell`, do:


```
pip3 install git+https://github.com/schultzm/ARBanker.git
arbanker grab 
```