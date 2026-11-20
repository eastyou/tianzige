"""把输入文字切分并排成田字格行与页。"""

from __future__ import annotations

from typing import List, Sequence

from .model import Cell, Page, TianzigeError, Workbook


def parse_chars(text: str) -> List[str]:
    """去掉所有空白字符，保留汉字、字母、数字和标点。"""
    if not isinstance(text, str):
        raise TianzigeError("输入内容必须是文本")
    chars = [char for char in text if not char.isspace()]
    if not chars:
        raise TianzigeError("没有可练习的字，请检查输入内容")
    return chars


def build_rows(
    chars: Sequence[str],
    repeat: int = 8,
    trace: int = 2,
    rows_per_char: int = 1,
) -> List[List[Cell]]:
    """每个字占 ``rows_per_char`` 行，每行写满 ``repeat`` 个格子。

    每行前 ``trace`` 个格子是描红，其余留白。
    """
    if not chars:
        raise TianzigeError("至少需要一个字")
    if not 1 <= repeat <= 12:
        raise TianzigeError("每行格子数必须在 1 到 12 之间")
    if not 0 <= trace <= repeat:
        raise TianzigeError("描红数量必须在 0 到每行格子数之间")
    if not 1 <= rows_per_char <= 5:
        raise TianzigeError("每个字的行数必须在 1 到 5 之间")

    rows: List[List[Cell]] = []
    for char in chars:
        if not char.strip():
            raise TianzigeError("不能包含空白字符")
        for _ in range(rows_per_char):
            row: List[Cell] = []
            for index in range(repeat):
                row.append(Cell(char=char, trace=index < trace))
            rows.append(row)
    return rows


def paginate(rows: Sequence[Sequence[Cell]], page_rows: int = 10) -> Workbook:
    """按每页行数切分，返回可以直接渲染的字帖。"""
    if not 1 <= page_rows <= 20:
        raise TianzigeError("每页行数必须在 1 到 20 之间")
    if not rows:
        raise TianzigeError("没有可排版的字")

    pages: List[Page] = []
    for start in range(0, len(rows), page_rows):
        chunk = tuple(tuple(row) for row in rows[start : start + page_rows])
        if chunk:
            pages.append(chunk)

    chars: List[str] = []
    for row in rows:
        if row:
            char = row[0].char
            if char not in chars:
                chars.append(char)

    return Workbook(pages=tuple(pages), chars=tuple(chars))


def build_workbook(
    text: str,
    repeat: int = 8,
    trace: int = 2,
    rows_per_char: int = 1,
    page_rows: int = 10,
) -> Workbook:
    """从原始文字一路生成字帖。"""
    chars = parse_chars(text)
    rows = build_rows(chars, repeat=repeat, trace=trace, rows_per_char=rows_per_char)
    return paginate(rows, page_rows=page_rows)
