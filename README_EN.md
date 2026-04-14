# pywubi - Chinese Character to Wubi Encoding

[![pypi](https://img.shields.io/badge/pypi-0.3.0-yellow.svg)](https://pypi.org/project/pywubi)
![python_version](https://img.shields.io/badge/python-%3E3.8-green.svg)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[中文文档](README.md)

A Python library for converting Chinese characters to [Wubi](https://en.wikipedia.org/wiki/Wubi_method) (五笔) input method encoding. It currently supports the **86-version** scheme and ships with a built-in dictionary covering about 21,004 Chinese characters.

## Features

- **Single-character encoding**: convert individual Chinese characters to Wubi codes
- **Phrase encoding**: generate codes following Wubi phrase rules (2-char, 3-char, 4+ char)
- **Multi-code query**: return all possible encodings for a character
- **Reverse lookup**: find characters by Wubi code
- **Fuzzy reverse lookup**: use `z` in place of unknown radicals to guess characters
- **Brief code query**: get the shortest code and its level (1st / 2nd / 3rd / full)
- **User phrase dictionary**: add, query, delete, and reverse-lookup custom phrases, persisted to a standalone file
- **Mixed text support**: automatically split Chinese and non-Chinese text while preserving punctuation
- **Zero dependencies**: no third-party packages required

## Installation

```bash
pip install pywubi
```

## Quick Start

```python
from pywubi import wubi

# Character-by-character mode (default)
wubi('我爱你')
# ['trnt', 'epdc', 'wqiy']

# Return all possible codes
wubi('我爱你', multicode=True)
# [['trnt', 'trn', 'q'], ['epdc', 'epd', 'ep'], ['wqiy', 'wqi', 'wq']]

# Phrase mode
wubi('我爱你', single=False)
# ['tewq']

# Mixed text, punctuation preserved
wubi('天气不错，出去走走!')
# ['gdi', 'rnb', 'gii', 'qajg', '，', 'bmt', 'fcu', 'tfht', 'tfht', '!']
```

## API Reference

### `wubi(hans, multicode=False, single=True)`

Convert a Chinese string to Wubi encodings.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hans` | `str` | - | Chinese character string |
| `multicode` | `bool` | `False` | Return all possible codes |
| `single` | `bool` | `True` | `True` for char-by-char mode, `False` for phrase mode |

**Returns**: `list`, a list of Wubi codes

### `single_wubi(han, multicode=False)`

Convert a single Chinese character to Wubi encoding.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `han` | `str` | - | A single Chinese character |
| `multicode` | `bool` | `False` | Return all possible codes |

**Returns**: `str` (single code) or `list[str]` (multiple codes)

### `combine_wubi(hans)`

Convert a phrase to Wubi encoding.

| Parameter | Type | Description |
|-----------|------|-------------|
| `hans` | `str` | Chinese phrase |

**Returns**: `str`, the Wubi code for the phrase

Encoding rules:

- 2-character phrase: take the first two codes of each character (4 codes total)
- 3-character phrase: take the first code of the first two characters plus the first two codes of the third character (4 codes total)
- 4-or-more-character phrase: take the first code of the 1st, 2nd, 3rd, and last characters (4 codes total)

### `lookup(char)`

Look up all Wubi codes for a single character.

```python
from pywubi import lookup

lookup('为')   # ['ylyi', 'yly', 'yl', 'o']
lookup('?')    # []
```

### `reverse_lookup(code)`

Reverse lookup characters by Wubi code.

```python
from pywubi import reverse_lookup

reverse_lookup('trnt')  # ['我']
reverse_lookup('q')     # ['我']
reverse_lookup('ggll')  # ['一']
```

### `fuzzy_reverse_lookup(code, limit=10)`

Fuzzy reverse lookup characters by Wubi code; use `z` for unknown radical keys.

Wubi 86 only uses keys `a`-`y`, so `z` is naturally unused and can act as a wildcard for any radical key. When the input contains no `z`, it behaves the same as an exact reverse lookup. The input length determines the matched code length.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `str` | - | Wubi code; use `z`/`Z` for unknown positions |
| `limit` | `int` | `10` | Maximum number of results to return; `0` means unlimited |

**Returns**: `list[tuple[str, str]]`, in the form `[(character, matched_code), ...]`, sorted by code

```python
from pywubi import fuzzy_reverse_lookup

fuzzy_reverse_lookup('vz')       # [('姑', 'vd'), ('灵', 'vo'), ...]
fuzzy_reverse_lookup('zzzg')     # last code is g, find all 4-code characters ending with g
fuzzy_reverse_lookup('trnt')     # no z, degrades to exact reverse lookup
fuzzy_reverse_lookup('zz', limit=5)  # limit to 5 results
```

### `brief_code(char)`

Get the shortest brief code for a character.

```python
from pywubi import brief_code

brief_code('我')  # 'q'
brief_code('一')  # 'g'
brief_code('?')   # None
```

### `brief_level(char)`

Get the brief-code level for a character (1 = 1st-level, 2 = 2nd-level, 3 = 3rd-level, 4 = full code).

```python
from pywubi import brief_level

brief_level('我')  # 1
brief_level('一')  # 1
brief_level('〇')  # 4
brief_level('?')   # None
```

### `add_user_phrase(word, *, dict_path=None)`

Add a user phrase. Automatically generates the Wubi encoding and saves it to the user phrase file.

Simply provide a Chinese phrase (≥ 2 characters). The function validates the input, generates the encoding, and persists it. The user phrase file is completely separate from the built-in dictionary.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `word` | `str` | - | Chinese phrase (at least 2 characters) |
| `dict_path` | `str \| None` | `None` | Optional custom path for the user phrase file |

**Returns**: `str`, the generated encoding

```python
from pywubi import add_user_phrase

add_user_phrase('爱你')            # 'epwq'
add_user_phrase('中华人民共和国')  # 'kwwl'
add_user_phrase('我爱你')          # 'tewq'
```

Default user phrase file locations:

| Platform | Path |
|----------|------|
| Windows | `%APPDATA%\pywubi\user_phrases.json` |
| macOS | `~/Library/Application Support/pywubi/user_phrases.json` |
| Linux | `~/.config/pywubi/user_phrases.json` |

You can also override the path via the `PYWUBI_USER_DICT` environment variable or the `dict_path` parameter.

### `lookup_phrase(word, *, dict_path=None)`

Look up the encoding of a user phrase.

```python
from pywubi import add_user_phrase, lookup_phrase

add_user_phrase('爱你')
lookup_phrase('爱你')   # 'epwq'
lookup_phrase('你好')   # None (not added)
```

### `remove_user_phrase(word, *, dict_path=None)`

Remove a user phrase. Returns `True` if the phrase was removed, `False` if it didn't exist.

```python
from pywubi import add_user_phrase, remove_user_phrase

add_user_phrase('爱你')
remove_user_phrase('爱你')  # True
remove_user_phrase('爱你')  # False (already removed)
```

### `list_user_phrases(*, dict_path=None)`

List all user phrases. Returns `dict[str, str]` in the form `{"phrase": "code", ...}`.

```python
from pywubi import add_user_phrase, list_user_phrases

add_user_phrase('爱你')
add_user_phrase('你好')
list_user_phrases()  # {'爱你': 'epwq', '你好': 'wqvb'}
```

### `reverse_lookup_phrase(code, *, dict_path=None)`

Reverse lookup user phrases by encoding. The same code can map to multiple phrases (code collision is normal in Wubi); results are returned as a list.

```python
from pywubi import add_user_phrase, reverse_lookup_phrase

add_user_phrase('爱你')
reverse_lookup_phrase('epwq')  # ['爱你']
reverse_lookup_phrase('xxxx')  # []
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Changelog

### 0.3.0

- Added user phrase dictionary for adding, querying, deleting, and reverse-looking-up custom phrases
- Added `add_user_phrase()` to input a Chinese phrase and automatically generate and save its encoding
- Added `lookup_phrase()` to query a user phrase's encoding
- Added `remove_user_phrase()` to delete a user phrase
- Added `list_user_phrases()` to list all user phrases
- Added `reverse_lookup_phrase()` to reverse lookup user phrases by encoding
- User phrases are persisted to a standalone JSON file, keeping the built-in dictionary untouched
- Cross-platform default paths with support for environment variable and parameter overrides

### 0.2.0

- Changed dictionary storage from Python source to JSON for faster loading and a smaller package size
- Added lazy loading so `import pywubi` no longer loads the full dictionary immediately
- Added `lookup()` to query all codes for a character
- Added `reverse_lookup()` to find characters by code
- Added `brief_code()` to get the shortest brief code
- Added `brief_level()` to get the brief-code level
- Added comprehensive unit tests

### 0.1.0

- Fixed the `single_seg` bug where trailing non-Chinese characters were lost
- Fixed typos (`utlis` -> `utils`, `conbin_wubi` -> `combine_wubi`)
- Switched package imports to relative imports
- Added type hints
- Added `.gitignore` and removed `.idea/` from tracking
- Fixed README typos

### 0.0.2

- Initial release

## License

MIT License. See [LICENSE](LICENSE) for details.
