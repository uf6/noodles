# noodles

We eat our data in a messy fashion, thank you.

## Requirements

- Flask, http://flask.pocoo.org/
- Elasticsearch, http://www.elasticsearch.org/

## Data

### Canada

- Source: http://www.tmxmoney.com/en/sector_profiles/energy.html
- Type: XLS File

Manual Processing:

1. Grab file from source (Oil & Gas Companies) as xls file
2. Create to separate files fom both sheets in file with columns "Name", "HQ Location"
3. Rename: "HQ Location" -> "Country"
4. Save both files as canada1.csv, canada2.csv with , as delimiter (and , quoted in company names)

### Australia

- Source: http://www.asx.com.au/asx/research/ASXListedCompanies.csv
- Type: -

### Concession Data - OpenOil

- Source: http://repository.openoil.net/wiki/Concession_Layer_Methodology#Sourcing
- Type: -

### SEC

- Source: -
- Type: -


## Installation

Getting Started:

```
$ cd /opt
$ git clone https://github.com/uf6/noodles
```

Docker for Elasticsearch (optional):

```
$ docker pull dockerfile/elasticsearch
$ mkdir /opt/noodles-elastic
$ vi /opt/noodles-elastic

path:
  logs: /data/log
  data: /data/data

$ mkdir /opt/noodles-elastic/data
$ mkdir /opt/noodles-elastic/log 
$ docker run -d -p 9200:9200 -p 9300:9300 -v /opt/noodles-elastic/:/data dockerfile/elasticsearch /elasticsearch/bin/elasticsearch -Des.config=/opt/noodles-elastic/elasticsearch.yml
$ /usr/bin/docker run -p 8089:80 -v /opt/noodles:/src -e VIRTUAL_HOST=noodles.iilab.org --privileged -d -t --name noodles iilab/static
````

Setup:

```
$ python setup.py install
$ python noodles/manage.py ingest edgar
$ python noodles/manage.py index edgar
```

## Run server

```
$ python noodles/manage.py runserver -p 7777
```
