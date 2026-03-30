# 汉字五笔转换工具（Python 版）

[![pypi](https://img.shields.io/badge/pypi-0.2.0-yellow.svg)](https://pypi.org/project/pywubi)
![python_version](https://img.shields.io/badge/python-%3E3.8-green.svg)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md)

将汉字转为五笔编码的 Python 工具库。当前支持 **86 版**五笔编码，内置约 21,004 个汉字的码表。

## 特性

- 单字转码：将单个汉字转成五笔编码
- 词组转码：按五笔词组规则（二字、三字、四字及以上）生成编码
- 多编码查询：返回汉字的所有可能编码
- 反查功能：根据五笔编码反查对应汉字
- 简码查询：获取汉字的最短简码及简码级别
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

将汉字字符串转换成五笔编码。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `hans` | `str` | — | 汉字字符串 |
| `multicode` | `bool` | `False` | 是否返回所有编码 |
| `single` | `bool` | `True` | `True` 逐字转码，`False` 词组取码 |

**返回**: `list` — 五笔编码列表

### `single_wubi(han, multicode=False)`

将单个汉字转成五笔编码。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `han` | `str` | — | 单个汉字 |
| `multicode` | `bool` | `False` | 是否返回所有编码 |

**返回**: `str`（单编码）或 `list[str]`（多编码）

### `combine_wubi(hans)`

将词组转成五笔编码。

| 参数 | 类型 | 说明 |
|------|------|------|
| `hans` | `str` | 汉字词组 |

**返回**: `str` — 词组的五笔编码

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

### `brief_code(char)`

获取汉字的最短简码。

```python
from pywubi import brief_code

brief_code('我')  # 'q'
brief_code('一')  # 'g'
brief_code('?')   # None
```

### `brief_level(char)`

获取汉字的简码级别（1=一级简码, 2=二级简码, 3=三级简码, 4=全码）。

```python
from pywubi import brief_level

brief_level('我')  # 1
brief_level('一')  # 1
brief_level('〇')  # 4
brief_level('?')   # None
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## Changelog

### 0.2.0

- 码表存储从 Python 源码改为 JSON，加载更快、体积更小
- 新增懒加载机制，`import pywubi` 不再立即加载码表
- 新增 `lookup()` 查询单字所有编码
- 新增 `reverse_lookup()` 编码反查汉字
- 新增 `brief_code()` 获取最短简码
- 新增 `brief_level()` 获取简码级别
- 添加完整单元测试

### 0.1.0

- 修复 `single_seg` 尾部非汉字字符丢失的 bug
- 修正拼写错误（`utlis` → `utils`，`conbin_wubi` → `combine_wubi`）
- 所有导入改为包内相对导入
- 添加类型注解（Type Hints）
- 添加 `.gitignore`，清理 `.idea/` 目录
- 修正 README 拼写错误

### 0.0.2

- 初始发布版本

## License

MIT License — 详见 [LICENSE](LICENSE) 文件。
