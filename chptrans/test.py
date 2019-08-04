
from pynput.keyboard import Listener

def on_press(key):
    # 监听按键
    print(str(key))
    if str(key)=='Key.ctrl_l':
        print('123')

with Listener(on_press=on_press) as listener:
    listener.join()