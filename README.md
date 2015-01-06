noodles
=======

We eat our data in a messy fashion, thank you.

Requirements
------------

- Flask, http://flask.pocoo.org/
- Elasticsearch, http://www.elasticsearch.org/

Data
----

Data is used from https://github.com/holgerd77/openoil-companies/

Installation
------------

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

Run server
----------
```
$ python noodles/manage.py runserver -p 7777
```
