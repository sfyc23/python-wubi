#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import re
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


def fuzzy_reverse_lookup(code: str, limit: int = 10) -> list[tuple[str, str]]:
    """根据五笔编码模糊查询汉字，不确定的字根可用 z 代替。

    支持精确查询与模糊查询：输入不含 z 时等同于精确反查，
    含 z 时将其作为通配符匹配任意字根键（a-y）。
    输入长度决定匹配编码长度，如 'vz' 只匹配 2 码编码。

    :param code: 五笔编码，不确定的位置用 z/Z 代替
    :param limit: 最大返回数量，默认 10，设为 0 表示不限制
    :return: [(汉字, 匹配到的编码), ...] 按编码字母序排列
    """
    if not code:
        return []
    code = code.lower()
    if 'z' not in code:
        chars = reverse_lookup(code)
        return [(c, code) for c in chars][:limit] if limit > 0 else [(c, code) for c in chars]
    pattern = ''.join('[a-y]' if c == 'z' else re.escape(c) for c in code)
    regex = re.compile(f'^{pattern}$')
    results: list[tuple[str, str]] = []
    seen: set[str] = set()
    rev = get_reverse_dict()
    for key, chars in rev.items():
        if regex.match(key):
            for char in chars:
                if char not in seen:
                    seen.add(char)
                    results.append((char, key))
    results.sort(key=lambda x: x[1])
    return results[:limit] if limit > 0 else results


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
