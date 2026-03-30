#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywubi.loader import (
    get_wubi_dict, get_reverse_dict,
    lookup, reverse_lookup,
    brief_code, brief_level,
)


class TestGetWubiDict:
    """码表加载测试"""

    def test_loads_successfully(self):
        d = get_wubi_dict()
        assert isinstance(d, dict)
        assert len(d) > 20000

    def test_key_is_char(self):
        d = get_wubi_dict()
        assert '我' in d
        assert '一' in d
        assert '〇' in d

    def test_value_is_list(self):
        d = get_wubi_dict()
        codes = d['我']
        assert isinstance(codes, list)
        assert all(isinstance(c, str) for c in codes)

    def test_singleton(self):
        d1 = get_wubi_dict()
        d2 = get_wubi_dict()
        assert d1 is d2


class TestLookup:
    """lookup 查询测试"""

    def test_known_char(self):
        assert lookup('我') == ['trnt', 'trn', 'q']

    def test_multi_code_char(self):
        codes = lookup('为')
        assert len(codes) == 4
        assert 'o' in codes

    def test_unknown_char(self):
        assert lookup('?') == []
        assert lookup('@') == []

    def test_special_zero(self):
        assert lookup('〇') == ['llll']


class TestReverseLookup:
    """reverse_lookup 反查测试"""

    def test_full_code(self):
        chars = reverse_lookup('trnt')
        assert '我' in chars

    def test_brief_code(self):
        chars = reverse_lookup('q')
        assert '我' in chars

    def test_case_insensitive(self):
        assert reverse_lookup('TRNT') == reverse_lookup('trnt')

    def test_unknown_code(self):
        assert reverse_lookup('zzzz') == []

    def test_reverse_dict_singleton(self):
        d1 = get_reverse_dict()
        d2 = get_reverse_dict()
        assert d1 is d2


class TestBriefCode:
    """brief_code 简码查询测试"""

    def test_level_1(self):
        assert brief_code('我') == 'q'
        assert brief_code('一') == 'g'

    def test_full_code_char(self):
        code = brief_code('〇')
        assert code == 'llll'

    def test_unknown_char(self):
        assert brief_code('?') is None


class TestBriefLevel:
    """brief_level 简码级别测试"""

    def test_level_1(self):
        assert brief_level('我') == 1
        assert brief_level('一') == 1

    def test_level_4_full_code(self):
        assert brief_level('〇') == 4

    def test_unknown_char(self):
        assert brief_level('?') is None

    def test_returns_int(self):
        level = brief_level('我')
        assert isinstance(level, int)
