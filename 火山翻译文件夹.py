import re
from bs4 import *
import os
import random
import json
from hashlib import md5
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
import time

# 路径
path_CNs = 'D:/汉化作品/卡拉迪亚的美好生活1.7.1/LifeInCalradia/ModuleData/Languages/'
path_CNs_IDs = 'D:/汉化作品/卡拉迪亚的美好生活1.7.1/LifeInCalradia/ModuleData/Languages/CNs/'

# 文件列表
files = []
matches = ["tag","Mesh","Material","flag","FIRSTNAME","name name","template","Plural"]


# 设置翻译API的账号和密码 Huoshan https://www.volcengine.com/docs
k_access_key = ""
k_secret_key = "=="
k_timeout = 5  # second

k_service_info = \
    ServiceInfo('open.volcengineapi.com',
                {'Content-Type': 'application/json'},
                Credentials(k_access_key, k_secret_key, 'translate', 'cn-north-1'),
                5,
                5)
k_query = {
    'Action': 'TranslateText',
    'Version': '2020-06-01'
}

k_api_info = {
    'translate': ApiInfo('POST', '/', k_query, {}, {})
}
service = Service(k_service_info, k_api_info)




#前面都是调用翻译API的部分



#下面是提取XML的部分


#从xml文本里面提取需要翻译的key

#获取提取前的string id
def get_id(_string):
    index_right = _string.index('}')
    index_left = _string.index('=')
    temp = _string[index_left + 1:index_right].replace(" ","_")
    return temp.replace("'","_")

#用text生成id并且替换
def replace_id(_string):
    index_left = _string.index('}')
    temp= _string[index_left + 1:].replace(" ","_")
    for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
        temp = temp.replace(*r)

    return temp


def get_string(_string):
    index_left = _string.index('}')
    return _string[index_left + 1:]

def get_id_to_extract(_string):
    index_right = _string.index('}')
    index_left = _string.index('=')
    temp = _string[index_left + 1:index_right].replace(" ","_")
    return temp.replace("'","_")


#translate single line
def translate(_string):
    print(_string)
    query = _string
    body = {
        'SourceLanguage': 'en',
        'TargetLanguage': 'zh',
        'TextList': [query],
    }
    r = service.json('translate', {}, json.dumps(body))
    # Send request
    result = json.loads(r)
    print(result)
    translate_result = result['TranslationList'][0]['Translation']
    print(translate_result)
    return translate_result

    # Show response
    #print(json.dumps(result, indent=4, ensure_ascii=False))

for file in os.listdir(path_CNs):
    print(file)
    if file.endswith(".xml"):
        strings = dict()
        with open("templateCNs.xml", "r", encoding='utf-8') as f:
            template = BeautifulSoup(f.read(), 'xml')
        common = template.find('strings')
        with open(path_CNs+file, 'r', encoding='utf8')as f:
            origin_lines = f.readlines()
        for origin_line in origin_lines:
            if any(x in origin_line for x in matches):
                continue
            elif 'id' in origin_line:

                #strings_src = re.findall(r'"(.*?)"', origin_line)
                strings_src = re.findall(r'"(.*?)"', origin_line)
                #print(strings_src)
                if strings_src:
                    strings[strings_src[0]]=strings_src[1]

        print(strings)
        for string in strings.keys():
            print(string)
            # enable this line to make new id from name
            # tag = template.new_tag(name='string', attrs={'id': replace_id(string).lower(), 'text': get_string(string)})
            # enable this line to read original String IDs
            tag = template.new_tag(name='string', attrs={'id': string, 'text': translate(strings[string])})
            common.append(tag)
        new_name = file[:file.index(".")]+"_CNs_translated.xml"

        with open(path_CNs_IDs+new_name, "w+", encoding='utf-8') as f:
            f.write(template.prettify())