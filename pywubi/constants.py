from enum import IntEnum, unique
# from __future__ import unicode_literals
import os
import re

from pywubi import wubi_dict

# 单字拼音库
WUBI_86_DICT = wubi_dict.wubi_86_dict

# 利用环境变量控制不做copy操作, 以减少内存使用
if not os.environ.get('PYWUBI_NO_DICT_COPY'):
    WUBI_86_DICT = WUBI_86_DICT.copy()

RE_HANS = re.compile(
    r'^(?:['
    r'\u3007'  # 〇
    r'\u4e00-\ufa29'
    r'])+$'
)

@unique
class Style(IntEnum):
    """编码"""
    # 86 版编码
    WUBI_86 = 1
    # 96 版编码
    WUBI_96 = 2
STYLE_WUBI_86 = Style.WUBI_86
STYLE_WUBI_96 = Style.WUBI_96
