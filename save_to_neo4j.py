# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""

from neo4j.v1 import GraphDatabase


def connect_to_server():
    # Database Credentials
    uri             = "bolt://localhost:7687"
    userName        = "neo4j"
    password        = "123456"
 
    # Connect to the neo4j database server
    graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))
    return graphDB_Driver


def form_CQL(paper, ref):
    # CQL to create a graph with current paper
    cql_create = """
    MATCH (n)
    WITH n.name AS name, COLLECT(n) AS nodelist, COUNT(*) AS count
    WHERE count > 1
    CALL apoc.refactor.mergeNodes(nodelist) YIELD node
    RETURN node
    """
    return cql_create


def write_to_database(graphDB_Driver, cql_create):
# Execute the CQL query
    with graphDB_Driver.session() as graphDB_Session:

        # Create nodes
        graphDB_Session.run(cql_create)


def load_current_paper(paper, ref):
    graphDB_Driver = connect_to_server()
    cql_create = form_CQL(paper, ref)
    write_to_database(graphDB_Driver, cql_create)