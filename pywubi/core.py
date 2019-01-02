#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywubi.utlis import (
    single_seg, combin_seg
)

from pywubi.constants import (
    WUBI_86_DICT,
    RE_HANS
)

def single_wubi(han, multicode=False):
    '''
    将单个汉字转成五笔编码
    :param han: str ,单个汉字
    :param multicode: bool,是否返回多个编码
                     如果 True,返回这个汉字的所有五笔编码。
                    如果 False，返回这个汉字编码中最长的。
                    默认为 False
    :return: str or list.
            如果 multicode = True，返回此汉字的所有编码。
            如果 multicode = False ，返回单个五笔编码
    '''
    if len(han) > 1:
        return conbin_wubi(han)
    num = ord(han)
    if num not in WUBI_86_DICT:
        return han
    pys = WUBI_86_DICT[num].split(',')  # 字的拼音列表
    if not multicode:
        return pys[0]
    return pys


def conbin_wubi(hans):
    '''
    将词组转成五笔编码
    :param hans:str,词组
    :return: str ,五笔编码
    '''
    len_han = len(hans)
    if len_han == 1:
        return single_wubi(hans)
    elif len_han == 2:
        s = ''
        s += single_wubi(hans[0])[:2]
        s += single_wubi(hans[1])[:2]
        return s
    elif len_han == 3:
        s = ''
        s += single_wubi(hans[0])[0]
        s += single_wubi(hans[1])[0]
        s += single_wubi(hans[2])[:2]
        return s
    elif len_han >= 4:
        s = ''
        s += single_wubi(hans[0])[0]
        s += single_wubi(hans[1])[0]
        s += single_wubi(hans[2])[0]
        s += single_wubi(hans[-1])[0]
        return s


# style=Style.WUBI_86，errors='default'
def wubi(hans, multicode=False, single=True):
    '''
    将汉字转换成五笔编码
    :param hans: str,  汉字字符串（'我爱你'），或单个字符（'滚'）
    :param multicode: bool,是否启用多编码：
                    如果 True,返回这个汉字的所有五笔编码。
                    如果 False，返回这个汉字编码中最长的。
                    默认为 False
    :param single:  bool，是否以单个字符处理
                    True,以单个字符处理
                    False,则为词组做处理。
                    默认为 True
    :return: list,五笔列表

    Usage::
    >>> from pywubi import wubi
    >>> wubi('我爱你')
    ['trnt', 'epdc', 'wqiy']
    >>> wubi('我爱你',multicode=True)
    [['trnt', 'trn', 'q'], ['epdc', 'epd', 'ep'], ['wqiy', 'wqi', 'wq']]
    >>> wubi('我爱你', single=False)
    ['tewq']
    '''
    res = []
    if single:
        # 将可以找到编码的单个汉字，
        han_list = single_seg(hans)
        for han in han_list:
            if RE_HANS.match(han):
                res.append(single_wubi(han, multicode))
            else:
                res.append(han)
    else:
        # 将可以找到编码的汉字进行分词，
        han_list = combin_seg(hans)
        for han in han_list:
            if RE_HANS.match(han):
                res.append(conbin_wubi(han))
            else:
                res.append(han)
    return res


# if __name__ == '__main__':
#
#     ret = wubi('我爱你')
#     print(ret)
#     ret = wubi('为',multicode=True)
#     print(ret)
#     ret = wubi('天气不错，我们去散步吧', single=True)
#
#     print(ret)
