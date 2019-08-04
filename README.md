# chptrans

## 功能
* 弹窗翻译pdf英文论文用的小工具，避免换行符的尴尬，免去打开浏览器的过程，翻译只需三个键，妈妈再也不用担心我看论文原文了:)
* **使用Bing接口，感谢Bing提供的接口**


## 安装方法
* 安装前请使用pip安装brotli、pynput、pyautogui以及requests库
```
python setup.py build
python setup.py install
```

## 用法：
```
            复制想翻译的英文（ctrl+c)，复制完后按f键翻译（翻译器会将剪切板中的内容翻译为中文）
```	

## 使用截图
![](show.png)

## 更新日志
* 2019.5.15 百度接口失效，改用Bing接口。
* 2019.6.25 Bing接口更新，加入firefox头部和brotli解码。
* 2019.7.16 Bing接口更新，改用Bing接口V3。
* 2019.8.4 程序功能更新，直接使用弹窗和按键，操作方便快捷。