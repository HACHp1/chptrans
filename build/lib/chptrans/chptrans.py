# encoding=utf-8

import xerox  # 读取剪切板数据
import keyboard
import pyautogui

import tkinter  # 自带的GUI库，生成文本框

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
    'Accept-Encoding': 'br',
    'Referer': 'https://www.bing.com/ttranslate?mkt=zh-CN',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers'
}

currentData = ''

ch_en_mode = False  # 中英对照模式


def getCopyText():
    '''
    获得剪切板数据
    '''
    try:
        copy_text = xerox.paste()
    except TypeError:
        copy_text = 'Please copy text!!!'
    return copy_text


# 传入url编码过的英文内容
def mytranslate(content):
    # print(content)
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
        print('查询有误\n')
    return raw_res


def on_press(key):
    global ch_en_mode

    if key == 'ctrl+e':  # 切换中英对照模式
        ch_en_mode = not ch_en_mode
    elif key == 'f':  # 按f键翻译

        currentData = str(getCopyText())  # 取得当前剪切板数据
        currentData = currentData.replace(
            '- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '')
        ### 翻译 ###

        translate_results = mytranslate(currentData)

        if ch_en_mode:
            temp_curdata = currentData.split('. ')
            temp_ch = translate_results.split('。')[:-1]

            # print(len(temp_curdata), len(temp_ch))
            assert (len(temp_curdata) == len(temp_ch))

            translate_results = ''
            try:
                for i in range(len(temp_curdata)):
                    translate_results = translate_results + \
                        temp_ch[i] + '。\n'+temp_curdata[i]+'. \n------------------------------------\n\n'
            except IndexError:
                translate_results = '中英分段数量不匹配，请检查中英内容：\n'+translate_results

        else:
            translate_results = translate_results.replace('。', '。\n\n')

        ### 显示 ###
        x, y = pyautogui.position()

        position = "500x400+"+str(x)+"+"+str(y)  # 取得当前鼠标位置
        top = tkinter.Tk()  # 窗口初始化
        top.title("CHP's translator by HACHp1")
        top.wm_attributes('-topmost', 1)  # 置顶窗口
        top.geometry(position)  # 指定定位生成指定大小窗口
        e = tkinter.Text()  # 生成文本框部件
        e.insert(1.0, translate_results)  # 插入数据
        e.pack()  # 将部件打包进窗口
        top.mainloop()  # 进入消息循环


def main():
    # 创建要提交的数据
    currentData = str(getCopyText())

    print('''
***************************************************************************************
        欢迎使用 CHP's translator
        用法：
            复制想翻译的英文（ctrl+c)，复制完后按f键翻译（翻译器会将剪切板中的内容翻译为中文）
            切换中英对照模式（ctrl+e）：方便进行单句的中英对比
            按Esc键退出
        感谢：
            感谢Bing的接口
***************************************************************************************
        ''')

    # 注册按键热键
    keyboard.add_hotkey('f', on_press, args=('f',))  # 翻译
    keyboard.add_hotkey('ctrl+e', on_press, args=('ctrl+e',))  # 中英对照模型切换
    # 开始监听
    recorded = keyboard.record(until='esc')


if __name__ == '__main__':
    main()
