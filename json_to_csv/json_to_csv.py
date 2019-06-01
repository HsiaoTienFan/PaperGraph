# -*- coding: utf-8 -*-
"""

@author: Daniel Fan
"""

import os
import csv
import glob
import json


def load_files(path_query):
    file_paths = glob.glob(path_query)
    files_names = [i.replace('\\', '/') for i in file_paths]
    return files_names


def convert(file):
    path = os.path.dirname(file) + '/'
    with open(file) as f:
        filename = os.path.basename(file)
        with open(path + filename[:-4] + 'csv', 'w', newline='', encoding='utf-8') as csvfile:
            for line in f:
                line_dict = process_dictionary(line)
                csv_columns = list(line_dict.keys())
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',')
                writer.writerow(line_dict)


def create_header(file_names):
    file = file_names[2]
    path = os.path.dirname(file) + '/'
    with open(file) as f:
        line = f.readline()
        first_line = process_dictionary(line)
        with open(path + '000.csv', 'w', newline='', encoding='utf-8') as header:
            writer = csv.writer(header, delimiter=',')
            writer.writerow(first_line)


def process_dictionary(line):
    line_dict = json.loads(line)
    line_dict = {i:line_dict[i] if line_dict[i] is not None else 'Missing' for i in line_dict}
    line_dict['abstract'] = line_dict['abstract'].replace('\n', '')
    line_dict.pop('rawRecordXml')
    line_dict.pop('enrichments')
    return line_dict


def convert_all_json(file_names):
    for count, file in enumerate(file_names):
        convert(file)
        print('{} out of {} converted'.format(count, len(file_names)))


def main():
    path_query = "D:/papers/*.json"
    file_names =  load_files(path_query)
    create_header(file_names)
    convert_all_json(file_names)


if __name__ == "__main__":
    main()
