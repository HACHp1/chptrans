# chptrans

## 功能
* 翻译pdf英文论文用的小工具，避免换行符的尴尬，免去打开浏览器的过程，命令行操作
* 支持三种模式（交互，文本翻译输出，文本翻译至文本。主要功能：换行变空格）
* **使用Bing接口，感谢Bing提供的接口**


## 安装方法
* 安装前请使用pip安装brotli以及requests库
```
python setup.py build
python setup.py install
```

## 用法（推荐用3）：
```
            1、chptrans 1.txt（英文文件）
                此时将输出1.txt的翻译
            2、chptrans 1.txt（英文文件） 2.txt（将会把翻译的中文写入的文件）
                此时将1.txt的翻译输出，并将其保存至2.txt
            *3*、chptrans ia（ia等于interactive，交互模式）
                进入交互模式，输入待翻译的英文并回车后，单独输入"翻译"并回车即可翻译。
                单独输入"退出"并回车即可退出程序。
```	

## 更新日志
* 2019.5.15 百度接口失效，改用Bing接口。
* 2019.6.25 Bing接口更新，加入firefox头部和brotli解码。
* 2019.7.16 Bing接口更新，改用Bing接口V3。