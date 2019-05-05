# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""

import glob
import bibtexparser
import xml.etree.ElementTree as ET


def read_paper():
    paper_file = glob.glob("data/*.cermxml")[0]
    tree = ET.parse(paper_file)
    root = tree.getroot()
    year = root.iter('year').__next__().text
    return 

def read_bibtext():
    bibtex_file = glob.glob("data/*.bibtex")[0]
    ref_list = read_bibtex(bibtex_file)
    return ref_list
    
def get_ref_list(bibtex_file):
    with open(bibtex_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    ref_list = bib_database.entries
    return ref_list


def extract_paper_data():
    
    

def main():


    ref_list = read_bibtext()



    test = ref_list[0]









tree = ET.parse(paper_file)
root = tree.getroot()
for child in root:
    print child.tag, child.attrib

for neighbor in root.iter('year'):
     print(neighbor.text)
