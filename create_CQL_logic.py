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
    paper_key_list = list(paper.keys())
    template = \
    """MERGE (article:Article{})
    SET article.year = "{}"
    SET article.title = "{}"
    SET article.journal = "{}"
    SET article.abstract = "{}"
    SET article.pages = "{}"
    SET article.loaded = "YES"
    """
    properties = '{title:"' + paper[paper_key_list[1]] + '"}'
    paper_cql = template.format(\
    properties,\
    paper[paper_key_list[0]],\
    paper[paper_key_list[1]],\
    paper[paper_key_list[2]],\
    paper[paper_key_list[4]],\
    paper[paper_key_list[6]])
    return paper_cql


def create_section_cql(paper):
    template = \
    """MERGE (section{}:Section{})
        MERGE (article)-[:HAS_THIS_SECTION]->(section{})
    """
    section_cql = ''
    for count, (key, value) in enumerate(paper['sections'].items()):
        properties = '{title:"' + key + '", content:"' + value + '"}'
        section_cql += template.format(str(count),\
                                       properties,\
                                       str(count))
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


def remove_outdated_authors():
    outdated_authors = \
    """MATCH (article)-[:WRITTEN_BY]->(outdated:author)
        DELETE outdated
    """
    return outdated_authors


def create_references_cql(ref_list):
    def rearrange_into_author_cql(author_list, reference_number, ID):
        full_name_list = []
        for i in range(0, len(author_list), 2):
            try:
                full_name_list.append(author_list[i+1] + author_list[i])
            except:
                pass
        author_cql = create_author_cql(full_name_list, 'article{}'.format(reference_number), ID)
        return author_cql


    template_part1 = \
    """MERGE (article{}:Article{})
    """
    template_part2 = \
    """ON CREATE SET article{}.{} = '{}'
    """
    template_part3 = \
    """MERGE (article)-[:REFERENCES]->(article{})
    """
    ref_list
    remove = ['ENTRYTYPE', 'author', 'title']
    ref_cql = ''
    for count, ref in enumerate(ref_list):
        if 'title' in ref:
            properties = '{title:"' + ref['title'] + '"}'
            author_list = ref['author'].split(',')
            filtered_ref = {key:value for key, value in ref.items() if key not in remove}
            part_1 = template_part1.format(count, properties)
            part_2 = ''
            for key, value in filtered_ref.items():
                part_2 += template_part2.format(count, key, value)
            part_3 = template_part3.format(count)
            ID = ref['ID']
            author_part = rearrange_into_author_cql(author_list, count, ID)
            ref_cql += part_1 + part_2 + part_3 + author_part
    return ref_cql









