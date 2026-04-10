from .core import wubi, single_wubi, combine_wubi
from .loader import reverse_lookup, fuzzy_reverse_lookup, brief_code, brief_level, lookup

# 向后兼容旧 API 名称
conbin_wubi = combine_wubi

__title__ = 'pywubi'
__version__ = '0.2.0'
__author__ = 'sfyc23'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2019 Thunder Bouble'
