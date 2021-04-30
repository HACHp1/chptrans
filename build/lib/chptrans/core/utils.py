import re

def re_split(content,re_par='([.?])\s'):
    '''
    保留分隔符的字符分割，注意保留的符号的正则需要加上小括号
    '''
    seg_content=re.split(re_par, content)
    values = seg_content[::2]
    delimiters = seg_content[1::2]+ ['']
    seg_content=[v + d for v,d in zip(values, delimiters)]

    return seg_content