#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from .constants import RE_HANS


def combin_seg(chars: str) -> list[str]:
    """对字符进行分割，能组合的汉字放一起，非汉字放一起。"""
    s = ''
    ret: list[str] = []
    flag = 0  # 0: 汉字, 1: 不是汉字

    for n, c in enumerate(chars):
        if RE_HANS.match(c):
            if n == 0:
                flag = 0

            if flag == 0:
                s += c
            else:
                ret.append(s)
                flag = 0
                s = c
        else:
            if n == 0:
                flag = 1

            if flag == 1:
                s += c
            else:
                ret.append(s)
                flag = 1
                s = c

    if s:
        ret.append(s)
    return ret


def single_seg(chars: str) -> list[str]:
    """对字符进行分组，汉字切割成单个字符，非汉字连续归组。"""
    res: list[str] = []
    s = ''
    for c in chars:
        if RE_HANS.match(c):
            if s:
                res.append(s)
                s = ''
            res.append(c)
        else:
            s += c
    if s:
        res.append(s)
    return res
