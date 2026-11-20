# tianzige

[![CI](https://github.com/eastyou/tianzige/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/tianzige/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](pyproject.toml)

给小学老师和家长用的田字格练字帖生成器：把生字表交给它，一条命令生成多页 A4 字帖，每行前几个字浅色描红，后面留白自己写。**零依赖，不联网，单文件 HTML。**

支持田字格、米字格和普通方格，字体优先使用楷体，适合低年级识字和书写练习。

## 特性

- **三种格子**：田字格（虚线十字）、米字格（加对角线）、方格
- **描红引导**：每行前 N 个格子是浅灰描红，其余留白，数量可调
- **重复练习**：每个字可写 1~5 行，每行 1~12 格
- **自动分页**：按每页行数自动切页，页码标注「第 N / M 页」
- **输入灵活**：命令行直接输入文字，或读取 TXT 文件；文件里 `#` 开头是注释
- **按字排版**：每个字占满一行，不会把词语拆得乱七八糟
- **A4 打印**：页面自带姓名、日期栏，打印时自动分页
- **38 个单元测试**：覆盖文字切分、排版、分页、参数校验与命令行

## 安装

```bash
pip install tianzige
```

也可以下载源码后直接运行：

```bash
python -m tianzige --help
```

## 输入格式

直接写文字：

```bash
tianzige --text "春眠不觉晓" -o 练字帖.html
```

或者准备一个 TXT，每行一个词或一串生字，空白字符会被忽略：

```text
# 一年级下册生字
春
风
花
草
```

仓库里的 [examples/zitie.txt](examples/zitie.txt) 可以直接改。

## 用法

生成 8 列田字格，每行描红 2 个，每个字写 2 行：

```bash
tianzige -i examples/zitie.txt -o 练字帖.html --rows-per-char 2
```

米字格、每行 10 格、描红 3 个：

```bash
tianzige --text "永和九年" --grid mi --repeat 10 --trace 3 -o 米字格.html
```

低年级大格子练习，每页 8 行：

```bash
tianzige --text "人口手足" --repeat 6 --page-rows 8 -o 大格练习.html
```

## 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `-t, --text` | 与 `-i` 二选一 | 直接输入要练习的文字 |
| `-i, --input` | 与 `-t` 二选一 | 字词文本文件，`#` 开头为注释 |
| `-o, --output` | `练字帖.html` | 输出 HTML 路径 |
| `--title` | `练字帖` | 字帖标题 |
| `--grid` | `tian` | `tian` 田字格、`mi` 米字格、`fang` 方格 |
| `--repeat` | `8` | 每行格子数，1~12 |
| `--trace` | `2` | 每行描红格数，不能超过每行格子数 |
| `--rows-per-char` | `1` | 每个字写几行，1~5 |
| `--page-rows` | `10` | 每页行数，1~20 |

## 打印

浏览器打开生成的 HTML，按 `Ctrl/Cmd + P`：

- 纸张：A4 纵向
- 缩放：100%
- 勾选「背景图形」，格线才会显示

每页自带姓名和日期栏，适合直接发给学生。字体按 `Kaiti SC` → `KaiTi` → `STKaiti` 的顺序回退，没有楷体时会用系统衬线字体。

## 开发

```bash
python -m unittest discover -s tests -v
```

## License

[MIT](LICENSE) © 2026 eastyou
