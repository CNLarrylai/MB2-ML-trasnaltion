import re
from bs4 import *
filename="totsk_spkingdoms.xml"

with open(filename, "r", encoding='utf-8') as f:
    origin_lines = f.readlines()

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

def get_string_no_id(_string):
    index_left = _string.index('=')
    temp = _string[index_left + 1:]
    return temp.replace("\"","")

with open(filename, "w+", encoding='utf-8') as nf:
     for origin_line in origin_lines:
            print("original line is："+origin_line)
            if 'name="{' in origin_line:

                print("line need will be replaced:"+origin_line)
                #test=re.findall(' name=.+?(?=")',origin_line)
                test = re.findall('name=.+?(?=")', origin_line)
                print("the extracted sentence is:" + test[0])
                #print("line need will be replaced:"+test)
                #print(test)
                string=test[0]
                #print(string)
                origin_name=get_string(string)
                replacement=replace_id(string)
                # print(string)
                # print(origin_name)
                #print(replacement)
                origin_line=re.sub('name=.+?(?=")','name=\"{='+replacement+'}'+origin_name,origin_line)
                #origin_line = '    name=\"{='+str(replacement)+'}'+str(origin_name)
                print(origin_line)

            elif ' name=' in origin_line:
                #print(origin_line)
                test=re.findall(' name=.+?(?=")',origin_line)
                #print(test)
                string = test[0]

                origin_name = get_string_no_id(string)
                replacement = replace_id_no_id(string)

                origin_line=re.sub(' name=.+?(?=")',' name=\"{='+replacement+'}'+origin_name,origin_line)

                elif ' name=' in origin_line:
                # print(origin_line)
                test = re.findall(' name=.+?(?=")', origin_line)
                # print(test)
                string = test[0]

                origin_name = get_string_no_id(string)
                replacement = replace_id_no_id(string)

                origin_line = re.sub(' name=.+?(?=")', ' name=\"{=' + replacement + '}' + origin_name, origin_line)
            nf.write(origin_line)



# with open("wild_notables.xml", "r", encoding='utf-8') as f:
#     origin_content = f.read()
# strings_src = re.findall(r'"(.*?)"', origin_content)
# strings = list()
# for string in strings_src:
#     if '=' in string:
#         strings.append(string)
#
# #with open("template.xml", "r", encoding='utf-8') as f:
# #    template = BeautifulSoup(f.read(), 'xml')
# #common = template.find('strings')
#
#
# def get_id(_string):
#     index_right = _string.index('}')
#     index_left = _string.index('=')
#     temp = _string[index_left + 1:index_right].replace(" ","_")
#     return temp.replace("'","_")
#
# def replace_id(_string):
#     index_left = _string.index('}')
#     temp= _string[index_left + 1:].replace(" ","_")
#     for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
#         temp = temp.replace(*r)
#
#     return temp
#
# def get_string(_string):
#     index_left = _string.index('}')
#     return _string[index_left + 1:]
#
#
# for string in strings:
#     # enable this line to make new id from name
#     #tag = template.new_tag(name='string', attrs={'id': replace_id(string).lower(), 'text': get_string(string)})
#
#     # enable this line to read original String IDs
#     #tag = template.new_tag(name='string', attrs={'id': get_id(string), 'text': get_string(string)})
#
#     #given by jiaxin
#     to_string=replace_id(string)
#     origin_content=re.sub(string,to_string,origin_content)
#
#
#     common.append(tag)
#
#
# with open("wild_notables_EN.xml", "w+", encoding='utf-8') as f:
#     f.write(template.prettify())
