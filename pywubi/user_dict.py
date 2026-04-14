#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from typing import Optional

from .constants import RE_HANS
from .core import combine_wubi
from .loader import get_wubi_dict


_user_phrases: Optional[dict[str, str]] = None
_user_reverse: Optional[dict[str, list[str]]] = None
_user_dict_path: Optional[str] = None


def _default_dict_path() -> str:
    """根据操作系统返回用户词组文件的默认路径。"""
    if sys.platform == 'win32':
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
        return os.path.join(base, 'pywubi', 'user_phrases.json')
    elif sys.platform == 'darwin':
        return os.path.join(
            os.path.expanduser('~'),
            'Library', 'Application Support', 'pywubi', 'user_phrases.json',
        )
    else:
        base = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
        return os.path.join(base, 'pywubi', 'user_phrases.json')


def _resolve_path(dict_path: Optional[str] = None) -> str:
    """按优先级解析用户词组文件路径：参数 > 环境变量 > 平台默认。"""
    if dict_path is not None:
        return dict_path
    env_path = os.environ.get('PYWUBI_USER_DICT')
    if env_path:
        return env_path
    return _default_dict_path()


def _load_phrases(path: str) -> dict[str, str]:
    """从 JSON 文件加载用户词组。文件不存在时返回空字典。"""
    if not os.path.isfile(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"用户词组文件格式错误: {path} ({e})") from e
    if not isinstance(data, dict):
        raise ValueError(f"用户词组文件内容必须是 JSON 对象: {path}")
    return data


def _save_phrases(phrases: dict[str, str], path: str) -> None:
    """将用户词组写入 JSON 文件。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(phrases, f, ensure_ascii=False, indent=2)


def _build_reverse(phrases: dict[str, str]) -> dict[str, list[str]]:
    """从词组字典构建反查索引 (编码 → 词组列表)。"""
    rev: dict[str, list[str]] = defaultdict(list)
    for word, code in phrases.items():
        rev[code].append(word)
    return dict(rev)


def _get_phrases(dict_path: Optional[str] = None) -> dict[str, str]:
    """获取用户词组（懒加载）。路径变化时重新加载。"""
    global _user_phrases, _user_reverse, _user_dict_path
    path = _resolve_path(dict_path)
    if _user_phrases is None or _user_dict_path != path:
        _user_phrases = _load_phrases(path)
        _user_reverse = _build_reverse(_user_phrases)
        _user_dict_path = path
    return _user_phrases


def _get_reverse(dict_path: Optional[str] = None) -> dict[str, list[str]]:
    """获取用户词组反查索引。"""
    global _user_reverse
    _get_phrases(dict_path)
    if _user_reverse is None:
        _user_reverse = _build_reverse(_user_phrases or {})
    return _user_reverse


def _invalidate_reverse() -> None:
    """增删操作后使反查索引失效，下次访问时重建。"""
    global _user_reverse
    _user_reverse = None


def _validate_word(word: str) -> None:
    """校验词组输入，不通过则抛出 ValueError。"""
    if not word:
        raise ValueError("词组不能为空")
    if not RE_HANS.match(word):
        raise ValueError("词组必须全部为中文字符")
    if len(word) < 2:
        raise ValueError("词组至少需要 2 个字")
    wubi_dict = get_wubi_dict()
    for char in word:
        if wubi_dict.get(char) is None:
            raise ValueError(f"字符 '{char}' 不在内置码表中，无法生成编码")


def add_user_phrase(word: str, *, dict_path: Optional[str] = None) -> str:
    """添加用户词组，自动生成五笔编码并保存。

    :param word: 中文词组（≥2 字），如 "爱你"
    :param dict_path: 可选，指定用户词组文件路径
    :return: 生成的编码字符串，如 "epwq"
    :raises ValueError: 词组不合法或包含码表外字符
    """
    _validate_word(word)
    phrases = _get_phrases(dict_path)
    existing = phrases.get(word)
    if existing is not None:
        return existing
    code = combine_wubi(word)
    phrases[word] = code
    _invalidate_reverse()
    _save_phrases(phrases, _resolve_path(dict_path))
    return code


def lookup_phrase(word: str, *, dict_path: Optional[str] = None) -> Optional[str]:
    """查询指定词组的编码。

    :param word: 中文词组
    :param dict_path: 可选，指定用户词组文件路径
    :return: 编码字符串，未找到返回 None
    """
    phrases = _get_phrases(dict_path)
    return phrases.get(word)


def remove_user_phrase(word: str, *, dict_path: Optional[str] = None) -> bool:
    """删除指定用户词组。

    :param word: 中文词组
    :param dict_path: 可选，指定用户词组文件路径
    :return: True 表示删除成功，False 表示词组不存在
    """
    phrases = _get_phrases(dict_path)
    if word not in phrases:
        return False
    del phrases[word]
    _invalidate_reverse()
    _save_phrases(phrases, _resolve_path(dict_path))
    return True


def list_user_phrases(*, dict_path: Optional[str] = None) -> dict[str, str]:
    """列出所有用户词组。

    :param dict_path: 可选，指定用户词组文件路径
    :return: 用户词组副本 {"词组": "编码", ...}
    """
    return dict(_get_phrases(dict_path))


def reverse_lookup_phrase(code: str, *, dict_path: Optional[str] = None) -> list[str]:
    """根据编码反查用户词组。

    :param code: 五笔编码
    :param dict_path: 可选，指定用户词组文件路径
    :return: 词组列表，未找到返回空列表
    """
    rev = _get_reverse(dict_path)
    return list(rev.get(code.lower(), []))
