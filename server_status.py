import os
import requests
import json
from pyArango.connection import *
from time import gmtime, strftime

#[x] TODO: Create the server object.
#[x] TODO: For each server in server.txt query server.
#[ ] TODO: Make server query multithreaded.
#[x] TODO: Save each Server response to DB.
#[ ] TODO: Mark any unavalable servers. Not required for MVP
#[ ] TODO: Mark any old servers. Not required for MVP
#[x] TODO: Update the list of Applications
#[ ] TODO: Create Graph of Applications, Versions, server status. Not required for MVP

#[x] TODO: Generate Aggrigate report per Applicationa and Version.
#[x] TODO: For each Application version. Perform a query and report Aggrigate
#[ ] TODO: Output a report to file. 
#[ ] TODO: Logging and metrix code. Not for MVP


SERVER = 'server_report'
COLLECTION = 'server_report'

CONN = Connection(username="root", password=os.environ['ARANGO_PASSWORD'])



def db_initialize(server, collection):
    db = CONN.createDatabase(name=server)
    coll = db.createCollection(name=collection)
    return db, coll

def db_save_element(col, key, data):
    try:
        doc = col[key]
    except KeyError:
        doc = col.createDocument()
        doc._key = key

    for k, v in data.items():
        doc[k] = v

    return doc.save()

class ServerStatus(object):

    def __init__(self, key):
        self.key = key

    def get_status(self):
        response = requests.get(f'http://127.0.0.1:5000/server?id={self.key}')
        self.data = json.loads(response.content)
        return self.data

    def save_status(self, coll):
        db_save_element(coll, f'{self.key}', self.data)


def line_to_key(line):
    split = line.split('-')
    key = split[1].strip('0').rstrip()
    return key

def query_application(app, db):
    aql = """FOR x in {0}
                FILTER x.Application == '{1}'
                RETURN x""".format(COLLECTION, app)
    query_results = db.AQLQuery(aql, rawResults=True, batchSize=10)
    versions = []
    for result in query_results:
        if result['Version'] not in versions:
            versions.append(result['Version'])
    versions.sort()
    return versions

def query_application_version(app, ver, db):
    aql = """FOR x in {0}
                 FILTER x.Application == '{1}'
                 FILTER x.Version == '{2}'
                 RETURN x""".format(COLLECTION, app, ver)
    query_results = db.AQLQuery(aql, rawResults=True, batchSize=10)
    return query_results

def generate_report(results, file_name):
    uptime = 0
    request_count = 0
    error_count = 0
    success_count = 0

    for result in results:
        uptime += result['Uptime']
        request_count += result['Request_Count']
        error_count += result['Error_Count']
        success_count += result['Success_Count']


    uptime = uptime / len(results)
    request_count = request_count / len(results)
    error_count = error_count / len(results)
    success_count = success_count / len(results)

    print('{0:15s} {1:15s} {2:15d} {3:15d} {4:15d} {5:15d}'.format(
        result['Application'],
        result['Version'],
        int(uptime),
        int(request_count),
        int(error_count),
        int(success_count)
    ))

    output = {}
    output['Application'] = result['Application']
    output['Version'] = result['Version']
    output['Uptime'] = uptime
    output['RequestCount'] = request_count
    output['ErrorCount'] = error_count
    output['SuccessCount'] = success_count

    with open(file_name, 'a') as f:
        f.write(json.dumps(output))
        f.write('\n')



def main():
    """
        Read the server file.
        Make a request to server for status.
        Save status to a DB.
        Create a list of Applications
        Create reports by quering DB.
    """

    try:
        db = CONN[SERVER]
        coll = db[COLLECTION]
    except KeyError:
        db_initialize(SERVER, COLLECTION)
        db = CONN[SERVER]
        coll = db[COLLECTION]

    file_name = 'server_report-{}.log'.format(strftime("%Y-%m-%d::%H:%M:%S", gmtime()))
    applications = []

    with open('servers.txt') as f:
        for line in f:
            key = line_to_key(line)
            server = ServerStatus(key)
            data = server.get_status()
            if data['Application'] not in applications:
                applications.append(data['Application'])
            server.save_status(coll)

    applications.sort()

    print('{0:15s} {1:15s} {2:>15s} {3:>15s} {4:>15s} {5:>15s}'.format(
        'Application',
        'Version',
        'Uptime',
        'Request_Count',
        'Error_Count',
        'Success_Count'
    ))

    for app in applications:
        versions = query_application(app, db)
        for ver in versions:
            results = query_application_version(app, ver, db)
            generate_report(results, file_name)


if __name__ == '__main__':
    main()
