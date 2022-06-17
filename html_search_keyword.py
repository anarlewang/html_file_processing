import re
import os
import pandas as pd
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime

def strip_string(s):
    clean_text = unicodedata.normalize("NFKD",s)
    s_0 = re.sub('\ {2,}', '', clean_text)
    s_1 = re.sub('\n*', '', s_0)
    return s_1

def print_text(bs_item):
    bs_list = bs_item.find_all(["p","table"])
    for i in bs_list:
        clean_string = strip_string(i.text).strip()
        if clean_string is not None and clean_string != '':
            print(clean_string)
        if i.find("div") is not None:
            inside_div = i.find_all("div")
            for div in inside_div:
                print("INNER:")
                div_text_list = div.find_all("p")
                print_text(div_text_list)

def html_to_text(bs_item,tags):
    bs_list = bs_item.find_all(tags)
    text_lst = []
    second_layer_list = []
    for i in bs_list:
        clean_string = strip_string(i.text).strip()
        if clean_string is not None and clean_string != '':
            text_lst.append(clean_string)
    return text_lst+second_layer_list

def extract_text_to_list(bs_object):
    # Try the new format first
    try:
        bs_content = bs_object.find('sec-document').find("document").find("type").find("sequence").find("filename").find("description").find("text").find_all("center")
        lst_of_text = []
        for item in bs_content:
            lst_of_text+=html_to_text(item, ["p","table"])
    except:
        try:
            bs_content = bs_object.find('sec-document').find("document").find("type").find("sequence").find("filename").find("description").find("text")
        except:
            try:
                # exception 1: structure is different from other files
                bs_content = bs_object.find('sec-document').find("document").find("type").find("sequence").find("filename").find("text")
            except:
                print("File could not be parsed, skip.")
                return
        lst_of_text = html_to_text(bs_content,["p","table","ul"])
    if len(lst_of_text) == 0:
        # Try all other methods again.
        try:
            bs_content = bs_object.find('sec-document').find("document").find("type").find("sequence").find("filename").find("description").find("text")
            lst_of_text = html_to_text(bs_content,["p","table","ul"])
        except:
            try:
                # exception 1: structure is different from other files
                bs_content = bs_object.find('sec-document').find("document").find("type").find("sequence").find("filename").find("text")
                lst_of_text = html_to_text(bs_content,["p","table","ul"])
            except:
                print("File could not be parsed, skip.")
                return
        if len(lst_of_text) == 0:
            # If still can't read anything, parsing problem
            lst_of_text = html_to_text(bs_object,["p","table","ul"])
    return lst_of_text


def search_keyword(key_word,list_paragraphs):
    paragraphs_w_keyword = []
    for i,paragraph in enumerate(list_paragraphs):
        if key_word.strip().lower() in paragraph.lower():
            if paragraph.strip()[-1] != '.' and i != len(list_paragraphs)-1: # the sentence is not ending
                new_paragraph = paragraph + list_paragraphs[i+1]
            elif paragraph.strip()[0].islower(): #the sentence has the other half in previous paragraph due to page break
                new_paragraph = list_paragraphs[i-1] + paragraph
            else:
                new_paragraph = paragraph
            paragraphs_w_keyword.append(new_paragraph)
    return paragraphs_w_keyword

def file_search_keyword(key_word, file_name):
    result_dict = {}
    with open(file_name) as fp:
        try:
            file_soup = BeautifulSoup(fp, "html.parser")
        except:
            return None
    list_of_paras = extract_text_to_list(file_soup)
    search_list = search_keyword(key_word,list_of_paras)
    if len(search_list) > 0:
        result_dict[key_word] = search_list
        return result_dict
    else:
        return None

def find_relative_filenames(path,start_date,end_date):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    file_names = [path+'/'+fn for fn in os.listdir(path) if fn.lower().endswith('html') and datetime.strptime(fn[:10], '%Y-%m-%d')>=start_datetime and datetime.strptime(fn[:10], '%Y-%m-%d')<=end_datetime]
    return file_names

def search_keyword_files(relevant_path, keyword_list, start_year="2008-01-01", end_year="2018-12-31"):
    filename_list = find_relative_filenames(relevant_path,start_year,end_year)
    search_results_dict = {}
    for file in filename_list:
        file_results_dict={} 
        for keyword in keyword_list:
            print("Searching keyword",keyword,"in file:",file)
            key_word_search_result = file_search_keyword(keyword, file)
            if key_word_search_result is not None:
                file_results_dict.update(key_word_search_result)
        search_results_dict[file] = file_results_dict
    return search_results_dict
