from neo4j import GraphDatabase

class Neo4jConnection:

    driver = GraphDatabase.driver(
            'neo4j://localhost:7687',
            auth=('neo4j','test')
    )