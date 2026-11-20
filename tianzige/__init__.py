"""tianzige：零依赖的田字格练字帖生成器。"""

from .layout import build_rows, build_workbook, paginate, parse_chars
from .model import GRID_STYLES, Cell, TianzigeError, Workbook
from .render import render_page

__version__ = "0.1.0"

__all__ = [
    "Cell",
    "GRID_STYLES",
    "TianzigeError",
    "Workbook",
    "build_rows",
    "build_workbook",
    "paginate",
    "parse_chars",
    "render_page",
    "__version__",
]
