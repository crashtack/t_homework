# Server Status Report Generator
Server Status Report Generator will query servers bases on a list of servers in 
the servers.txt file. The individual server status are saved to an ArangoDB 
collection and then a query is done to generate an aggregated report. The report
will output to the console and to a time stamped log file.

## Setup

### Install Python 3.6 if not installed

```
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.6
```

### Create a virtualenv
 
```
$ sudo apt-get install python3-pip
$ pip3 install virtualenv
$ virtualenv -p /usr/bin/python3.6 server_report_gen
```

### Set up ArangoDB
Download and instal ArangoDB 
https://www.arangodb.com/download-major/

### Add ArangoDB root password to environment variables
Edit ```server_report_gen/bin/activate```

add the following to the bottom of the file.

```export ARANGO_PASSWORD="whatever you set the Arango root password to"```

### Install required packages
```
$ pip install pyarango
$ pip install pytest
```

## Running
To run Server Status Report Generator type.

```
$ python server_status.py
```
