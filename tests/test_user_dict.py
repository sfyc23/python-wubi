#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

import pytest

from pywubi import (
    wubi, reverse_lookup, fuzzy_reverse_lookup,
    add_user_phrase, lookup_phrase, remove_user_phrase,
    list_user_phrases, reverse_lookup_phrase,
)
from pywubi.user_dict import _user_phrases, _user_reverse, _user_dict_path


@pytest.fixture(autouse=True)
def isolated_dict(tmp_path):
    """每个测试用例使用独立的临时词组文件，并在测试后重置全局状态。"""
    import pywubi.user_dict as mod
    mod._user_phrases = None
    mod._user_reverse = None
    mod._user_dict_path = None
    path = str(tmp_path / 'user_phrases.json')
    yield path
    mod._user_phrases = None
    mod._user_reverse = None
    mod._user_dict_path = None


class TestAddUserPhrase:
    """add_user_phrase 添加词组测试"""

    def test_basic_two_chars(self, isolated_dict):
        """T1: 添加二字词"""
        code = add_user_phrase('爱你', dict_path=isolated_dict)
        assert code == 'epwq'

    def test_long_phrase(self, isolated_dict):
        """T2: 添加四字以上词组"""
        code = add_user_phrase('中华人民共和国', dict_path=isolated_dict)
        assert code == 'kwwl'

    def test_three_chars(self, isolated_dict):
        """三字词取码"""
        code = add_user_phrase('我爱你', dict_path=isolated_dict)
        assert code == 'tewq'

    def test_reject_non_chinese(self, isolated_dict):
        """T3: 含非中文字符"""
        with pytest.raises(ValueError, match='中文'):
            add_user_phrase('爱你!', dict_path=isolated_dict)

    def test_reject_english(self, isolated_dict):
        """T4: 纯英文"""
        with pytest.raises(ValueError, match='中文'):
            add_user_phrase('love', dict_path=isolated_dict)

    def test_reject_empty(self, isolated_dict):
        """T5: 空字符串"""
        with pytest.raises(ValueError, match='不能为空'):
            add_user_phrase('', dict_path=isolated_dict)

    def test_reject_single_char(self, isolated_dict):
        """T6: 单字"""
        with pytest.raises(ValueError, match='至少需要 2 个字'):
            add_user_phrase('爱', dict_path=isolated_dict)

    def test_reject_unknown_char(self, isolated_dict):
        """T7: 码表外生僻字（\u9fa6 在汉字范围内但不在码表中）"""
        with pytest.raises(ValueError, match='不在内置码表中'):
            add_user_phrase('爱\u9fa6', dict_path=isolated_dict)

    def test_idempotent(self, isolated_dict):
        """T8: 重复添加幂等"""
        code1 = add_user_phrase('爱你', dict_path=isolated_dict)
        code2 = add_user_phrase('爱你', dict_path=isolated_dict)
        assert code1 == code2 == 'epwq'


class TestLookupPhrase:
    """lookup_phrase 查询词组测试"""

    def test_found(self, isolated_dict):
        add_user_phrase('爱你', dict_path=isolated_dict)
        assert lookup_phrase('爱你', dict_path=isolated_dict) == 'epwq'

    def test_not_found(self, isolated_dict):
        assert lookup_phrase('不存在', dict_path=isolated_dict) is None


class TestRemoveUserPhrase:
    """remove_user_phrase 删除词组测试"""

    def test_remove_existing(self, isolated_dict):
        """T11: 删除后查不到"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        assert remove_user_phrase('爱你', dict_path=isolated_dict) is True
        assert lookup_phrase('爱你', dict_path=isolated_dict) is None

    def test_remove_nonexistent(self, isolated_dict):
        assert remove_user_phrase('不存在', dict_path=isolated_dict) is False


class TestListUserPhrases:
    """list_user_phrases 列出词组测试"""

    def test_empty(self, isolated_dict):
        assert list_user_phrases(dict_path=isolated_dict) == {}

    def test_with_phrases(self, isolated_dict):
        add_user_phrase('爱你', dict_path=isolated_dict)
        add_user_phrase('你好', dict_path=isolated_dict)
        result = list_user_phrases(dict_path=isolated_dict)
        assert result == {'爱你': 'epwq', '你好': result['你好']}
        assert len(result) == 2

    def test_returns_copy(self, isolated_dict):
        """返回的是副本，修改不影响内部状态"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        copy = list_user_phrases(dict_path=isolated_dict)
        copy['测试'] = 'xxxx'
        assert lookup_phrase('测试', dict_path=isolated_dict) is None


