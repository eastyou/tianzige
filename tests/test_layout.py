"""测试文字切分、行排版与分页。"""

from __future__ import annotations

import unittest

from tianzige.layout import build_rows, build_workbook, paginate, parse_chars
from tianzige.model import TianzigeError, Workbook


class ParseCharsTests(unittest.TestCase):
    def test_removes_whitespace(self) -> None:
        self.assertEqual(parse_chars("春 眠\n不觉\t晓"), ["春", "眠", "不", "觉", "晓"])

    def test_keeps_punctuation(self) -> None:
        self.assertEqual(parse_chars("你好，世界"), ["你", "好", "，", "世", "界"])

    def test_empty_rejected(self) -> None:
        with self.assertRaises(TianzigeError):
            parse_chars("   \n\t ")

    def test_non_text_rejected(self) -> None:
        with self.assertRaises(TianzigeError):
            parse_chars(None)  # type: ignore[arg-type]


class BuildRowsTests(unittest.TestCase):
    def test_row_count(self) -> None:
        rows = build_rows(["春", "眠"], repeat=6, trace=2, rows_per_char=3)
        self.assertEqual(len(rows), 6)
        self.assertEqual(len(rows[0]), 6)

    def test_trace_prefix(self) -> None:
        rows = build_rows(["春"], repeat=5, trace=2)
        flags = [cell.trace for cell in rows[0]]
        self.assertEqual(flags, [True, True, False, False, False])
        self.assertTrue(all(cell.char == "春" for cell in rows[0]))

    def test_zero_trace(self) -> None:
        rows = build_rows(["春"], repeat=4, trace=0)
        self.assertFalse(any(cell.trace for cell in rows[0]))

    def test_invalid_repeat(self) -> None:
        for repeat in (0, 13):
            with self.assertRaises(TianzigeError):
                build_rows(["春"], repeat=repeat)

    def test_invalid_trace(self) -> None:
        for trace in (-1, 9):
            with self.assertRaises(TianzigeError):
                build_rows(["春"], repeat=8, trace=trace)

    def test_invalid_rows_per_char(self) -> None:
        for value in (0, 6):
            with self.assertRaises(TianzigeError):
                build_rows(["春"], rows_per_char=value)

    def test_empty_chars(self) -> None:
        with self.assertRaises(TianzigeError):
            build_rows([])

    def test_blank_char_rejected(self) -> None:
        with self.assertRaises(TianzigeError):
            build_rows([" "])


class PaginateTests(unittest.TestCase):
    def test_splits_pages(self) -> None:
        rows = build_rows(["春", "眠", "不", "觉", "晓", "风", "雨"], repeat=4)
        workbook = paginate(rows, page_rows=3)
        self.assertEqual(workbook.page_count, 3)
        self.assertEqual([len(page) for page in workbook.pages], [3, 3, 1])
        self.assertEqual(workbook.row_count, 7)

    def test_cell_width(self) -> None:
        rows = build_rows(["春"], repeat=9)
        self.assertEqual(paginate(rows, page_rows=5).cell_width, 9)

    def test_chars_are_unique_in_order(self) -> None:
        rows = build_rows(["春", "春", "眠"], repeat=3)
        workbook = paginate(rows, page_rows=10)
        self.assertEqual(workbook.chars, ("春", "眠"))

    def test_invalid_page_rows(self) -> None:
        rows = build_rows(["春"], repeat=3)
        for value in (0, 21):
            with self.assertRaises(TianzigeError):
                paginate(rows, page_rows=value)

    def test_empty_rows(self) -> None:
        with self.assertRaises(TianzigeError):
            paginate([], page_rows=10)

    def test_build_workbook(self) -> None:
        workbook = build_workbook("春眠", repeat=6, trace=1, rows_per_char=2, page_rows=2)
        self.assertEqual(len(workbook.chars), 2)
        self.assertEqual(workbook.page_count, 2)
        self.assertEqual(workbook.row_count, 4)

    def test_empty_workbook_rejected(self) -> None:
        with self.assertRaises(TianzigeError):
            Workbook(pages=(), chars=("春",))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
