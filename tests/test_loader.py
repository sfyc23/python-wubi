#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywubi.loader import (
    get_wubi_dict, get_reverse_dict,
    lookup, reverse_lookup, fuzzy_reverse_lookup,
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


class TestFuzzyReverseLookup:
    """fuzzy_reverse_lookup 容错反查测试"""

    def test_single_wildcard(self):
        results = fuzzy_reverse_lookup('vz')
        chars = [r[0] for r in results]
        assert len(results) > 0
        assert all(len(code) == 2 for _, code in results)
        assert all(code.startswith('v') for _, code in results)

    def test_wildcard_at_first_position(self):
        results = fuzzy_reverse_lookup('zq')
        assert len(results) > 0
        assert all(len(code) == 2 for _, code in results)
        assert all(code.endswith('q') for _, code in results)

    def test_multiple_wildcards(self):
        results = fuzzy_reverse_lookup('zzzg')
        assert len(results) > 0
        assert all(len(code) == 4 for _, code in results)
        assert all(code.endswith('g') for _, code in results)

    def test_no_wildcard_degrades_to_exact(self):
        results = fuzzy_reverse_lookup('trnt')
        chars = [r[0] for r in results]
        assert '我' in chars

    def test_case_insensitive(self):
        assert fuzzy_reverse_lookup('VZ') == fuzzy_reverse_lookup('vz')

    def test_empty_input(self):
        assert fuzzy_reverse_lookup('') == []

    def test_limit(self):
        results = fuzzy_reverse_lookup('zz', limit=3)
        assert len(results) <= 3

    def test_limit_zero_returns_all(self):
        limited = fuzzy_reverse_lookup('zz', limit=5)
        unlimited = fuzzy_reverse_lookup('zz', limit=0)
        assert len(unlimited) >= len(limited)

    def test_results_sorted_by_code(self):
        results = fuzzy_reverse_lookup('vz')
        codes = [r[1] for r in results]
        assert codes == sorted(codes)

    def test_result_is_tuple_pair(self):
        results = fuzzy_reverse_lookup('vz')
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_unknown_pattern_returns_empty(self):
        assert fuzzy_reverse_lookup('99') == []


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
