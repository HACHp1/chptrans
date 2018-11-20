# encoding=utf-8
import requests
import json
import sys
import os


def mytranslate(content):
    url = 'https://fanyi.baidu.com/transapi?from=auto&to=zh&query=' + content
    result = requests.get(url)
    try:
        result = json.loads(result.text)['data'][0]['dst'].replace('。', '。\n')
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
        欢迎使用 CHP's translator v1.0
            用法：
            1、python chptrans.py 1.txt（英文文件）
                此时将输出1.txt的翻译
            2、python chptrans.py 1.txt（英文文件） 2.txt（将会把翻译的中文写入的文件）
                此时将1.txt的翻译输出，并将其保存至2.txt
            3、python chptrans.py ia（ia等于interactive，交互模式）
                进入交互模式，输入待翻译的英文并回车后，单独输入"翻译"并回车即可翻译。
                单独输入"退出"并回车即可退出程序。
***************************************************************************************
        ''')


if __name__ == '__main__':
    main()
