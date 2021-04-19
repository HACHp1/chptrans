import win32clipboard as wc #读取剪切板数据
from pynput.keyboard import Listener
import pyautogui

import tkinter         #自带的GUI库，生成文本框

currentData='' 


#获得剪切板数据    
def getCopyText():
    wc.OpenClipboard()
    copy_text = wc.GetClipboardData()
    wc.CloseClipboard()
    return copy_text


def on_press(key):
    if str(key)=='\'f\'': # 按f键翻译

        currentData=str(getCopyText())#取得当前剪切板数据
            
        ### 翻译 ###

        translate_results = currentData
        x,y=pyautogui.position()

        position="500x400+"+str(x)+"+"+str(y) #取得当前鼠标位置
        top = tkinter.Tk()#窗口初始化
        top.wm_attributes('-topmost',1)#置顶窗口
        top.geometry(position)#指定定位生成指定大小窗口
        e=tkinter.Text()#生成文本框部件
        e.insert(1.0,translate_results)#插入数据
        e.pack()#将部件打包进窗口
        top.mainloop()# 进入消息循环





if __name__ == '__main__':
    # 创建要提交的数据
    currentData=str(getCopyText())
    
    with Listener(on_press=on_press) as listener:
        listener.join()     
    
              