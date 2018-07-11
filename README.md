# Server Status Report Generator

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
### Add ArangoDB root password to environment variables
Edit ```server_report_gen/bin/activate```

add

```export ARANGO_PASSWORD="whatever you set the Arango root password to"```

### Set up ArangoDB
Download and instal ArangoDB 
https://www.arangodb.com/download-major/

### Install required packages
```
$ pip install pyarango


