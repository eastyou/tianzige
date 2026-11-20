"""命令行入口：生成可打印的田字格练字帖。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .layout import build_workbook
from .model import GRID_NAMES, GRID_STYLES, TianzigeError
from .render import render_page


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tianzige",
        description="田字格练字帖生成器：输入文字，输出可打印的 A4 字帖",
    )
    parser.add_argument("--version", action="version", version="tianzige 0.1.0")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", "--input", help="字词文本文件，空白字符会被忽略")
    source.add_argument("-t", "--text", help="直接输入要练习的文字")
    parser.add_argument("-o", "--output", default="练字帖.html", help="输出 HTML 路径")
    parser.add_argument("--title", default="练字帖", help="字帖标题")
    parser.add_argument(
        "--grid",
        choices=GRID_STYLES,
        default="tian",
        help="格子样式：tian 田字格、mi 米字格、fang 方格，默认 tian",
    )
    parser.add_argument(
        "--repeat", type=int, default=8, help="每行格子数，1~12，默认 8"
    )
    parser.add_argument(
        "--trace", type=int, default=2, help="每行描红格数，默认 2"
    )
    parser.add_argument(
        "--rows-per-char", type=int, default=1, help="每个字写几行，1~5，默认 1"
    )
    parser.add_argument(
        "--page-rows", type=int, default=10, help="每页行数，1~20，默认 10"
    )
    return parser


def _read_input(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    source = Path(args.input)
    if not source.exists():
        raise TianzigeError("文件不存在: %s" % args.input)
    if source.is_dir():
        raise TianzigeError("这是一个目录，需要文本文件: %s" % args.input)
    try:
        content = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise TianzigeError(
            "无法以 UTF-8 读取 %s，请另存为 UTF-8 编码" % args.input
        ) from None
    except OSError as exc:
        raise TianzigeError("读取文件失败: %s" % exc) from exc
    # 以 # 开头的行视为注释，方便在字词表里写说明
    return "\n".join(
        line for line in content.splitlines() if not line.strip().startswith("#")
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        text = _read_input(args)
        workbook = build_workbook(
            text,
            repeat=args.repeat,
            trace=args.trace,
            rows_per_char=args.rows_per_char,
            page_rows=args.page_rows,
        )
        meta = "%s · 共 %d 个字 · 每字 %d 行" % (
            GRID_NAMES[args.grid],
            len(workbook.chars),
            args.rows_per_char,
        )
        page = render_page(workbook, title=args.title, grid=args.grid, meta=meta)
    except TianzigeError as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2

    try:
        Path(args.output).write_text(page, encoding="utf-8")
    except OSError as exc:
        print("错误: 写入文件失败: %s" % exc, file=sys.stderr)
        return 1

    print(
        "已生成 %s：%d 个字，%d 行，%d 页（%s）"
        % (
            args.output,
            len(workbook.chars),
            workbook.row_count,
            workbook.page_count,
            GRID_NAMES[args.grid],
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
