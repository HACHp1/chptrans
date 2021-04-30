# encoding=utf-8

import xerox  # 读取剪切板数据
import keyboard
import pyautogui

import tkinter  # 自带的GUI库，生成文本框

from .core.trans_api import translators

currentData = ''

ch_en_mode = False  # 中英对照模式

translator_i = 0  # 当前翻译器index
translator_num = len(translators)  # 翻译器总数

mytranslate = translators[translator_i]  # 初始化翻译器


def getCopyText():
    '''
    获得剪切板数据
    '''
    try:
        copy_text = xerox.paste(xsel=True)
    except TypeError:
        copy_text = 'Please copy text!!!'
    except pywintypes.error:
        copy_text = 'Please copy text!!!'
    return copy_text


def on_press(vcmd):
    '''
    监听按键
    '''
    global ch_en_mode
    global translator_i
    global mytranslate

    if vcmd == 'translator': # 切换翻译器
        translator_i = (translator_i+1) % translator_num
        mytranslate=translators[translator_i]
        print('当前翻译器：'+mytranslate.__name__)

    elif vcmd == 'zh_en':  # 切换中英对照模式
        ch_en_mode = not ch_en_mode
        if ch_en_mode:
            print('当前模式：中英对照')
        else:
            print('当前模式：仅显示翻译')

    elif vcmd == 'fanyi':  # 按f键翻译

        currentData = str(getCopyText())  # 取得当前剪切板数据
        currentData = currentData.replace(
            '- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '').strip()
        ### 翻译 ###

        translate_results = mytranslate(currentData)

        if ch_en_mode:
            temp_curdata = currentData.split('. ')

            temp_seg = translate_results.split('。')
            if len(temp_seg) > 1:
                if temp_seg[-1] == '':
                    temp_ch = temp_seg[:-1]
                else:
                    temp_ch = temp_seg
            else:
                temp_ch = [translate_results]

            # print(len(temp_curdata), len(temp_ch))
            # assert (len(temp_curdata) == len(temp_ch))

            translate_results = ''
            try:
                for i in range(len(temp_curdata)):
                    translate_results = translate_results + \
                        temp_ch[i] + '。\n'+temp_curdata[i] + \
                        '. \n------------------------------------\n\n'
            except IndexError:
                translate_results = '中英分段数量不匹配，对照结果可能有误，请检查中英内容：\n\n'+translate_results

        else:
            translate_results = translate_results.replace('。', '。\n\n')

        ### 显示 ###
        x, y = pyautogui.position()

        position = "500x400+"+str(x)+"+"+str(y)  # 取得当前鼠标位置
        top = tkinter.Tk()  # 窗口初始化
        top.title("CHP's translator by HACHp1")
        top.wm_attributes('-topmost', 1)  # 置顶窗口
        top.geometry(position)  # 指定定位生成指定大小窗口
        top.configure(bg=('#%02x%02x%02x' % (199, 237, 204)))
        e = tkinter.Text()  # 生成文本框部件
        e.configure(bg=('#%02x%02x%02x' % (199, 237, 204)))
        e.insert(1.0, translate_results)  # 插入数据
        e.pack()  # 将部件打包进窗口
        top.mainloop()  # 进入消息循环


def main():
    '''
    主程序
    '''
    # 创建要提交的数据
    currentData = str(getCopyText())

    print('''
***************************************************************************************
        欢迎使用 CHP's translator
        用法：
            复制想翻译的英文（ctrl+c)，复制完后按f键翻译（翻译器会将剪切板中的内容翻译为中文）
            切换中英对照模式（ctrl+e）：方便进行单句的中英对比
            切换翻译器（ctrl+r）：目前支持Bing和有道
            按Esc键退出
        感谢：
            感谢Bing的接口
***************************************************************************************
        ''')

    # 注册按键热键
    keyboard.add_hotkey('f', on_press, args=('fanyi',))  # 翻译
    keyboard.add_hotkey('ctrl+e', on_press, args=('zh_en',))  # 中英对照模型切换
    keyboard.add_hotkey('ctrl+r', on_press, args=('translator',)) # 翻译器切换
    # 开始监听
    recorded = keyboard.record(until='esc')


if __name__ == '__main__':
    main()
