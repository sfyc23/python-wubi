# pywubi - 汉字转五笔编码

[![pypi](https://img.shields.io/badge/pypi-0.3.0-yellow.svg)](https://pypi.org/project/pywubi)
![python_version](https://img.shields.io/badge/python-%3E3.8-green.svg)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README_EN.md)

一个将汉字转换为五笔编码的 Python 工具库。当前支持 **86 版** 五笔编码，内置约 21,004 个汉字的码表。

## 特性

- 单字转码：将单个汉字转换为五笔编码
- 词组转码：按五笔词组规则（二字、三字、四字及以上）生成编码
- 多编码查询：返回汉字的所有可能编码
- 反查功能：根据五笔编码反查对应汉字
- 模糊反查：不确定的字根可用 `z` 代替，进行模糊查询猜字
- 简码查询：获取汉字的最短简码及简码级别
- 用户词组词库：自定义词组的添加、查询、删除与反查，持久化到独立文件
- 混合文本：自动分割汉字与非汉字，标点符号原样保留
- 零依赖：无任何第三方依赖

## 安装

```bash
pip install pywubi
```

## 快速开始

```python
from pywubi import wubi

# 逐字转码（默认模式）
wubi('我爱你')
# ['trnt', 'epdc', 'wqiy']

# 返回所有可能的编码
wubi('我爱你', multicode=True)
# [['trnt', 'trn', 'q'], ['epdc', 'epd', 'ep'], ['wqiy', 'wqi', 'wq']]

# 以词组方式取码
wubi('我爱你', single=False)
# ['tewq']

# 混合文本，标点原样保留
wubi('天气不错，出去走走!')
# ['gdi', 'rnb', 'gii', 'qajg', '，', 'bmt', 'fcu', 'tfht', 'tfht', '!']
```

## API 文档

### `wubi(hans, multicode=False, single=True)`

将汉字字符串转换为五笔编码。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `hans` | `str` | - | 汉字字符串 |
| `multicode` | `bool` | `False` | 是否返回所有编码 |
| `single` | `bool` | `True` | `True` 表示逐字转码，`False` 表示词组取码 |

**返回**：`list`，五笔编码列表

### `single_wubi(han, multicode=False)`

将单个汉字转换为五笔编码。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `han` | `str` | - | 单个汉字 |
| `multicode` | `bool` | `False` | 是否返回所有编码 |

**返回**：`str`（单编码）或 `list[str]`（多编码）

### `combine_wubi(hans)`

将词组转换为五笔编码。

| 参数 | 类型 | 说明 |
|------|------|------|
| `hans` | `str` | 汉字词组 |

**返回**：`str`，词组的五笔编码

取码规则：

- 二字词：各取前两码（共 4 码）
- 三字词：前两字各取首码 + 第三字取前两码（共 4 码）
- 四字及以上：取第 1、2、3、末字的首码（共 4 码）

### `lookup(char)`

查询单个汉字的所有五笔编码。

```python
from pywubi import lookup

lookup('为')   # ['ylyi', 'yly', 'yl', 'o']
lookup('?')    # []
```

### `reverse_lookup(code)`

根据五笔编码反查汉字。

```python
from pywubi import reverse_lookup

reverse_lookup('trnt')  # ['我']
reverse_lookup('q')     # ['我']
reverse_lookup('ggll')  # ['一']
```

### `fuzzy_reverse_lookup(code, limit=10)`

根据五笔编码模糊查询汉字，不确定的字根可用 `z` 代替。

五笔 86 版编码仅使用 `a`-`y`，`z` 键天然空闲，可作为通配符匹配任意字根。输入不含 `z` 时等同于精确反查；输入长度决定匹配编码长度。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `code` | `str` | - | 五笔编码，不确定的位置用 `z`/`Z` 代替 |
| `limit` | `int` | `10` | 最大返回数量，`0` 表示不限制 |

**返回**：`list[tuple[str, str]]`，格式为 `[(汉字, 匹配编码), ...]`，按编码字母序排列

```python
from pywubi import fuzzy_reverse_lookup

fuzzy_reverse_lookup('vz')       # [('姑', 'vd'), ('灵', 'vo'), ...]
fuzzy_reverse_lookup('zzzg')     # 只知道末码是 g，返回末码为 g 的四码字
fuzzy_reverse_lookup('trnt')     # 无 z，退化为精确反查
fuzzy_reverse_lookup('zz', limit=5)  # 限制返回 5 条
```

### `brief_code(char)`

获取汉字的最短简码。

```python
from pywubi import brief_code

brief_code('我')  # 'q'
brief_code('一')  # 'g'
brief_code('?')   # None
```

### `brief_level(char)`

获取汉字的简码级别（1=一级简码，2=二级简码，3=三级简码，4=全码）。

```python
from pywubi import brief_level

brief_level('我')  # 1
brief_level('一')  # 1
brief_level('〇')  # 4
brief_level('?')   # None
```

### `add_user_phrase(word, *, dict_path=None)`

添加用户词组，自动生成五笔编码并保存到用户词组文件。

只需输入中文词组（≥2 字），程序会校验输入、生成编码并持久化保存。用户词组文件与内置码表完全隔离，不会影响官方数据。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `word` | `str` | - | 中文词组（至少 2 个字） |
| `dict_path` | `str \| None` | `None` | 可选，指定用户词组文件路径 |

**返回**：`str`，生成的编码

```python
from pywubi import add_user_phrase

add_user_phrase('爱你')            # 'epwq'
add_user_phrase('中华人民共和国')  # 'kwwl'
add_user_phrase('我爱你')          # 'tewq'
```

用户词组默认保存位置：

| 平台 | 路径 |
|------|------|
| Windows | `%APPDATA%\pywubi\user_phrases.json` |
| macOS | `~/Library/Application Support/pywubi/user_phrases.json` |
| Linux | `~/.config/pywubi/user_phrases.json` |

也可通过环境变量 `PYWUBI_USER_DICT` 或 `dict_path` 参数自定义路径。

### `lookup_phrase(word, *, dict_path=None)`

查询用户词组的编码。

```python
from pywubi import add_user_phrase, lookup_phrase

add_user_phrase('爱你')
lookup_phrase('爱你')   # 'epwq'
lookup_phrase('你好')   # None（未添加过）
```

### `remove_user_phrase(word, *, dict_path=None)`

删除用户词组。返回 `True` 表示删除成功，`False` 表示词组不存在。

```python
from pywubi import add_user_phrase, remove_user_phrase

add_user_phrase('爱你')
remove_user_phrase('爱你')  # True
remove_user_phrase('爱你')  # False（已不存在）
```

### `list_user_phrases(*, dict_path=None)`

列出所有用户词组。返回 `dict[str, str]`，格式为 `{"词组": "编码", ...}`。

```python
from pywubi import add_user_phrase, list_user_phrases

add_user_phrase('爱你')
add_user_phrase('你好')
list_user_phrases()  # {'爱你': 'epwq', '你好': 'wqvb'}
```

### `reverse_lookup_phrase(code, *, dict_path=None)`

根据编码反查用户词组。同一编码可对应多个词组（重码），按列表返回。

```python
from pywubi import add_user_phrase, reverse_lookup_phrase

add_user_phrase('爱你')
reverse_lookup_phrase('epwq')  # ['爱你']
reverse_lookup_phrase('xxxx')  # []
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 更新日志

### 0.3.0

- 新增用户词组词库功能，支持自定义词组的添加、查询、删除与反查
- 新增 `add_user_phrase()` 输入中文词组自动生成编码并保存
- 新增 `lookup_phrase()` 查询用户词组编码
- 新增 `remove_user_phrase()` 删除用户词组
- 新增 `list_user_phrases()` 列出所有用户词组
- 新增 `reverse_lookup_phrase()` 按编码反查用户词组
- 用户词组持久化到独立 JSON 文件，不污染内置码表
- 支持跨平台默认路径、环境变量和参数自定义路径

### 0.2.0

- 码表存储从 Python 源码改为 JSON，加载更快、体积更小
- 新增懒加载机制，`import pywubi` 不再立即加载码表
- 新增 `lookup()` 查询单字所有编码
- 新增 `reverse_lookup()` 编码反查汉字
- 新增 `brief_code()` 获取最短简码
- 新增 `brief_level()` 获取简码级别
- 添加完整单元测试

### 0.1.0

- 修复 `single_seg` 尾部非汉字字符丢失的问题
- 修正拼写错误（`utlis` -> `utils`，`conbin_wubi` -> `combine_wubi`）
- 所有导入改为包内相对导入
- 添加类型注解（Type Hints）
- 添加 `.gitignore`，清理 `.idea/` 目录
- 修正 README 拼写错误

### 0.0.2

- 初始发布版本

## License

MIT License，详见 [LICENSE](LICENSE)。
