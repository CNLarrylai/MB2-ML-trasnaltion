import re
from bs4 import *
#从xml文本里面提取需要翻译的key
with open("spnpccharactersGHK.xml", "r", encoding='utf-8') as f:
    origin_content = f.read()
strings_src = re.findall(r'"(.*?)"', origin_content)
strings = list()
for string in strings_src:
    if '=' in string:
        strings.append(string)

with open("template.xml", "r", encoding='utf-8') as f:
    template = BeautifulSoup(f.read(), 'xml')
common = template.find('strings')


def get_id(_string):
    index_right = _string.index('}')
    index_left = _string.index('=')
    temp = _string[index_left + 1:index_right].replace(" ","_")
    return temp.replace("'","_")

def replace_id(_string):
    index_left = _string.index('}')
    temp= _string[index_left + 1:].replace(" ","_")
    for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
        temp = temp.replace(*r)

    return temp

def get_string(_string):
    index_left = _string.index('}')
    return _string[index_left + 1:]


for string in strings:
    # enable this line to make new id from name
    #tag = template.new_tag(name='string', attrs={'id': replace_id(string).lower(), 'text': get_string(string)})

    # enable this line to read original String IDs
    tag = template.new_tag(name='string', attrs={'id': get_id(string), 'text': get_string(string)})
    common.append(tag)


with open("spnpccharactersGHK_cnS.xml", "w+", encoding='utf-8') as f:
    f.write(template.prettify())
