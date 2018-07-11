import os
from pyArango.connection import *

from server_status import ServerStatus, line_to_key
from server_status import query_application, query_application_version, db_initialize


SERVER = 'server_report'
COLLECTION = 'server_report'

CONN = Connection(username="root", password=os.environ['ARANGO_PASSWORD'])
DB = CONN[SERVER]
COLL = DB[COLLECTION]

def test_server_creation():
    server = ServerStatus(4)
    assert server.key == 4

def test_server_get_status():
    server = ServerStatus(4)
    data = server.get_status()
    assert type(data) is dict

def test_save_status():
    server = ServerStatus(1)
    server.get_status()
    server.save_status(COLL)
    element = COLL['1']
    assert element['Application'] == 'Cache2'

def test_line_to_key():
    assert line_to_key("server-0022") == '22'

def test_query_application():
    assert len(query_application('Cache1', DB)) == 18

def test_query_application_version():
    results = query_application_version('Cache1', '0.0.2', DB)
    assert len(results) == 10

def test_db_initialize():
    server = 'test2'
    collection = 'test_coll'
    try:
        db = CONN[server]
    except KeyError:
        assert True

    try:
        db = CONN[server]
    except KeyError:
        db_initialize(server, collection)

    try:
        db = CONN[server]
        coll = db[collection]
        assert True
    except:
        assert False
