# pywubi — Chinese Character to Wubi Encoding

[![pypi](https://img.shields.io/badge/pypi-0.2.0-yellow.svg)](https://pypi.org/project/pywubi)
![python_version](https://img.shields.io/badge/python-%3E3.8-green.svg)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[中文文档](README_CN.md)

A Python library for converting Chinese characters to [Wubi](https://en.wikipedia.org/wiki/Wubi_method) (五笔) input method encoding. Currently supports the **86-version** scheme with a built-in dictionary of ~21,004 characters.

## Features

- **Single-character encoding** — convert individual Chinese characters to Wubi codes
- **Phrase encoding** — generate codes following Wubi phrase rules (2-char, 3-char, 4+ char)
- **Multi-code query** — return all possible encodings for a character
- **Reverse lookup** — find characters by Wubi code
- **Brief code query** — get the shortest code and its level (1st / 2nd / 3rd / full)
- **Mixed text** — automatically split Chinese and non-Chinese; punctuation is preserved as-is
- **Zero dependencies** — no third-party packages required

## Installation

```bash
pip install pywubi
```

## Quick Start

```python
from pywubi import wubi

# Character-by-character (default)
wubi('我爱你')
# ['trnt', 'epdc', 'wqiy']

# Return all possible codes
wubi('我爱你', multicode=True)
# [['trnt', 'trn', 'q'], ['epdc', 'epd', 'ep'], ['wqiy', 'wqi', 'wq']]

# Phrase mode
wubi('我爱你', single=False)
# ['tewq']

# Mixed text — punctuation preserved
wubi('天气不错，出去走走!')
# ['gdi', 'rnb', 'gii', 'qajg', '，', 'bmt', 'fcu', 'tfht', 'tfht', '!']
```

## API Reference

### `wubi(hans, multicode=False, single=True)`

Convert a Chinese string to Wubi encodings.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hans` | `str` | — | Chinese character string |
| `multicode` | `bool` | `False` | Return all possible codes |
| `single` | `bool` | `True` | `True` for char-by-char, `False` for phrase mode |

**Returns**: `list` — list of Wubi codes

### `single_wubi(han, multicode=False)`

Convert a single Chinese character to Wubi encoding.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `han` | `str` | — | A single Chinese character |
| `multicode` | `bool` | `False` | Return all possible codes |

**Returns**: `str` (single code) or `list[str]` (multiple codes)

### `combine_wubi(hans)`

Convert a phrase to Wubi encoding.

| Parameter | Type | Description |
|-----------|------|-------------|
| `hans` | `str` | Chinese phrase |

**Returns**: `str` — Wubi code for the phrase

Encoding rules:
- 2-char phrase: first 2 codes of each character (4 codes total)
- 3-char phrase: 1st code of char 1 & 2 + first 2 codes of char 3 (4 codes total)
- 4+ char phrase: 1st code of char 1, 2, 3, and last (4 codes total)

### `lookup(char)`

Look up all Wubi codes for a single character.

```python
from pywubi import lookup

lookup('为')   # ['ylyi', 'yly', 'yl', 'o']
lookup('?')    # []
```

### `reverse_lookup(code)`

Reverse-lookup characters by Wubi code.

```python
from pywubi import reverse_lookup

reverse_lookup('trnt')  # ['我']
reverse_lookup('q')     # ['我']
reverse_lookup('ggll')  # ['一']
```

### `brief_code(char)`

Get the shortest (brief) code for a character.

```python
from pywubi import brief_code

brief_code('我')  # 'q'
brief_code('一')  # 'g'
brief_code('?')   # None
```

### `brief_level(char)`

Get the brief-code level (1 = 1st-level, 2 = 2nd-level, 3 = 3rd-level, 4 = full code).

```python
from pywubi import brief_level

brief_level('我')  # 1
brief_level('一')  # 1
brief_level('〇')  # 4
brief_level('?')   # None
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Changelog

### 0.2.0

- Dictionary storage changed from Python source to JSON — faster loading, smaller size
- Added lazy-loading: `import pywubi` no longer loads the full dictionary immediately
- Added `lookup()` to query all codes for a character
- Added `reverse_lookup()` to find characters by code
- Added `brief_code()` to get the shortest code
- Added `brief_level()` to get the brief-code level
- Added comprehensive unit tests

### 0.1.0

- Fixed `single_seg` bug where trailing non-Chinese characters were lost
- Fixed typos (`utlis` → `utils`, `conbin_wubi` → `combine_wubi`)
- Switched to relative imports within the package
- Added type hints
- Added `.gitignore`, removed `.idea/` from tracking
- Fixed README typos

### 0.0.2

- Initial release

## PyPI Account Verification

I am the owner of the PyPI account "sfyc23" and the maintainer of this repository:
https://github.com/sfyc23/python-wubi

I am currently requesting account recovery for the PyPI project/package "pywubi".

This note is added to help PyPI administrators verify that I still control the source repository associated with the package.

GitHub profile: https://github.com/sfyc23
PyPI project: https://pypi.org/project/pywubi/
Date: 2026-03-30

## License

MIT License — see [LICENSE](LICENSE) for details.
