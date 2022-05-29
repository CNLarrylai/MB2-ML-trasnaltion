import os
import re
from bs4 import *

# 路径
path = 'D:/汉化作品/时光之轮1.7.1/Wheel of Time Mod - MAIN FILE/ModuleData/'
#path_CNs = 'c:/Users/Administrator/PycharmProjects/pythonProject/Wheel of Time Mod - MAIN FILE - IDs/'
path_CNs_IDs = 'D:/汉化作品/时光之轮1.7.1/Wheel of Time Mod - MAIN FILE/ModuleData/Languages/'
# 文件列表
files = []
matches = ["tag","Mesh","Material","flag","FIRSTNAME","name name","template","Plural"]

if not os.path.exists(path_CNs_IDs): os.mkdir(path_CNs_IDs)

def replace_id(_string):
    index_left = _string.index('}')
    temp= _string[index_left + 1:].replace(" ","_")
    if "," in temp:
        temp = temp[:temp.index(",")]
    for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
        temp = temp.replace(*r)
        temp = temp.replace("\"","")
        temp = temp.replace("\n", "")
    return temp.lower()

def replace_id_no_id(_string):
    index_left = _string.index('=')
    temp= _string[index_left + 1:].replace(" ","_")
    if "," in temp:
        temp = temp[:temp.index(",")]
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


#---------------------------------------------------------------------------------------------
# 从xml文本里面提取需要翻译的key
def get_id_to_extract(_string):
    #print(_string)
    if '}' in _string:
        index_right = _string.index('}')
        index_left = _string.index('=')
        temp = _string[index_left + 1:index_right].replace(" ","_")
        return temp.replace("'","_")
    else :
        return ""



for file in os.listdir(path):
    #print(file)
    strings = list()
    with open("template.xml", "r", encoding='utf-8') as f:
        template = BeautifulSoup(f.read(), 'xml')
    common = template.find('strings')
    if file.endswith(".xml"):
        with open(path+file, 'r', encoding='utf8')as f:
            origin_lines = f.readlines()
        for origin_line in origin_lines:

            if any(x in origin_line for x in matches):
                continue
            else:
                strings_src = re.findall(r'"(.*?)"', origin_line)
            for string in strings_src:

                if '=' in string:
                    #print(string)
                    strings.append(string)
        # print("strings are:")
        # print(strings)

        for string in strings:
            # enable this line to make new id from name
            # tag = template.new_tag(name='string', attrs={'id': replace_id(string).lower(), 'text': get_string(string)})
            # enable this line to read original String IDs
            if '}' in string:
                tag = template.new_tag(name='string', attrs={'id': get_id_to_extract(string), 'text': get_string(string)})
                common.append(tag)
        new_name = file[:file.index(".")]+"_CNs.xml"

        with open(path_CNs_IDs+new_name, "w+", encoding='utf-8') as f:
            f.write(template.prettify())
