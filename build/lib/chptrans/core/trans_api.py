import json
import re
import requests
import brotli
import urllib
from .utils import re_split

from .BaiduTranslate import TransDict

'''
翻译器api
传入url编码过的英文内容字符串
传出中文内容字符串
'''


def translate_bing_api(content):
    content = content.replace('"', '\'')
    data = {}
    data['from'] = '"en"'
    data['to'] = '"zh"'
    data['texts'] = '["'
    data['texts'] += content
    data['texts'] += '"]'
    data['options'] = "{}"
    data['oncomplete'] = 'onComplete_3'
    data['onerror'] = 'onError_3'
    data['_'] = '1430745999189'
    data['appId'] = '"3DAEE5B978BA031557E739EE1E2A68CB1FAD5909"'

    data = urllib.parse.urlencode(data).encode('utf-8')
    strUrl = "http://api.microsofttranslator.com/v2/ajax.svc/TranslateArray2?" + data.decode()

    response = requests.get(strUrl)
    str_data = response.text
    try:
        tmp, str_data = str_data.split('"TranslatedText":')
        translate_data = str_data[1:str_data.find('"', 1)]
    except ValueError:
        translate_data = 'Bing接口请求过快，请一分钟后再翻译。'

    return translate_data


def translate_bing(content):
    url = 'https://cn.bing.com/ttranslatev3?isVertical=1&=&IG=43F6EAE362AC485D8E0BF54A0F50F65D&IID=translator.5023.1'

    headers = {
        'Host': 'cn.bing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/107.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://cn.bing.com/translator',
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': '927',
        'Origin': 'https://cn.bing.com',
        'Connection': 'close',
        'Cookie': 'MUID=0FC1DA47D10C651B259BC81BD0B664E7; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=9AB6F7E5646A4786B569618A5F59C9DC&dmnchg=1; SRCHUSR=DOB=20221114&T=1668562992000; SRCHHPGUSR=SRCHLANG=zh-Hans&HV=1668563603&WTS=63804159792; _tarLang=default=zh-Hans; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJ6aC1IYW5zIl0=; SUID=M; _EDGE_S=SID=16FA16E71A4C66E939B804B91BF667B6; _SS=SID=16FA16E71A4C66E939B804B91BF667B6; ipv6=hit=1668566595271&t=4; btstkn=S01zalQ7p%252B2YrnqgczdHOZw%252B6XsIGWbad61FcQGvtZKrF%252BsraySWpl0jLYkK2AuxiHVPd1K%252B7UWFLBOQB5yfgna6BjbkjOYn7EBKf5PZFBM%253D; SNRHOP=I=&TS=; MUIDB=0FC1DA47D10C651B259BC81BD0B664E7',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    data = {
        'fromLang': 'en',
        'text': content,
        'to': 'zh-Hans',
        'token': '5iIThOcjbkBquoI1iWnDyetbweEq_dyS',
        'key': '1668563596751'
    }

    try:
        res = requests.post(url, data=data, headers=headers)
        ts = json.loads(res.text)
        translate_data = ts[0]['translations'][0]['text']
    except ValueError:
        translate_data = 'Bing接口请求过快，请一分钟后再翻译。'
    return translate_data


def translate_youdao(content):

    seg_content = re_split(content, '([.?]\s)')
    transres = ''

    for vcontent in seg_content:
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=https://www.baidu.com/link'
        data = {'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict', 'client': 'fanyideskweb', 'salt': '1500092479607',
                'sign': 'c98235a85b213d482b8e65f6b1065e26', 'doctype': 'json', 'version': '2.1', 'keyfrom': 'fanyi.web',
                'action': 'FY_BY_CL1CKBUTTON', 'typoResult': 'true', 'i': vcontent}

        data = urllib.parse.urlencode(data).encode('utf-8')
        wy = urllib.request.urlopen(url, data)
        html = wy.read().decode('utf-8')
        ta = json.loads(html)

        transres += ta['translateResult'][0][0]['tgt']+' '

    return transres


def translate_baidu(content):

    d = TransDict()

    json = d.dictionary(content, dst='zh', src='en')

    try:
        res = json['trans_result']['data'][0]['dst']
    except KeyError:
        res = '请求过快，请稍后重试'

    return res

# 翻译器列表


translators = [
    translate_bing,
    translate_baidu,
    translate_youdao,
]
