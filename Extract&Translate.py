import re
from bs4 import *
import requests
import random
import json
from hashlib import md5

# 设置翻译API的账号和密码 BAIDU Setup your APIid and Appkey acquired from baidu API
appid = ''
appkey = ''

# 设置从A语音翻译到B语言，其他语言码查看  If you need more language code refer to:`https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

#组合翻译的地址 sent your translation to translate to here
endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

#example query
query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

# Generate salt and sign 组装校验码
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()




#前面都是调用翻译API的部分 Everything about machine translation is above



#下面是提取XML的部分 Everything about extracting texts from Xmls is underneath


#从xml文本里面提取需要翻译的key extract key from XML
with open("spclans.xml", "r", encoding='utf-8') as f:
    origin_content = f.read()
strings_src = re.findall(r'"(.*?)"', origin_content)
strings = list()
for string in strings_src:
    if '=' in string:
        strings.append(string)

#从打开模板XML open Template XML
with open("template.xml", "r", encoding='utf-8') as f:
    template = BeautifulSoup(f.read(), 'xml')
common = template.find('strings')

#获取提取前的string id Extract String ID before extraction
def get_id(_string):
    index_right = _string.index('}')
    index_left = _string.index('=')
    temp = _string[index_left + 1:index_right].replace(" ","_")
    return temp.replace("'","_")

#用text生成id并且替换 Generate new id based on old text
def replace_id(_string):
    index_left = _string.index('}')
    temp= _string[index_left + 1:].replace(" ","_")
    for r in ((" ", "_"), ("'", "_"),(":", "_"),(")", "_"),("(", "_")):
        temp = temp.replace(*r)

    return temp






def get_string(_string):
    index_left = _string.index('}')
    return _string[index_left + 1:]

def translate(_string):
    print(_string)
    query = _string
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    translate_result = result["trans_result"][0]["dst"]
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


with open("spclans_cnS.xml", "w+", encoding='utf-8') as f:
    f.write(template.prettify())
