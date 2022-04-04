import os
import re
from bs4 import *

def replace_id(_string):
    index_left = _string.index('}')
    temp= _string[index_left + 1:].replace(" ","_")
    for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
        temp = temp.replace(*r)
        temp = temp.replace("\"","")
        temp = temp.replace("\n", "")
    return temp.lower()

def replace_id_no_id(_string):
    index_left = _string.index('=')
    temp= _string[index_left + 1:].replace(" ","_")
    for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
        temp = temp.replace(*r)
        temp = temp.replace("\"","")
        temp = temp.replace("\n", "")
    return temp.lower()

def get_string(_string):
    index_left = _string.index('}')
    temp = _string[index_left + 1:]
    return temp

def get_id(_string):
    index_left = _string.index('\"')
    temp = _string[index_left + 1:]
    return temp

def get_string_no_id(_string):
    index_left = _string.index('=')
    temp = _string[index_left + 1:]
    return temp.replace("\"","")

# 路径
path = 'c:/Users/Administrator/PycharmProjects/pythonProject/viking storm/'
path_CNs = 'c:/Users/Administrator/PycharmProjects/pythonProject/viking storm_CNs/'
# 文件列表
files = []
matches = ["tag","Mesh","Material","flag","FIRSTNAME"]
for file in os.listdir(path):
    if file.endswith(".xml"):
        print(file)
        nf_name = 'new_' + file
        nf = open(path_CNs+file, "w+", encoding='utf-8')
        with open(path+file, 'r', encoding='utf8')as f:
            origin_lines = f.readlines()
        for origin_line in origin_lines:
            if any(x in origin_line for x in matches):
                nf.write(origin_line)
                continue
            # if 'tag' not in origin_line:
            else:
                if 'name' in origin_line:
                    original_names = re.search(' name=.+?(?=")', origin_line)
                    original_name = original_names.group(0) if original_names else ""
                    print(original_name)
                if 'id=' in origin_line:
                    original_ids = re.search('id=.+?(?=")', origin_line)
                    original_id = original_ids.group(0) if original_ids.group else ""
                    print(original_id)

                if ' name="{' in origin_line:
                    origin_name = get_string(original_name)
                    replacement = get_id(original_id)

                    origin_line = re.sub(' name=.+?(?=")', ' name=\"{=' + replacement + '}' + origin_name, origin_line)
                elif ' name=' in origin_line:
                    origin_name = get_string_no_id(original_name)
                    replacement = get_id(original_id)

                    origin_line = re.sub(' name=.+?(?=")', ' name=\"{=' + replacement + '}' + origin_name, origin_line)
                elif '*' in origin_line:

                    origin_name = get_string(original_name)
                    replacement = get_id(original_id)

                    origin_line = re.sub('\*', replacement, origin_line)
            nf.write(origin_line)