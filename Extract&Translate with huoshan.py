import re
from bs4 import *
import requests
import random
import json
from hashlib import md5
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
import time

# 设置翻译API的账号和密码 Huoshan https://www.volcengine.com/docs
k_access_key = "paste your access key here"
k_secret_key = "paste your secret key here"
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


#前面都是调用翻译API的部分 Everything about machine translation is above

#下面是提取XML的部分 Everything about extracting texts from Xmls is underneath


#从xml文本里面提取需要翻译的key
with open("sandboxcore_spnpccharacters.xml", "r", encoding='utf-8') as f:
    origin_content = f.read()
strings_src = re.findall(r'"(.*?)"', origin_content)
strings = list()
for string in strings_src:
    if '=' in string:
        strings.append(string)

#从打开模板XML
with open("templateCNs.xml", "r", encoding='utf-8') as f:
    template = BeautifulSoup(f.read(), 'xml')
common = template.find('strings')

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



for string in strings:
    # enable this line to make new id from name
    #tag = template.new_tag(name='string', attrs={'id': replace_id(string).lower(), 'text': get_string(string)})
    original = get_string(string)
    translation = translate(original)
    # enable this line to read original String IDs
    tag = template.new_tag(name='string', attrs={'id': get_id(string), 'text': translation})
    common.append(tag)
    time.sleep(0.05)

with open("sandboxcore_spnpccharacters_CNs.xml", "w+", encoding='utf-8') as f:
    f.write(template.prettify())
