from urllib.parse import parse_qs
import re
import requests
import json

content = '''In this section, we propose some preliminary guiding
principles for using deep learning to detect vulnerabilities.
These principles are sufﬁcient for the present study, but may
need to be reﬁned to serve the more general purpose of deep
learning-based vulnerability detection. These principles are
centered at answering three fundamental questions: (i) How
to represent programs for deep learning-based vulnerability
detection? (ii) What is the appropriate granularity for deep
learning-based vulnerability detection? (iii) How to select a
speciﬁc neural network for vulnerability detection?
'''.replace(
    '- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '').strip()

# content = re.split('([.?])\s', content)


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

res = requests.post(url, data=data, headers=headers)
ts = json.loads(res.text)
print()