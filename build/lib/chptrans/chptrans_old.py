# encoding=utf-8
import requests
import json
import sys
import os
import brotli

url = 'https://cn.bing.com/ttranslatev3?isVertical=1&IID=translator.5028.1'
headers = {
    'Host': 'cn.bing.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.bing.com/ttranslate?mkt=zh-CN',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers'
}


sess = requests.session()


# 传入url编码过的英文内容
def mytranslate(content):
    # print(content)
    data = {
        'fromLang':'en',
        'text': content,
        'from': 'en',
        'to': 'zh-Hans'
    }
    result = sess.post(url, data=data, headers=headers)
    result.encoding = result.apparent_encoding 
    try:
        # print(result.status_code)
        # print(result.headers)
        chi_json  = brotli.decompress(result.content)
        chi_json=json.loads(str(chi_json,encoding='utf8'))
        raw_res=chi_json[0]['translations'][0]['text']
        # exit()
        result = raw_res.replace('。', '。\n')

    except KeyError:
        print('查询有误\n')
    return result


def main():
    if (len(sys.argv) == 2):
        if (sys.argv[1] == 'ia'):
            strings = ''
            laststrings = ''  # 记录上一个字符串
            while (1):
                string = input('\n请输入待翻译的英文；输入"退出"退出，"翻译"翻译，"重复"重新翻译：\n')
                os.system('cls')
                if (string == '退出'):
                    break
                elif (string == '翻译'):
                    laststrings = strings
                    print(mytranslate(strings))
                    strings = ''
                elif (string == '重复'):
                    print(mytranslate(laststrings))
                else:
                    strings += ' ' + string
        else:
            string = ''
            engsfile = sys.argv[1]
            with open(engsfile) as f:
                strings = f.readlines()
            for vstr in strings:
                string += vstr.replace('\n', ' ')
            print(mytranslate(string))
    elif (len(sys.argv) == 3):
        string = ''
        engsfile = sys.argv[1]
        wfile = sys.argv[2]
        with open(engsfile) as f:
            strings = f.readlines()
        fw = open(wfile, 'w', encoding='gbk')
        for vstr in strings:
            string += vstr.replace('\n', ' ')
        translated = mytranslate(string)
        fw.write(translated)
        print(translated)
        fw.close()

    else:
        print('''
***************************************************************************************
        欢迎使用 CHP's translator
            用法：
            1、python chptrans.py 1.txt（英文文件）
                此时将输出1.txt的翻译
            2、python chptrans.py 1.txt（英文文件） 2.txt（将会把翻译的中文写入的文件）
                此时将1.txt的翻译输出，并将其保存至2.txt
            3、python chptrans.py ia（ia等于interactive，交互模式）
                进入交互模式，输入待翻译的英文并回车后，单独输入"翻译"并回车即可翻译。
                单独输入"退出"并回车即可退出程序。
        感谢：
            感谢Bing的接口
***************************************************************************************
        ''')


if __name__ == '__main__':
    # print(mytranslate('I will take a test tomorrow!'))
    main()