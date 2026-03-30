#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from enum import IntEnum, unique
import re

RE_HANS = re.compile(
    r'^(?:['
    r'\u3007'  # 〇
    r'\u4e00-\ufa29'
    r'])+$'
)


@unique
class Style(IntEnum):
    """五笔编码版本"""
    WUBI_86 = 1
    WUBI_96 = 2


STYLE_WUBI_86 = Style.WUBI_86
STYLE_WUBI_96 = Style.WUBI_96
