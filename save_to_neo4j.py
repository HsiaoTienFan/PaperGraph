# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""

import create_CQL_logic
from neo4j.v1 import GraphDatabase


def connect_to_server():
    # Database Credentials
    uri             = "bolt://localhost:7687"
    userName        = "neo4j"
    password        = "123456"
 
    # Connect to the neo4j database server
    graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))
    return graphDB_Driver


def write_to_database(graphDB_Driver, cql_create):
# Execute the CQL query
    with graphDB_Driver.session() as graphDB_Session:

        # Create nodes
        graphDB_Session.run(cql_create)


def load_current_paper(paper, ref_list):
    graphDB_Driver = connect_to_server()
    cql_create = create_CQL_logic.create_cql_for_paper_load(paper, ref_list)
    write_to_database(graphDB_Driver, cql_create)

