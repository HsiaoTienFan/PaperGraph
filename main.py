# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""

import re
import glob
import bibtexparser
import xml.etree.ElementTree as ET
import save_to_neo4j


def clean_paper(paper_file):
    with open(paper_file, 'r+', encoding="utf-8") as f:
        text = f.read()
        text = re.sub('(\\n)(.*?)(<xref)(.*?)(>)', '', text)
        text = re.sub('(<\/xref>\\n\s+)', '', text)
        text = re.sub('(<\/xref>)', '', text)
        f.seek(0)
        f.write(text)
        f.truncate()
        f.close()


def extract_sections(tree):
    sections = {}
    for section in tree.findall(".//sec"):
        title = section.find(".//title").text
        paragraphs = section.findall(".//p")
        content = ''
        for paragraph in paragraphs:
            content += paragraph.text.lstrip() + '\n'
        sections[title.title()] = content
    return sections


def read_paper(paper_file):
    clean_paper(paper_file)
    tree = ET.parse(paper_file)
    year = tree.find(".//year").text
    title = tree.find(".//article-title").text
    journal = [name.text for name in tree.findall(".//journal-title")]
    author = [name.text for name in tree.findall(".//contrib//string-name")]
    abstract = tree.find(".//abstract//p").text
    sections = extract_sections(tree)
    pages = tree.find(".//fpage").text + '--' + tree.find(".//lpage").text
    paper = {'year':year, 'title':title, 'journal':journal, 'author':author, 'abstract':abstract, 'sections':sections, 'pages':pages}
    try:
        paper['sections'].pop('-')
    except:
        pass
    return paper


def get_ref_list(bibtex_file):
    with open(bibtex_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    ref_list = bib_database.entries
    return ref_list


def main():
    bibtex_file = glob.glob("data/*.bibtex")[0]
    paper_file = glob.glob("data/*.cermxml")[0]
    ref_list = get_ref_list(bibtex_file)
    paper = read_paper(paper_file)
    save_to_neo4j.load_current_paper(paper, ref_list)




