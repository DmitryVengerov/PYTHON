import couchdb
import socket 

couchserver = couchdb.Server("http://0.0.0.0:5984/")

user = "admin"
password = 'admin'

couchserver = couchdb.Server("http://%s:%s@0.0.0.0:5984/" % (user, password))

for dbname in couchserver:
    print(dbname)

