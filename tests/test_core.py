#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pywubi import wubi, single_wubi, combine_wubi, conbin_wubi


class TestSingleWubi:
    """single_wubi 单字编码测试"""

    def test_basic_char(self):
        assert single_wubi('我') == 'trnt'

    def test_multicode_false(self):
        result = single_wubi('为')
        assert isinstance(result, str)
        assert result == 'ylyi'

    def test_multicode_true(self):
        result = single_wubi('为', multicode=True)
        assert isinstance(result, list)
        assert result == ['ylyi', 'yly', 'yl', 'o']

    def test_unknown_char(self):
        assert single_wubi('?') == '?'
        assert single_wubi('@') == '@'

    def test_special_char_zero(self):
        assert single_wubi('〇') == 'llll'

    def test_multichar_delegates_to_combine(self):
        result = single_wubi('你好')
        assert isinstance(result, str)
        assert result == combine_wubi('你好')


class TestCombineWubi:
    """combine_wubi 词组编码测试"""

    def test_single_char(self):
        assert combine_wubi('我') == 'trnt'

    def test_two_chars(self):
        result = combine_wubi('你好')
        assert isinstance(result, str)
        assert len(result) == 4

    def test_three_chars(self):
        result = combine_wubi('我爱你')
        assert isinstance(result, str)
        assert result == 'tewq'

    def test_four_chars(self):
        result = combine_wubi('生死有命')
        assert isinstance(result, str)
        assert result == 'tgdw'

    def test_more_than_four_chars(self):
        result = combine_wubi('中华人民共和国')
        assert isinstance(result, str)
        assert len(result) == 4

    def test_backward_compat_alias(self):
        assert conbin_wubi is combine_wubi


class TestWubi:
    """wubi 主函数测试"""

    def test_single_mode_default(self):
        result = wubi('我爱你')
        assert result == ['trnt', 'epdc', 'wqiy']

    def test_single_mode_multicode(self):
        result = wubi('我爱你', multicode=True)
        assert len(result) == 3
        assert all(isinstance(r, list) for r in result)
        assert result[0] == ['trnt', 'trn', 'q']

    def test_combine_mode(self):
        result = wubi('我爱你', single=False)
        assert result == ['tewq']

    def test_mixed_text(self):
        result = wubi('你好!')
        assert len(result) == 3
        assert result[2] == '!'

    def test_punctuation_preserved(self):
        result = wubi('天气不错，我们去散步吧!')
        assert '，' in result
        assert '!' in result

    def test_empty_string(self):
        assert wubi('') == []

    def test_pure_ascii(self):
        result = wubi('hello')
        assert result == ['hello']

    def test_single_char(self):
        result = wubi('滚')
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], str)
