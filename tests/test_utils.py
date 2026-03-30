#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywubi.utils import single_seg, combin_seg


class TestSingleSeg:
    """single_seg 单字分割测试"""

    def test_chinese_only(self):
        assert single_seg('你好') == ['你', '好']

    def test_ascii_only(self):
        assert single_seg('hello') == ['hello']

    def test_mixed_chinese_then_ascii(self):
        assert single_seg('你好abc') == ['你', '好', 'abc']

    def test_mixed_ascii_then_chinese(self):
        assert single_seg('abc你好') == ['abc', '你', '好']

    def test_interleaved(self):
        result = single_seg('a你b好c')
        assert result == ['a', '你', 'b', '好', 'c']

    def test_empty_string(self):
        assert single_seg('') == []

    def test_punctuation(self):
        result = single_seg('你好，世界!')
        assert result == ['你', '好', '，', '世', '界', '!']

    def test_special_zero(self):
        result = single_seg('〇')
        assert result == ['〇']


class TestCombinSeg:
    """combin_seg 词组分割测试"""

    def test_chinese_only(self):
        assert combin_seg('你好世界') == ['你好世界']

    def test_ascii_only(self):
        assert combin_seg('hello') == ['hello']

    def test_mixed(self):
        result = combin_seg('你好abc世界')
        assert result == ['你好', 'abc', '世界']

    def test_punctuation_splits(self):
        result = combin_seg('你好，世界')
        assert result == ['你好', '，', '世界']

    def test_empty_string(self):
        assert combin_seg('') == []

    def test_single_chinese(self):
        assert combin_seg('我') == ['我']

    def test_single_ascii(self):
        assert combin_seg('a') == ['a']
