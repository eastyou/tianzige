"""田字格字帖的数据结构与异常定义。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

GRID_STYLES = ("tian", "mi", "fang")

GRID_NAMES = {
    "tian": "田字格",
    "mi": "米字格",
    "fang": "方格",
}


class TianzigeError(ValueError):
    """参数不合法或没有可练习的字符。"""


@dataclass(frozen=True)
class Cell:
    """一个格子：``trace`` 为真时是浅色描红字。"""

    char: str
    trace: bool


Row = Tuple[Cell, ...]
Page = Tuple[Row, ...]


@dataclass(frozen=True)
class Workbook:
    """分好页的字帖。"""

    pages: Tuple[Page, ...]
    chars: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.pages:
            raise TianzigeError("字帖至少需要一页")
        if not self.chars:
            raise TianzigeError("字帖至少需要一个字")

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def row_count(self) -> int:
        return sum(len(page) for page in self.pages)

    @property
    def cell_width(self) -> int:
        return len(self.pages[0][0])
