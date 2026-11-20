"""测试字帖 HTML 输出。"""

from __future__ import annotations

import unittest

from tianzige.layout import build_workbook
from tianzige.model import TianzigeError
from tianzige.render import render_page


class RenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workbook = build_workbook(
            "春眠不觉晓", repeat=6, trace=2, rows_per_char=2, page_rows=4
        )

    def test_page_count(self) -> None:
        page = render_page(self.workbook)
        self.assertEqual(page.count('class="page"'), 3)
        self.assertIn("第 1 / 3 页", page)
        self.assertIn("第 3 / 3 页", page)

    def test_cell_count(self) -> None:
        page = render_page(self.workbook)
        self.assertEqual(page.count('class="cell'), 10 * 6)

    def test_trace_cells(self) -> None:
        page = render_page(self.workbook)
        self.assertEqual(page.count('class="cell trace"'), 10 * 2)

    def test_grid_style_class(self) -> None:
        self.assertIn('class="grid mi"', render_page(self.workbook, grid="mi"))
        self.assertIn('class="grid fang"', render_page(self.workbook, grid="fang"))

    def test_columns_variable(self) -> None:
        self.assertIn("--cols: 6", render_page(self.workbook))

    def test_title_escaped(self) -> None:
        page = render_page(self.workbook, title="<b>练字</b>")
        self.assertNotIn("<b>练字</b>", page)
        self.assertIn("&lt;b&gt;", page)

    def test_char_escaped(self) -> None:
        workbook = build_workbook("<", repeat=3, page_rows=1)
        page = render_page(workbook)
        self.assertIn("&lt;", page)
        self.assertNotIn("<div class=\"cell\"><</div>", page)

    def test_invalid_grid(self) -> None:
        with self.assertRaises(TianzigeError):
            render_page(self.workbook, grid="circle")

    def test_blank_title(self) -> None:
        with self.assertRaises(TianzigeError):
            render_page(self.workbook, title="   ")

    def test_meta_rendered(self) -> None:
        page = render_page(self.workbook, meta="米字格 · 共 5 个字")
        self.assertIn("米字格 · 共 5 个字", page)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
