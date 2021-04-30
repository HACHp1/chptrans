import json
import requests
import brotli
import urllib
from .utils import re_split

'''
翻译器api
传入url编码过的英文内容字符串
传出中文内容字符串
'''


def translate_bing(content):
    url = 'https://cn.bing.com/ttranslatev3?isVertical=1&IID=translator.5028.1'
    headers = {
        'Host': 'cn.bing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'br',
        'Referer': 'https://www.bing.com/ttranslate?mkt=zh-CN',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers'
    }
    # print(content)
    if content == '':
        return '查询不能为空\n'

    data = {
        'fromLang': 'en',
        'text': content,
        'from': 'en',
        'to': 'zh-Hans'
    }

    while 1:
        try:
            result = requests.post(url, data=data, headers=headers)
            break
        except Exception as e:  # 连接失败则重试
            print(e)

    result.encoding = result.apparent_encoding
    try:
        chi_json = brotli.decompress(result.content)
        chi_json = json.loads(str(chi_json, encoding='utf8'))
        raw_res = chi_json[0]['translations'][0]['text']
    except brotli.error:
        chi_json = json.loads(str(result.content, encoding='utf8'))
        raw_res = chi_json[0]['translations'][0]['text']
    except KeyError:
        raw_res = '查询有误或查询过快\n'
    return raw_res


def translate_youdao(content):

    seg_content=re_split(content,'([.?]\s)')
    transres=''

    for vcontent in seg_content:
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=https://www.baidu.com/link'
        data = {'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict', 'client': 'fanyideskweb', 'salt': '1500092479607',
                'sign': 'c98235a85b213d482b8e65f6b1065e26', 'doctype': 'json', 'version': '2.1', 'keyfrom': 'fanyi.web',
                'action': 'FY_BY_CL1CKBUTTON', 'typoResult': 'true', 'i': vcontent}

        data = urllib.parse.urlencode(data).encode('utf-8')
        wy = urllib.request.urlopen(url, data)
        html = wy.read().decode('utf-8')
        ta = json.loads(html)

        transres+=ta['translateResult'][0][0]['tgt']+' '
    
    return transres

# 翻译器列表

translators = [
    translate_bing,
    translate_youdao
] 