class TestReverseLookupPhrase:
    """reverse_lookup_phrase 词组反查测试"""

    def test_basic(self, isolated_dict):
        """T10: 反查编码"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        result = reverse_lookup_phrase('epwq', dict_path=isolated_dict)
        assert result == ['爱你']

    def test_not_found(self, isolated_dict):
        assert reverse_lookup_phrase('xxxx', dict_path=isolated_dict) == []

    def test_case_insensitive(self, isolated_dict):
        add_user_phrase('爱你', dict_path=isolated_dict)
        assert reverse_lookup_phrase('EPWQ', dict_path=isolated_dict) == ['爱你']

    def test_multiple_phrases_same_code(self, isolated_dict):
        """T15: 多词组同码"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        # 手动写入一个同编码的词组来模拟冲突
        import pywubi.user_dict as mod
        phrases = mod._get_phrases(isolated_dict)
        phrases['假词'] = 'epwq'
        mod._invalidate_reverse()
        mod._save_phrases(phrases, isolated_dict)
        result = reverse_lookup_phrase('epwq', dict_path=isolated_dict)
        assert '爱你' in result
        assert '假词' in result
        assert len(result) == 2


class TestPersistence:
    """持久化测试"""

    def test_save_and_reload(self, isolated_dict):
        """T9: 保存后重新加载"""
        add_user_phrase('爱你', dict_path=isolated_dict)

        # 重置内存缓存，模拟重新启动
        import pywubi.user_dict as mod
        mod._user_phrases = None
        mod._user_reverse = None
        mod._user_dict_path = None

        assert lookup_phrase('爱你', dict_path=isolated_dict) == 'epwq'

    def test_file_content(self, isolated_dict):
        """验证文件内容格式"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        with open(isolated_dict, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data == {'爱你': 'epwq'}

    def test_auto_create_directory(self, tmp_path):
        """保存时自动创建目录"""
        deep_path = str(tmp_path / 'a' / 'b' / 'user_phrases.json')
        add_user_phrase('爱你', dict_path=deep_path)
        assert os.path.isfile(deep_path)

    def test_custom_dict_path(self, tmp_path):
        """T16: 自定义路径"""
        path1 = str(tmp_path / 'dict1.json')
        path2 = str(tmp_path / 'dict2.json')
        add_user_phrase('爱你', dict_path=path1)
        add_user_phrase('你好', dict_path=path2)
        assert lookup_phrase('爱你', dict_path=path1) == 'epwq'
        assert lookup_phrase('爱你', dict_path=path2) is None
        assert lookup_phrase('你好', dict_path=path2) is not None


class TestNoSideEffects:
    """验证不影响现有 API"""

    def test_wubi_single_unchanged(self, isolated_dict):
        """T12: 现有逐字转码不受影响"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        assert wubi('爱你') == ['epdc', 'wqiy']

    def test_reverse_lookup_unchanged(self, isolated_dict):
        """T13: 现有单字反查不受影响"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        result = reverse_lookup('epdc')
        assert '爱' in result

    def test_fuzzy_reverse_lookup_unchanged(self, isolated_dict):
        """T14: 现有模糊反查不受影响"""
        add_user_phrase('爱你', dict_path=isolated_dict)
        results = fuzzy_reverse_lookup('vz')
        assert len(results) > 0
        chars = [r[0] for r in results]
        assert all(len(c) == 1 for c in chars)


class TestCorruptedFile:
    """损坏文件处理测试"""

    def test_invalid_json(self, tmp_path):
        path = str(tmp_path / 'bad.json')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('{invalid json}')
        with pytest.raises(ValueError, match='格式错误'):
            lookup_phrase('爱你', dict_path=path)

    def test_wrong_structure(self, tmp_path):
        path = str(tmp_path / 'bad.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(['not', 'a', 'dict'], f)
        with pytest.raises(ValueError, match='JSON 对象'):
            lookup_phrase('爱你', dict_path=path)
