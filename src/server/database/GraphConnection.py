from neo4j import GraphDatabase
from decouple import config

DB_URI=config('DB_IP')
DB_NAME=config('DB_NAME')
DB_PSW=config('DB_PSW')

class GraphConnection:

    def __init__(self, uri = DB_URI, user = DB_NAME, password = DB_PSW):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()