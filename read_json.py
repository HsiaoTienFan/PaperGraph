# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""

import glob
import save_to_neo4j


def load_files(path_query):
    file_paths = glob.glob(path_query)
    files_names = [i[3:].replace('\\', '/') for i in file_paths]
    return files_names


def form_json_cql(file_path):
    json_cql = """
    CALL apoc.periodic.iterate("
    CALL apoc.load.json('file:///papers/1.json') YIELD value as paper
    ","
    WHERE paper['title'] IS NOT NULL
    CREATE (a:Article{title: paper['title']})
    SET a.abstract = paper['abstract']
    SET a.author = paper['authors']
    SET a.contributors = paper['contributors']
    SET a.coreId = paper['coreId']
    SET a.datePublished = paper['datePublished']
    SET a.doi = paper['doi']
    SET a.downloadUrl = paper['downloadUrl']
    SET a.fullTextIdentifier = paper['fullTextIdentifier']
    SET a.oai = paper['oai']
    SET a.publisher = paper['publisher']
    SET a.topics = paper['topics']
    SET a.year = paper['year']
    ", {batchSize: 1000, iterateList: true});
    """
    return json_cql


def load_all_json(file_names):
    graphDB_Driver = save_to_neo4j.connect_to_server()
    for count, file in enumerate(file_names):
        json_cql = form_json_cql(file)
        save_to_neo4j.write_to_database(graphDB_Driver, json_cql)
        print('{} out of {} loaded'.format(count, len(file_names)))


def main():
    path_query = "D:/papers/*"
    file_names =  load_files(path_query)
    load_all_json(file_names)


if __name__ == "__main__":
    main()
