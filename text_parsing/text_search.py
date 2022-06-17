import re
import os
from datetime import datetime

def find_relative_filenames(path,start_date,end_date):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    file_names = [path+'/'+fn for fn in os.listdir(path) if datetime.strptime(fn[:10], '%Y-%m-%d')>=start_datetime and datetime.strptime(fn[:10], '%Y-%m-%d')<=end_datetime]
    return file_names

def read_as_string(filename):
    with open(filename, "r", encoding='utf-8') as f:
        text_content = f.read()
    return text_content

def find_keyword(keyword, content):
    result_dict = {}
    if keyword.lower() in content.lower():
        location = content.lower().find(keyword.lower())
        #result_dict[keyword] = location
        return location
    else:
        return None

def find_keyword_in_files(listofkeywords, path, start_date='2008-01-01', end_date="2018-12-31"):
    file_list = find_relative_filenames(path,start_date,end_date)
    consolidated_results = {}
    for file in file_list:
        print("Searching file:", file)
        file_content = read_as_string(file)
        search_result = {}
        for word in listofkeywords:
            keyword_result = find_keyword(word, file_content)
            if keyword_result is not None:
                search_result[word]=keyword_result
        consolidated_results[file] = search_result
    return consolidated_results