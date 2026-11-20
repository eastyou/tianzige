"""把字帖渲染成多页 A4 打印页面。"""

from __future__ import annotations

import html
from typing import List, Sequence

from .model import GRID_NAMES, GRID_STYLES, TianzigeError, Workbook

PAGE_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 18px 20px 24px;
    background: #f8fafc;
    color: #0f172a;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  }
  .page {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 18px 18px;
    margin: 0 auto 18px;
    max-width: 920px;
  }
  .page-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 14px;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }
  .page-head h1 { font-size: 19px; margin: 0; letter-spacing: 1px; }
  .page-head .meta { color: #64748b; font-size: 11px; margin-top: 3px; }
  .fields {
    display: flex;
    gap: 14px;
    color: #334155;
    font-size: 11px;
    white-space: nowrap;
  }
  .fields span { border-bottom: 1px solid #94a3b8; padding: 0 16px 2px 4px; }
  .grid {
    display: grid;
    grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
  }
  .cell {
    position: relative;
    aspect-ratio: 1 / 1;
    border: 1px solid #f0a8a8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "Kaiti SC", "KaiTi", "STKaiti", "Noto Serif CJK SC", serif;
    font-size: clamp(16px, 3.1vw, 38px);
    line-height: 1;
    color: #0f172a;
    user-select: none;
  }
  .cell.trace { color: #d4d4d8; }
  .grid.tian .cell::before,
  .grid.tian .cell::after,
  .grid.mi .cell::before,
  .grid.mi .cell::after {
    content: "";
    position: absolute;
    pointer-events: none;
  }
  .grid.tian .cell::before,
  .grid.mi .cell::before {
    left: 50%;
    top: 0;
    bottom: 0;
    border-left: 1px dashed #f0a8a8;
  }
  .grid.tian .cell::after,
  .grid.mi .cell::after {
    top: 50%;
    left: 0;
    right: 0;
    border-top: 1px dashed #f0a8a8;
  }
  .grid.mi .cell {
    background-image:
      linear-gradient(45deg, transparent calc(50% - 0.5px), #f7caca calc(50% - 0.5px), #f7caca calc(50% + 0.5px), transparent calc(50% + 0.5px)),
      linear-gradient(-45deg, transparent calc(50% - 0.5px), #f7caca calc(50% - 0.5px), #f7caca calc(50% + 0.5px), transparent calc(50% + 0.5px));
  }
  footer {
    color: #94a3b8;
    font-size: 11px;
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
  }
  @page { size: A4 portrait; margin: 10mm; }
  @media print {
    body { background: #fff; padding: 0; }
    .page {
      border: none;
      border-radius: 0;
      padding: 0;
      margin: 0;
      max-width: none;
    }
    .page + .page { break-before: page; }
    .cell { border-color: #e79a9a; }
    * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
</style>
</head>
<body>
__PAGES__
</body>
</html>
"""

PAGE_BLOCK = """<section class="page">
  <div class="page-head">
    <div>
      <h1>__TITLE__</h1>
      <div class="meta">__META__</div>
    </div>
    <div class="fields">
      <div>姓名<span>&nbsp;</span></div>
      <div>日期<span>&nbsp;</span></div>
    </div>
  </div>
  <div class="grid __STYLE__" style="--cols: __COLS__">
__CELLS__
  </div>
  <footer>
    <span>tianzige · 第 __INDEX__ / __TOTAL__ 页</span>
    <span>A4 纵向打印，建议缩放 100%</span>
  </footer>
</section>"""


def _render_cells(rows: Sequence[Sequence[object]]) -> str:
    cells: List[str] = []
    for row in rows:
        for cell in row:
            trace = bool(getattr(cell, "trace", False))
            char = str(getattr(cell, "char", ""))
            classes = "cell trace" if trace else "cell"
            cells.append(
                '<div class="%s">%s</div>' % (classes, html.escape(char))
            )
    return "\n".join(cells)


def render_page(
    workbook: Workbook,
    title: str = "练字帖",
    grid: str = "tian",
    meta: str = "",
) -> str:
    """生成整份字帖 HTML；参数不合法时抛出 ``TianzigeError``。"""
    if not title.strip():
        raise TianzigeError("标题不能为空")
    if grid not in GRID_STYLES:
        raise TianzigeError("格子样式只能是 tian、mi 或 fang")

    blocks: List[str] = []
    total = workbook.page_count
    for index, page in enumerate(workbook.pages, start=1):
        block = PAGE_BLOCK
        replacements = {
            "__TITLE__": html.escape(title.strip()),
            "__META__": html.escape(meta.strip())
            or "%s · 每字 %d 行" % (GRID_NAMES[grid], workbook.row_count),
            "__STYLE__": grid,
            "__COLS__": str(workbook.cell_width),
            "__CELLS__": _render_cells(page),
            "__INDEX__": str(index),
            "__TOTAL__": str(total),
        }
        for key, value in replacements.items():
            block = block.replace(key, value)
        blocks.append(block)

    return PAGE_TEMPLATE.replace("__PAGES__", "\n".join(blocks))
