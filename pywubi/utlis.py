# from __future__ import unicode_literals

from pywubi.constants import RE_HANS


def combin_seg(chars):
    '''
    对字符进行分割，能组合的字放一起。
    :param chars:
    :return:
    '''
    s = ''  # 保存一个词
    ret = []  # 分词结果
    flag = 0  # 上一个字符是什么? 0: 汉字, 1: 不是汉字

    for n, c in enumerate(chars):
        if RE_HANS.match(c):  # 汉字, 确定 flag 的初始值
            if n == 0:  # 第一个字符
                flag = 0

            if flag == 0:
                s += c
            else:  # 上一个字符不是汉字, 分词
                ret.append(s)
                flag = 0
                s = c

        else:  # 不是汉字
            if n == 0:  # 第一个字符, 确定 flag 的初始值
                flag = 1

            if flag == 1:
                s += c
            else:  # 上一个字符是汉字, 分词
                ret.append(s)
                flag = 1
                s = c

    ret.append(s)  # 最后的词
    return ret



def single_seg(chars):
    '''
    对字符进行分组。切割成单个字符
    :param chars:
    :return:
    '''
    res = []
    s = ''
    for c in chars:
        if RE_HANS.match(c):  # 汉字, 确定 flag 的初始值
            if s:
                res.append(s)
                s = ''
            res.append(c)
        else:
            s += c
    return res
