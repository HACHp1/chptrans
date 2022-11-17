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


class BingToken:
    key = None
    token = None
    ig = None
    sess = None
    initialed = False


bingToken = BingToken()


def translate_bing(content):

    global bingToken
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/107.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://cn.bing.com/translator',
    }

    if not bingToken.initialed:

        sess = requests.Session()
        res = sess.get('https://www.bing.com/translator', headers=headers)

        tmp_txt = res.text
        pos1 = tmp_txt.find('var params_RichTranslateHelper = ')
        pos2 = tmp_txt.find(';', pos1)
        pos3 = tmp_txt.find('"ig":"')
        pos4 = tmp_txt.find(',', pos3)

        t1 = tmp_txt[pos1+len('var params_RichTranslateHelper = '):pos2]
        t1 = json.loads(t1)
        t2 = tmp_txt[pos3:pos4]
        key = t1[0]
        token = t1[1]
        ig = t2[6:-1]

        bingToken.sess = sess
        bingToken.key = key
        bingToken.token = token
        bingToken.ig = ig

    data = {
        'fromLang': 'en',
        'text': content,
        'to': 'zh-Hans',
        'token': bingToken.token,
        'key': bingToken.key
    }

    url = f'https://cn.bing.com/ttranslatev3?isVertical=1&=&IG={bingToken.ig}&IID=translator.5023.1'
    res = sess.post(url, data=data, headers=headers)
    translate_data = json.loads(res.text)[0]['translations'][0]['text']

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
