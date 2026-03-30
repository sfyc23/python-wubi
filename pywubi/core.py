#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from .utils import single_seg, combin_seg
from .constants import RE_HANS
from .loader import get_wubi_dict


def single_wubi(han: str, multicode: bool = False) -> str | list[str]:
    """将单个汉字转成五笔编码。

    :param han: 单个汉字
    :param multicode: 是否返回多个编码。
        True  — 返回该汉字的所有五笔编码列表。
        False — 返回最长的那个编码字符串。
    """
    if len(han) > 1:
        return combine_wubi(han)
    wubi_dict = get_wubi_dict()
    codes = wubi_dict.get(han)
    if codes is None:
        return han
    if not multicode:
        return codes[0]
    return list(codes)


def combine_wubi(hans: str) -> str:
    """将词组转成五笔编码。

    取码规则：
    - 二字词：各取前两码
    - 三字词：前两字各取首码 + 第三字取前两码
    - 四字及以上：取第 1、2、3、末字的首码
    """
    length = len(hans)
    if length == 1:
        result = single_wubi(hans)
        return result if isinstance(result, str) else result[0]
    elif length == 2:
        return single_wubi(hans[0])[:2] + single_wubi(hans[1])[:2]
    elif length == 3:
        return (single_wubi(hans[0])[0]
                + single_wubi(hans[1])[0]
                + single_wubi(hans[2])[:2])
    else:
        return (single_wubi(hans[0])[0]
                + single_wubi(hans[1])[0]
                + single_wubi(hans[2])[0]
                + single_wubi(hans[-1])[0])


# 向后兼容旧 API 名称
conbin_wubi = combine_wubi


def wubi(hans: str, multicode: bool = False, single: bool = True) -> list[str | list[str]]:
    """将汉字转换成五笔编码。

    :param hans: 汉字字符串（如 '我爱你'）或单个字符（如 '滚'）
    :param multicode: 是否返回多个编码。
        True  — 返回每个汉字的所有五笔编码。
        False — 返回每个汉字最长的编码。
    :param single: 是否以单个字符处理。
        True  — 逐字转码。
        False — 以词组方式取码。
    :return: 五笔编码列表

    Usage::
    >>> from pywubi import wubi
    >>> wubi('我爱你')
    ['trnt', 'epdc', 'wqiy']
    >>> wubi('我爱你', multicode=True)
    [['trnt', 'trn', 'q'], ['epdc', 'epd', 'ep'], ['wqiy', 'wqi', 'wq']]
    >>> wubi('我爱你', single=False)
    ['tewq']
    """
    res: list[str | list[str]] = []
    if single:
        han_list = single_seg(hans)
        for han in han_list:
            if RE_HANS.match(han):
                res.append(single_wubi(han, multicode))
            else:
                res.append(han)
    else:
        han_list = combin_seg(hans)
        for han in han_list:
            if RE_HANS.match(han):
                res.append(combine_wubi(han))
            else:
                res.append(han)
    return res
