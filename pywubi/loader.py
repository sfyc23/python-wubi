#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from collections import defaultdict
from importlib import resources
from typing import Optional


_wubi_86_dict: Optional[dict[str, list[str]]] = None
_reverse_dict: Optional[dict[str, list[str]]] = None


def _load_json() -> dict[str, list[str]]:
    """从 JSON 文件加载 86 版五笔码表。"""
    ref = resources.files('pywubi').joinpath('data/wubi_86.json')
    with resources.as_file(ref) as path:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


def get_wubi_dict() -> dict[str, list[str]]:
    """获取五笔编码字典（懒加载，首次调用时加载）。

    返回 dict，key 为汉字字符，value 为编码列表（按长度降序）。
    """
    global _wubi_86_dict
    if _wubi_86_dict is None:
        _wubi_86_dict = _load_json()
    return _wubi_86_dict


def get_reverse_dict() -> dict[str, list[str]]:
    """获取反查字典（懒加载，首次调用时从正向码表构建）。

    返回 dict，key 为五笔编码，value 为对应的汉字列表。
    """
    global _reverse_dict
    if _reverse_dict is None:
        wubi_dict = get_wubi_dict()
        rev: dict[str, list[str]] = defaultdict(list)
        for char, codes in wubi_dict.items():
            for code in codes:
                rev[code].append(char)
        _reverse_dict = dict(rev)
    return _reverse_dict


def lookup(char: str) -> list[str]:
    """查询单个汉字的所有五笔编码。

    :param char: 单个汉字
    :return: 编码列表（按长度降序），未找到返回空列表
    """
    return get_wubi_dict().get(char, [])


def reverse_lookup(code: str) -> list[str]:
    """根据五笔编码反查汉字。

    :param code: 五笔编码（如 'trnt'）
    :return: 对应的汉字列表，未找到返回空列表
    """
    return get_reverse_dict().get(code.lower(), [])


def brief_code(char: str) -> Optional[str]:
    """获取汉字的最短简码。

    :param char: 单个汉字
    :return: 最短的五笔编码，未找到返回 None
    """
    codes = lookup(char)
    if not codes:
        return None
    return min(codes, key=len)


def brief_level(char: str) -> Optional[int]:
    """获取汉字的简码级别。

    :param char: 单个汉字
    :return: 简码级别（1=一级简码, 2=二级简码, 3=三级简码, 4=全码），
             未找到返回 None
    """
    code = brief_code(char)
    if code is None:
        return None
    length = len(code)
    if length <= 4:
        return length
    return 4
