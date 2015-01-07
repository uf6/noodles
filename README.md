# noodles

We eat our data in a messy fashion, thank you.

## Requirements

- Flask, http://flask.pocoo.org/
- Elasticsearch, http://www.elasticsearch.org/
- Elasticsearch.js, http://www.elasticsearch.org/guide/en/elasticsearch/client/javascript-api/current/
- Facetview, https://github.com/okfn/facetview
- d3.js, http://d3js.org/

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
- Type: CSV File

Processing with Google (Open) Refine:

1. Download file from source
2. Create a new project from within OpenRefine (http://openrefine.org)
3. Create a text facet (filter) on column3 (GICS industry group) for groups "Energy" and "Materials"
4. Export project/file as comma-separated CSV file
5. Open file, remove 2nd, 3rd column (just company name remaining), rename column header to "Name" and add second empty column "country"
6. Save as ``data/australia_YYYY-MM-DD.csv``

### Concession Data - OpenOil

- Source: http://repository.openoil.net/wiki/Concession_Layer_Methodology#Sourcing
- Type: CSV File(s)

Processing with Google Refine:

1. Download TOTAL file with all concessions (if available) or otherwise download country concession files and concatenate to one file with csvtoolkit -> csvstack command
2. Load into Google Refine
3. Delete all columns except "ConcessionContractor"
4. Split "ConcessionContractor" values and distribute to different rows ("Edit Cells" -> "Split multi-valued cells...")
5. Export as CSV file, rename "ConcessionContractor" column to "Name", add empty "County" column
6. Save as ``data/concession-companies_YYYY-MM-DD.csv``

### SEC

- Source: -
- Type: -


## Installation

Getting Started:

```
$ cd /opt
$ git clone https://github.com/uf6/noodles
```

## Meteor Frontend

 * Install & run noodles in meteor - https://www.meteor.com/install - 

```
$ curl https://install.meteor.com/ | sh
$ cd noodles/frontend
$ meteor
```

You should be able to access the application from ```http://localhost:3000```

 * Load data into Mongo's meteor

Default local settings are for an external Mongo database. To run the importer with the meteor MongoDB, modify local_settings to 
```
MONGO_URL = 'localhost'
MONGO_PORT = 3002
MONGO_DATABASE = 'meteor'
MONGO_COLLECTION = 'documents'
```

In a python virtualenv
```
$ python noodles/manage.py load_mongo
```


## Docker for Elasticsearch (optional):

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
