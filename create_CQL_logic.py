# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""


def create_cql_for_paper_load(paper, ref_list):
    full_name_list = paper['author']
    cql_create = """
        {}

        {}

        {}

        {}
        """.format(\
        creat_paper_cql(paper),\
        create_section_cql(paper),\
        create_author_cql(full_name_list, 'article', 'base'),\
        create_references_cql(ref_list))
    return cql_create


def creat_paper_cql(paper):
    template_part1 = \
    """MERGE (article:Article{})
    """
    template_part2 = \
    """SET article.{} = "{}"
    """
    current_cql = ''
    remove = ['author', 'title', 'sections', 'ENTRYTYPE', 'ID']
    title = '{title:"' + paper['title'] + '"}'
    filtered_paper_properties = {key:value for key, value in paper.items() if key not in remove}
    for key, value in filtered_paper_properties.items():
        current_cql += template_part2.format(key, value)
    paper_cql = template_part1.format(title) + current_cql
    return paper_cql


def create_ref_cql(paper, ref):

    template_part1 = \
    """MERGE (article:Article{})
    """
    template_part2 = \
    """SET article.{} = "{}"
    """
    current_cql = ''
    remove = ['author', 'title', 'sections', 'ENTRYTYPE', 'ID']
    paper_title = '{title:"' + paper['title'] + '"}'
    ref_title = '{title:"' + ref['title'] + '"}'
    filtered_paper_properties = {key:value for key, value in paper.items() if key not in remove}

    match = \
    """MATCH (source:Article{})
    """.format(paper_title)
    join = \
    """MERGE (source)-[:REFERENCES]->(article)
    """

    for key, value in filtered_paper_properties.items():
        current_cql += template_part2.format(key, value)
    paper_cql = match + template_part1.format(ref_title) + current_cql + join
    return paper_cql


def create_section_cql(paper):
    template1 = """MATCH (article:Article{})
    """
    template2 = \
    """MERGE (section{}:Section{})
MERGE (article)-[:HAS_THIS_SECTION]->(section{})

    """
    current_cql = ''
    title = '{title:"' + paper['title'] + '"}'
    for count, (key, value) in enumerate(paper['sections'].items()):
        properties = '{section:"' + key + '", content:"' + value + '"}'
        current_cql += template2.format(str(count),\
                                       properties,\
                                       str(count))
    section_cql = template1.format(title) + current_cql
    return section_cql


def create_author_cql(full_name_list, article_key, ID):
    template = \
    """MERGE (author{}:Authors{})
        MERGE ({})-[:WRITTEN_BY]->(author{})
    """
    author_cql = ''
    name_break_down = ['Last', 'First', 'Middle']
    for count, full_name in enumerate(full_name_list):
        collection = []
        each_name = list(map(str.strip, full_name.strip().split(' ')))
        each_name = each_name[-1:] + each_name[:-1]
        name_to_key = zip(name_break_down, each_name)
        for key, name in name_to_key:
            collection.append(key + ':"' + name + '"')
        deconstructed_names = '{' + ' ,'.join(collection) + '}'
        author_cql += template.format(ID+str(count),\
                                       deconstructed_names,\
                                       article_key,\
                                       ID+str(count))
    return author_cql

