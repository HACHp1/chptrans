# encoding=utf-8

from setuptools import setup, find_packages

setup(
    name="chptrans",
    version="0.3",
    keywords=("chptrans"),
    description="翻译pdf英文论文用的小工具，避免换行符的尴尬，免去打开浏览器的过程，命令行操作",
    long_description=
    '''
    翻译pdf论文用，支持三种模式（交互，文本翻译输出，文本翻译至文本。主要功能：换行变空格；
	
	0.2版本更新：增加重复功能，对服务器接口翻译不完全的情况进行重新翻译操作。
    ''',
    license="MIT Licence",

    url="",
    author="CHP",
    author_email="hachp1@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="windows",
    install_requires=['requests>=2.18.1','brotli','pynput','pyautogui'],

    #scripts=['scripts/chptrans.py'],
    entry_points={
        'console_scripts': [
            'chptrans = chptrans.chptrans:main'
        ],
    }
)
